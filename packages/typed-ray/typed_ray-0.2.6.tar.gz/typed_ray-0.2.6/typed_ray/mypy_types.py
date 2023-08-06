"""Type aliases for various types and callbacks defined in mypy."""
import typing

from mypy.plugin import AnalyzeTypeContext, ClassDefContext
from mypy.types import Type as MypyType

ClassDecoratorHookCallback = typing.Callable[[ClassDefContext], None]
TypeAnalyzeHookCallback = typing.Callable[[AnalyzeTypeContext], MypyType]
