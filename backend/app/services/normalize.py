"""Input cleaning shared by validation and search."""

import re
import unicodedata

_BANGLA_DIGITS = str.maketrans("০১২৩৪৫৬৭৮৯", "0123456789")


def clean_text(value: object) -> str | None:
    """Collapse whitespace; empty -> None."""
    if value is None:
        return None
    text = " ".join(str(value).split())
    return text or None


def ascii_digits(value: str) -> str:
    return value.translate(_BANGLA_DIGITS)


def digits_only(value: str) -> str:
    """Bangla digits -> ASCII, and drop spaces/dashes people type inside numbers."""
    return re.sub(r"[\s\-]", "", ascii_digits(value))


def normalize_phone(value: str) -> str:
    phone = digits_only(value)
    if phone.startswith("+880"):
        phone = "0" + phone[4:]
    elif phone.startswith("880") and len(phone) == 13:
        phone = "0" + phone[3:]
    return phone


def normalize_registration(value: str) -> str:
    """'Dhaka Metro-GA 12-3456' -> 'DHAKAMETROGA123456' (Bangla letters kept)."""
    # Keep letters, digits and combining marks (Bangla vowel signs are marks, not letters).
    kept = (ch for ch in ascii_digits(value) if unicodedata.category(ch)[0] in "LNM")
    return "".join(kept).upper()
