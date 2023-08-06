from mypy.plugin import AnalyzeTypeContext, Plugin
from mypy.types import Type as MypyType


class ActorHandleTypeAnalyzeHookCallback:
    def __init__(self, plugin: Plugin, fullname: str) -> None: ...

    def __call__(self, ctx: AnalyzeTypeContext) -> MypyType: ...
