"""Build the types in ray_types using Mypy."""
import typing

from mypy.nodes import (
    ARG_OPT,
    Argument,
    Block,
    ClassDef,
    FuncDef,
    SymbolTable,
    TypeInfo,
)
from mypy.plugin import AnalyzeTypeContext, ClassDefContext
from mypy.semanal import SemanticAnalyzer
from mypy.types import Instance
from mypy.types import Type as MypyType
from mypy.types import TypeVarLikeType
from typed_ray import ray_types, utils


def build_options_args(api: SemanticAnalyzer) -> typing.List[Argument]:
    """Build the arguments for the ActorHandle.options method."""
    return [
        utils.build_argument(arg_name, api.named_type(arg_type_str), arg_type=ARG_OPT)
        for arg_name, arg_type_str in ray_types.OPTIONS_KWARGS.items()
    ]


def build_type_info(
    api: SemanticAnalyzer,
    module_name: str,
    cls_full_name: str,
    column: int = -1,
    line: int = -1,
    class_def: typing.Optional[ClassDef] = None,
    class_name: typing.Optional[str] = None,
    type_vars: typing.Optional[typing.List[TypeVarLikeType]] = None,
) -> TypeInfo:
    """Build a well constructed TypeInfo object."""
    if type_vars is None:
        type_vars = []
    if class_def is None:
        assert (
            class_name is not None
        ), "One of class_def and class_name must be specified"
        class_def = ClassDef(
            name=class_name,
            defs=Block([]),
            type_vars=type_vars,
        )
        class_def.column = column
        class_def.line = line
        class_def.fullname = cls_full_name
    result = TypeInfo(
        names=SymbolTable(),
        defn=class_def,
        module_name=module_name,
    )
    class_def.info = result
    result._fullname = cls_full_name  # type: ignore
    result.bases = [api.named_type("builtins.object")]
    object_type = api.named_type("builtins.object").type  # type: ignore
    assert isinstance(object_type, TypeInfo)
    result.mro = [result, object_type]
    return result


def build_object_ref(
    ctx: typing.Union[ClassDefContext, AnalyzeTypeContext], wraps: MypyType
) -> MypyType:
    """Build the type of the object reference."""
    utils.add_object_ref_to_context(ctx)
    api = utils.get_sem_api(ctx)
    obj_ref_info: TypeInfo = api.lookup_fully_qualified(
        ray_types.ObjectRefFullName
    ).node  # type: ignore
    return Instance(obj_ref_info, [wraps])


def build_remote_method_info(
    api: SemanticAnalyzer,
    module_name: str,
    column: int,
    line: int,
    cls_full_name: str,
) -> TypeInfo:
    return build_type_info(
        api=api,
        module_name=module_name,
        cls_full_name=cls_full_name,
        column=column,
        line=line,
        class_name="RemoteFunction",
    )


def build_remote_method(
    ctx: typing.Union[ClassDefContext, AnalyzeTypeContext],
    method: FuncDef,
) -> MypyType:
    api = utils.get_sem_api(ctx)
    info: TypeInfo = method.info  # type: ignore
    remote_method_info = build_remote_method_info(
        api=api,
        module_name=info.module_name,
        cls_full_name=info._fullname,  # type: ignore
        column=method.column,  # type: ignore
        line=method.line,  # type: ignore
    )
    method_ret_type = utils.get_return_type(method)
    bound_method_ret_type = utils.unbound_to_instance(api, method_ret_type)
    return_type = build_object_ref(ctx, bound_method_ret_type)
    remote_method = utils.build_func_def(
        args=method.arguments[1:],  # type: ignore
        return_type=return_type,
        fallback=api.named_type("builtins.function"),
        func_info=remote_method_info,
        name="remote",
        body=method.body,
    )
    utils.add_method(
        name="remote", func=remote_method, cls_info=remote_method_info, replace=True
    )
    return Instance(remote_method_info, [bound_method_ret_type])


def build_actor_class_info(
    ctx: typing.Union[ClassDefContext, AnalyzeTypeContext],
    methods: typing.List[FuncDef],
) -> TypeInfo:
    """Build the Actor class TypeInfo for an object having methods `methods`."""
    api = utils.get_sem_api(ctx)

    result = build_type_info(
        api=api,
        module_name="typed_ray.ray_types",
        cls_full_name="typed_ray.ray_types.ActorHandle",
        class_name="ActorHandle",
    )
    for method in methods:
        type_ = build_remote_method(ctx, method)
        utils.add_attribute(name=method.name, cls=result.defn, type_=type_)
    return result


def build_actor_class_instance(
    ctx: typing.Union[ClassDefContext, AnalyzeTypeContext],
    methods: typing.List[FuncDef],
    decorated_cls: MypyType,
) -> MypyType:
    """Build the Actor class instance for an object having methods `methods`."""
    return Instance(build_actor_class_info(ctx=ctx, methods=methods), [decorated_cls])
