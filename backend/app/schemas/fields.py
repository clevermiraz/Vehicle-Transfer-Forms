"""Reusable validated field types. Bangla digits, spaces and dashes are accepted on input."""

import re
from datetime import date
from typing import Annotated, Literal

from pydantic import AfterValidator, BeforeValidator, StringConstraints

from app.services.normalize import clean_text, digits_only, normalize_phone


def _optional(fn):
    return lambda v: None if clean_text(v) is None else fn(clean_text(v))


def _nid(v: str) -> str:
    v = digits_only(v)
    if not re.fullmatch(r"\d{10}|\d{13}|\d{17}", v):
        raise ValueError("NID must be 10, 13 or 17 digits")
    return v


def _tin(v: str) -> str:
    v = digits_only(v)
    if not re.fullmatch(r"\d{12}", v):
        raise ValueError("TIN must be 12 digits")
    return v


def _phone(v: str) -> str:
    v = normalize_phone(v)
    if not re.fullmatch(r"01[3-9]\d{8}", v):
        raise ValueError("Mobile must look like 01XXXXXXXXX (11 digits)")
    return v


def _upper(v: str) -> str:
    return v.upper()


def _not_future(v: date | None) -> date | None:
    if v and v > date.today():
        raise ValueError("Date cannot be in the future")
    return v


def Text(max_length: int):  # noqa: N802 - reads like a type
    return Annotated[
        Annotated[str, StringConstraints(max_length=max_length)] | None,
        BeforeValidator(clean_text),
    ]


def RequiredText(max_length: int):  # noqa: N802
    return Annotated[str, BeforeValidator(clean_text), StringConstraints(min_length=1, max_length=max_length)]


Nid = Annotated[str | None, BeforeValidator(_optional(_nid))]
Tin = Annotated[str | None, BeforeValidator(_optional(_tin))]
Phone = Annotated[str | None, BeforeValidator(_optional(_phone))]
Gender = Annotated[Literal["MALE", "FEMALE", "OTHER"] | None, BeforeValidator(_optional(_upper))]
OptionalDate = Annotated[date | None, BeforeValidator(lambda v: v or None)]
PastDate = Annotated[OptionalDate, AfterValidator(_not_future)]
