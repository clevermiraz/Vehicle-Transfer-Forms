"""Turn transfer data into the flat canonical values the form mappings refer to.

Input has the same shape as SAMPLE_DATA.json:
    {"seller": {...}, "buyer": {...}, "vehicle": {...}, "transfer": {..., "witnesses": [...]}}

Output keys look like "seller.name", "vehicle.chassis_number", "witnesses.1.details".
All formatting decisions (upper case, date format, money) live here, not in the mappings.
"""

from datetime import date
from typing import Any

from app.services.money import amount_in_words, format_taka


def _text(value: Any) -> str:
    if value is None:
        return ""
    return " ".join(str(value).split()).upper()


def _date(value: Any) -> str:
    if not value:
        return ""
    if isinstance(value, str):
        value = date.fromisoformat(value)
    return value.strftime("%d/%m/%Y")


def _person(prefix: str, p: dict) -> dict[str, str]:
    father_or_husband = p.get("spouse_name") if p.get("father_or_husband_pref") == "husband" else p.get("father_name")
    values = {
        "name": p.get("name"),
        "father_name": p.get("father_name"),
        "mother_name": p.get("mother_name"),
        "spouse_name": p.get("spouse_name"),
        "father_or_husband": father_or_husband,
        "guardian_name": p.get("guardian_name"),
        "gender": p.get("gender"),
        "nationality": p.get("nationality"),
        "nid": p.get("nid"),
        "tin": p.get("tin"),
        "phone": p.get("phone"),
        # Forms 20/21/22 have a single address line: present address (decision #4).
        "address": p.get("present_address"),
        "present_address": p.get("present_address"),
        "permanent_address": p.get("permanent_address"),
    }
    out = {f"{prefix}.{k}": _text(v) for k, v in values.items()}
    out[f"{prefix}.date_of_birth"] = _date(p.get("date_of_birth"))
    return out


def _sale_price(t: dict) -> str:
    price = t.get("sale_price")
    if not price:
        return ""
    words = t.get("sale_price_words") or amount_in_words(int(price))
    return f"{format_taka(int(price))} ({words})"


def _witness(w: dict) -> str:
    parts = [_text(w.get("name")), _text(w.get("address"))]
    if w.get("phone"):
        parts.append(f"MOBILE: {w['phone']}")
    return ", ".join(p for p in parts if p)


def build_context(data: dict) -> dict[str, str]:
    t = data["transfer"]
    ctx = {**_person("seller", data["seller"]), **_person("buyer", data["buyer"])}
    ctx.update({f"vehicle.{k}": _text(v) for k, v in data["vehicle"].items()})
    ctx.update(
        {
            "transfer.registration_authority": _text(t.get("registration_authority")),
            "transfer.sale_price_text": _sale_price(t),
            "transfer.sale_date": _date(t.get("sale_date")),
            "transfer.fee_bank_name": _text(t.get("fee_bank_name")),
        }
    )
    for w in t.get("witnesses") or []:
        ctx[f"witnesses.{w['position']}.details"] = _witness(w)
    return ctx
