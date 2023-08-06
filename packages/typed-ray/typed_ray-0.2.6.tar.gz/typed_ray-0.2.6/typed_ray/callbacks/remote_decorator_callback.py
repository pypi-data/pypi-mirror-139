import typing

from dataclasses import dataclass
from mypy.nodes import Argument, ClassDef, Expression, FuncDef, SymbolTable, TypeInfo
from mypy.plugin import ClassDefContext, Plugin, SemanticAnalyzerPluginInterface
from mypy.semanal import SemanticAnalyzer
from mypy.types import Instance, TypeType
from mypy.types import Type as MypyType
from mypy.types import TypeVarType
from typed_ray import build_ray_types, utils


class ActorClassTransformer:
    """Transforms Actor class to a new class with a new base class."""

    def __init__(self, ctx: ClassDefContext):
        self.ctx = ctx
        self.api: SemanticAnalyzer = ctx.api
        self.class_def: ClassDef = ctx.cls
        self.reason: Expression = ctx.reason
        self.info: TypeInfo = ctx.cls.info
        self.symbol_table: SymbolTable = self.info.names
        # TODO: Figure out why pyright complains about this.
        self.body: typing.List[FuncDef] = self.class_def.defs.body  # type: ignore

    def transform(self) -> None:
        """Transforms Actor class to a new class with a new base class."""
        self._add_remote_init_method()
        self._add_options_method()

    def _add_remote_init_method(self) -> None:
        """Add remote method to the class.

        @ray.remote
        class A:
            def __init__(self):
                pass

        a = A.remote()

        This method lets mypy return type of a as ActorHandle[A].
        """
        self._add_class_method(
            name="remote",
            args=self._get_method_args("__init__"),
            return_type=build_ray_types.build_actor_class_instance(
                ctx=self.ctx,
                methods=utils.get_non_magic_methods(self.class_def),
                decorated_cls=self._get_my_type(),
            ),
        )

    def _add_options_method(self) -> None:
        """Add options method to the class.

        @ray.remote
        class A:
            def __init__(self):
                pass

        a = A.options(...).remote()
        """
        self._add_class_method(
            name="options",
            args=build_ray_types.build_options_args(self.api),
            return_type=TypeType(self._get_my_type()),
        )

    def _add_class_method(
        self,
        name: str,
        args: typing.List[Argument],
        return_type: MypyType,
        tvar_def: typing.Optional[TypeVarType] = None,
    ):
        # First remove any previously generated methods with the same name
        # to avoid clashes and problems in the semantic analyzer.
        if name in self.info.names:
            sym = self.info.names[name]
            if sym.plugin_generated and isinstance(sym.node, FuncDef):  # type: ignore
                self.class_def.defs.body.remove(sym.node)  # type: ignore

        assert isinstance(self.api, SemanticAnalyzerPluginInterface)
        function_type = self.api.named_type("builtins.function")

        func = utils.build_func_def(
            args=args,
            return_type=return_type,
            fallback=function_type,
            func_info=self.info,
            name=name,
            tvar_def=tvar_def,
            is_static=True,
        )
        utils.add_method(name=name, func=func, cls_info=self.info)

    def _get_method_args(self, method_name: str) -> typing.List[Argument]:
        """Get arguments of method belonging to the class.

        class A:
            def foo(a: int, b: Dict[str, int]):
                pass

        _get_method_args("__init__")  # Returns [Argument(a, ...), Argument(b, ...)]
        or rather their mypy representations.
        """
        args = []
        for stmt in self.body:
            if isinstance(stmt, FuncDef) and stmt.name == method_name:
                # Skip self argument.
                args = stmt.arguments[1:]  # type: ignore
                break
        return args  # type: ignore

    def _get_ray_exposed_methods(self) -> typing.List[FuncDef]:
        """Get methods of the decorated class."""
        return [
            stmt
            for stmt in self.body
            if isinstance(stmt, FuncDef) and not utils.is_magic_method(stmt.name)
        ]

    def _get_my_type(self) -> MypyType:
        """Get mypy representation of the class."""
        return Instance(self.info, [])


@dataclass()
class RayWorkerDecoratorCallback:
    plugin: Plugin
    fullname: str

    def __call__(self, ctx: ClassDefContext) -> None:
        transformer = ActorClassTransformer(ctx)
        transformer.transform()
