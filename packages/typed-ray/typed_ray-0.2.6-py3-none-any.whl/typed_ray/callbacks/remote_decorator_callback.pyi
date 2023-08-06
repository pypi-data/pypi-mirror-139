from mypy.nodes import ClassDef as ClassDef
from mypy.plugin import ClassDefContext as ClassDefContext, Plugin as Plugin
from typing import Any

class ActorClassTransformer:
    ctx: Any
    api: Any
    class_def: Any
    reason: Any
    info: Any
    symbol_table: Any
    body: Any
    def __init__(self, ctx: ClassDefContext) -> None: ...
    def transform(self) -> ClassDef: ...

class RayWorkerDecoratorCallback:
    plugin: Plugin
    fullname: str
    def __call__(self, ctx: ClassDefContext) -> None: ...
    def __init__(self, plugin: Plugin, fullname: str) -> None: ...
