from types import NoneType
from typing import Annotated, Literal
import pydantic


class E2Keyword(pydantic.BaseModel):
    keyword: Literal[
        "if",
        "else",
        "elseif",
        "switch",
        "case",
        "default",
        "break",
        "continue",
        "for",
        "foreach",
        "while",
        "do",
        "function",
        "let",
        "local",
        "const",
        "return",
    ]


class E2Operator(pydantic.BaseModel):
    operator: Literal[
        "++",
        "--",
        "~",
        "$",
        "->",
        "(",
        ")",
        ":",
        "[",
        "]",
        "+",
        "-",
        "!",
        "^",
        "*",
        "/",
        "%",
        "+",
        "-",
        "<<",
        ">>",
        ">",
        "<",
        ">=",
        "<=",
        "==",
        "!=",
        "^^",
        "&&",
        "||",
        "&",
        "|",
        "?",
        "?:",
        "=",
    ]


class E2Type(pydantic.BaseModel):
    type: Literal[
        "void",
        "number",
        "string",
        "array",
        "table",
        "function",
        "vector2",
        "vector3",
        "vector4",
        "entity",
        "angle",
        "ranger",
        "bone",
        "matrix2",
        "matrix3",
        "matrix4",
        "wirelink",
        "complex",
        "quaternion",
    ]


def is_not_empty(s: str) -> str:
    if s == "":
        raise ValueError(f"{s} is empty")
    return s


def is_lower(s: str) -> str:
    if s.isupper():
        raise ValueError(f"{s} is uppercase")
    return s


def is_upper(s: str) -> str:
    if s.islower():
        raise ValueError(f"{s} is lowercase")
    return s


def starts_with_character(s: str) -> str:
    if s[0].isdigit():
        raise ValueError(f"Identifier {s} starts with a digit")
    elif s[0].isspace():
        raise ValueError(f"Identifier {s} starts with a space")
    return s


def E2FunctionIdentifierAfterValidator(s: str) -> str:
    s = is_not_empty(s)
    s = is_lower(s)
    s = starts_with_character(s)
    return s


def E2VariableIdentifierAfterValidator(s: str) -> str:
    s = is_not_empty(s)
    s = is_upper(s)
    s = starts_with_character(s)
    return s


class E2VariableIdentifier(pydantic.BaseModel):
    id: Annotated[str, pydantic.AfterValidator(E2VariableIdentifierAfterValidator)]


class E2FunctionIdentifier(pydantic.BaseModel):
    id: Annotated[str, pydantic.AfterValidator(E2FunctionIdentifierAfterValidator)]


class E2Argument(pydantic.BaseModel):
    id: E2VariableIdentifier
    type: E2Type


class E2FunctionDefinition(pydantic.BaseModel):
    id: E2FunctionIdentifier
    return_type: E2Type
    arguments: list[E2Argument] | list[NoneType]
