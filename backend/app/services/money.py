"""Bangladeshi amount formatting: 500000 -> '5,00,000/-' and 'Five Lac'."""

_ONES = (
    "", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten",
    "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen",
)
_TENS = ("", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety")


def _below_100(n: int) -> str:
    if n < 20:
        return _ONES[n]
    tens, ones = divmod(n, 10)
    return _TENS[tens] + (f" {_ONES[ones]}" if ones else "")


def amount_in_words(amount: int) -> str:
    if amount == 0:
        return "Zero"
    crore, rest = divmod(amount, 10_000_000)
    lac, rest = divmod(rest, 100_000)
    thousand, rest = divmod(rest, 1_000)
    hundred, rest = divmod(rest, 100)
    parts = []
    if crore:
        parts.append(f"{amount_in_words(crore)} Crore")
    for value, unit in ((lac, "Lac"), (thousand, "Thousand"), (hundred, "Hundred")):
        if value:
            parts.append(f"{_below_100(value)} {unit}")
    if rest:
        parts.append(_below_100(rest))
    return " ".join(parts)


def format_taka(amount: int) -> str:
    """Indian/Bangladeshi digit grouping: 12500000 -> '1,25,00,000/-'."""
    digits = str(amount)
    head, tail = digits[:-3], digits[-3:]
    groups = []
    while len(head) > 2:
        groups.insert(0, head[-2:])
        head = head[:-2]
    if head:
        groups.insert(0, head)
    return ",".join([*groups, tail]) + "/-"
