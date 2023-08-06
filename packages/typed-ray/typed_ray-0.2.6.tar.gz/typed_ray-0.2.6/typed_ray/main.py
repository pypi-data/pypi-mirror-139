import typing

from mypy.plugin import Plugin
from typed_ray import callbacks, constants, mypy_types


class _RayPlugin(Plugin):
    def get_type_analyze_hook(
        self, fullname: str
    ) -> typing.Optional[mypy_types.TypeAnalyzeHookCallback]:
        if fullname.endswith(constants.ACTOR_HANDLE_TYPE):
            return callbacks.ActorHandleTypeAnalyzeHookCallback(self, fullname)

    def get_class_decorator_hook(
        self, fullname: str
    ) -> typing.Optional[mypy_types.ClassDecoratorHookCallback]:
        if fullname.endswith(constants.TYPED_RAY_REMOTE_DECORATOR):
            return callbacks.RayWorkerDecoratorCallback(self, fullname)


def plugin(version: str) -> typing.Type[Plugin]:
    return _RayPlugin
