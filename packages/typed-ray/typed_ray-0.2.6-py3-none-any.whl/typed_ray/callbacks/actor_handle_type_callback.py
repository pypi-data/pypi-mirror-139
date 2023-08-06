import typing
from dataclasses import dataclass
from mypy.plugin import Plugin, AnalyzeTypeContext
from mypy.types import Instance, Type as MypyType, UnboundType
from mypy.typeanal import TypeAnalyser

from typed_ray import build_ray_types, utils


@dataclass()
class ActorHandleTypeAnalyzeHookCallback:
    plugin: Plugin
    fullname: str

    def __call__(self, ctx: AnalyzeTypeContext) -> MypyType:
        api: TypeAnalyser = ctx.api
        type_: UnboundType = ctx.type
        args: typing.Optional[typing.Sequence[MypyType]] = type_.args  # type: ignore
        assert args is not None
        # Only a single class can be wrapped in an ActorHandle
        assert len(args) == 1
        wrapped_type: Instance = api.analyze_type(args[0])  # type: ignore
        return build_ray_types.build_actor_class_instance(
            ctx=ctx,
            methods=utils.get_non_magic_methods(wrapped_type),
            decorated_cls=wrapped_type,
        )
