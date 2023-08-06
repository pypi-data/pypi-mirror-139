import typing
from mypy.plugin import Plugin
from typed_ray import mypy_types as mypy_types

class _RayPlugin(Plugin):
    def get_type_analyze_hook(self, fullname: str) -> typing.Optional[mypy_types.TypeAnalyzeHookCallback]: ...
    def get_class_decorator_hook(
        self, fullname: str
    ) -> typing.Optional[mypy_types.ClassDecoratorHookCallback]: ...

def plugin(version: str) -> Plugin: ...
