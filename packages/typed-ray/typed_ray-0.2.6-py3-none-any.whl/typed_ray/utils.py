# pyright: reportPrivateUsage=false
import typing
from pprint import pformat, pprint

from mypy.nodes import (
    ARG_POS,
    MDEF,
    ArgKind,
    Argument,
    Block,
    ClassDef,
    FuncDef,
    PassStmt,
    SymbolTableNode,
    TypeAlias,
    TypeInfo,
    TypeVarExpr,
    Var,
)
from mypy.plugin import AnalyzeTypeContext, ClassDefContext, DynamicClassDefContext
from mypy.semanal import SemanticAnalyzer
from mypy.semanal_shared import set_callable_name
from mypy.types import AnyType, CallableType, Instance, NoneType
from mypy.types import Type as MypyType
from mypy.types import TypeOfAny, TypeVarType, UnboundType, UnionType
from mypy.typevars import fill_typevars


def get_sem_api(
    ctx: typing.Union[ClassDefContext, DynamicClassDefContext, AnalyzeTypeContext]
) -> SemanticAnalyzer:
    if isinstance(ctx, (ClassDefContext, DynamicClassDefContext)):
        return ctx.api
    return ctx.api.api


def get_class_def(instance: Instance) -> ClassDef:
    return instance.type.defn  # type: ignore


def get_func_defs(class_def: ClassDef) -> typing.List[FuncDef]:
    return [x for x in class_def.defs.body if isinstance(x, FuncDef)]  # type: ignore


def get_non_magic_methods(
    body: typing.Union[Instance, ClassDef]
) -> typing.List[FuncDef]:
    try:
        class_def = get_class_def(body) if isinstance(body, Instance) else body
        methods: typing.List[FuncDef] = get_func_defs(class_def)

        return [f for f in methods if not is_magic_method(f.name)]  # type: ignore
    except AttributeError:
        return []


def build_argument(
    name: str,
    type_: typing.Optional[MypyType] = None,
    arg_type: ArgKind = ARG_POS,
) -> Argument:
    """Builds a function argument."""
    if type_ is None:
        type_ = AnyType(TypeOfAny.unannotated)
    return Argument(Var(name, type_), type_, None, arg_type)


def build_func_def(
    args: typing.List[Argument],
    return_type: MypyType,
    fallback: Instance,
    func_info: TypeInfo,
    name: str,
    tvar_def: typing.Optional[TypeVarType] = None,
    self_type: typing.Optional[MypyType] = None,
    is_static: bool = False,
    is_property: bool = False,
    body: typing.Optional[Block] = None,
) -> FuncDef:
    if not is_static:
        self_type = self_type or fill_typevars(func_info)
        args = [Argument(Var("self"), self_type, None, ARG_POS)] + args
    arg_types, arg_names, arg_kinds = [], [], []
    for arg in args:
        assert arg.type_annotation, "All arguments must be fully typed."  # type: ignore
        arg_types.append(arg.type_annotation)  # type: ignore
        arg_names.append(arg.variable.name)  # type: ignore
        arg_kinds.append(arg.kind)  # type: ignore

    signature = CallableType(arg_types, arg_kinds, arg_names, return_type, fallback)  # type: ignore
    if tvar_def:
        signature.variables = [tvar_def]
    if not body:
        body = Block([PassStmt()])
    func = FuncDef(name, args, body)
    func.info = func_info
    func.type = set_callable_name(signature, func)
    func._fullname = func_info.fullname + "." + name  # type: ignore
    func.line = func_info.line  # type: ignore
    func.is_static = is_static
    func.is_property = is_property
    return func


def add_method(
    name: str, func: FuncDef, cls_info: TypeInfo, replace: bool = False
) -> None:
    # First remove any previously generated methods with the same name
    # to avoid clashes and problems in the semantic analyzer.
    if name in cls_info.names:
        sym = cls_info.names[name]
        if sym.plugin_generated and isinstance(sym.node, FuncDef):  # type: ignore
            try:
                cls_info.defn.defs.body.remove(sym.node)  # type: ignore
            except ValueError:
                pass
    # NOTE: we would like the plugin generated node to dominate, but we still
    # need to keep any existing definitions so they get semantically analyzed.
    if name in cls_info.names and not replace:
        # Get a nice unique name instead.
        return
        # r_name = get_unique_redefinition_name(name, cls_info.names)
        # cls_info.names[r_name] = cls_info.names[name]

    cls_info.names[name] = SymbolTableNode(MDEF, func, plugin_generated=True)
    cls_info.defn.defs.body.append(func)  # type: ignore


def add_attribute(name: str, cls: ClassDef, type_: MypyType) -> None:
    var = Var(name)
    var.info = cls.info
    var.type = type_
    var._fullname = cls.info.fullname + "." + name  # type: ignore
    cls.info.names[name] = SymbolTableNode(MDEF, var)


def add_global(
    ctx: typing.Union[ClassDefContext, DynamicClassDefContext, AnalyzeTypeContext],
    module: str,
    symbol_name: str,
    asname: str,
) -> None:
    if isinstance(ctx, (ClassDefContext, DynamicClassDefContext)):
        api: SemanticAnalyzer = ctx.api
    else:
        api: SemanticAnalyzer = ctx.api.api
    module_globals = api.modules[api.cur_mod_id].names  # type: ignore
    if asname not in module_globals:
        lookup_sym: SymbolTableNode = api.modules[module].names[symbol_name]

        module_globals[asname] = lookup_sym


def add_remote_method_to_context(ctx: ClassDefContext) -> None:
    add_global(
        ctx,
        "typed_ray.ray_types",
        "RemoteFunction",
        "__tr_RemoteMethod",
    )


def add_actor_class_to_context(ctx: ClassDefContext) -> None:
    add_global(
        ctx,
        "typed_ray.ray_types",
        "ActorClass",
        "__tr_ActorClass",
    )


def add_object_ref_to_context(
    ctx: typing.Union[ClassDefContext, AnalyzeTypeContext]
) -> None:
    add_global(
        ctx,
        "typed_ray.ray_types",
        "ObjectRef",
        "__tr_ObjectRef",
    )


def is_magic_method(name: str) -> bool:
    return name.startswith("__") and name.endswith("__")


def get_return_type(method: FuncDef) -> MypyType:
    try:
        return method.type.ret_type  # type: ignore
    except AttributeError:
        return AnyType(TypeOfAny.unannotated)


def var_to_type(var: Var) -> MypyType:
    return var.type or AnyType(TypeOfAny.unannotated)


def unbound_to_instance(api: SemanticAnalyzer, type_: MypyType) -> MypyType:
    if not isinstance(type_, UnboundType):
        return type_

    type_name: str = type_.name  # type: ignore

    if type_name == "Optional":
        # convert from "Optional?" to the more familiar
        # UnionType[..., NoneType()]
        return unbound_to_instance(
            api,
            UnionType(
                [unbound_to_instance(api, typ_arg) for typ_arg in type_.args]  # type: ignore
                + [NoneType()]
            ),
        )

    node = api.lookup(type_name, type_)

    if node is None or not isinstance(node, SymbolTableNode):  # type: ignore
        return type_
    bound_type = node.node  # type: ignore
    if isinstance(bound_type, Var) and bound_type.name == "None":
        return NoneType()
    if isinstance(bound_type, Var):
        bound_type = var_to_type(bound_type)  # type: ignore
    args: typing.List[MypyType] = []
    for arg in type_.args:  # type: ignore
        if isinstance(arg, UnboundType):
            args.append(unbound_to_instance(api, arg))
        elif isinstance(arg, TypeVarExpr):
            args.extend(arg.values)
        else:
            assert isinstance(arg, MypyType)
            args.append(arg)
    if isinstance(bound_type, TypeAlias):
        bound_type = bound_type.target.type  # type: ignore
    assert isinstance(bound_type, TypeInfo), type(bound_type)  # type: ignore
    return Instance(bound_type, args)  # type: ignore


def pformat_(
    x: typing.Any, seen: typing.Optional[typing.Set[int]] = None
) -> typing.Any:
    if seen is None:
        seen = set()
    if isinstance(x, list):
        if not x:
            return "[]"
        list_result: typing.List[str] = []
        for y in x:  # type: ignore
            list_result.append(pformat_(y, seen))
            seen.add(id(y))  # type: ignore
        return list_result
    if isinstance(x, str):
        return x
    result: typing.Dict[str, typing.Any] = {}
    for name in dir(x):
        try:
            value = getattr(x, name)
        except (AttributeError, AssertionError):
            continue
        value_id = id(value)
        if name.startswith("__") and name.endswith("__"):
            continue
        if value_id in seen:
            continue
        seen.add(value_id)
        result[name] = pformat_(value, seen)
    result["class"] = type(x)
    result["id"] = id(x)
    return result


def print_(x: typing.Any) -> None:
    as_str = f"----------{type(x)}----------\n"
    as_str += pformat(pformat_(x))
    as_str += "\n"
    as_str += "-----------------------------"
    pprint(as_str)
