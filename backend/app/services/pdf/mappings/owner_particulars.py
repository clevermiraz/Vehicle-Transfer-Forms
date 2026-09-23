from app.services.pdf.generator import Box, FormSpec

# Values go right of the ":" column (x=312-317). Baselines = the English label baselines.
_X0, _X1 = 322, 526
_ROW = dict(size=10, min_size=6.5, pitch=11.4)


def _row(key: str, label: str, baseline: float, rows: int = 1, x1: float = _X1) -> Box:
    return Box(key, label, _X0, x1, baseline, rows=rows, **_ROW)


# Filled for the new owner (buyer).
OWNER_PARTICULARS = FormSpec(
    slug="owner-particulars",
    title="Owner's Particulars",
    template="owner_particulars.pdf",
    boxes=[
        # Stay clear of the photo box (x>=458). A 2nd line (below the box) is free space.
        _row("buyer.name", "Name", 149.4, rows=2, x1=455),
        _row("buyer.father_name", "Father's name", 172.6),
        _row("buyer.mother_name", "Mother's name", 196.9),
        _row("buyer.spouse_name", "Husband/Wife name", 221.2),
        _row("buyer.present_address", "Present address", 245.6, rows=3),
        _row("buyer.permanent_address", "Permanent address", 281.1, rows=2),
        _row("buyer.gender", "Sex", 305.3),
        _row("buyer.phone", "Cell phone", 329.7),
        _row("buyer.nationality", "Nationality", 353.9),
        _row("buyer.date_of_birth", "Date of birth", 378.3),
        _row("buyer.nid", "NID", 402.5),
        _row("buyer.tin", "e-TIN", 426.9),
        _row("buyer.guardian_name", "Guardian's name", 451.8),
        _row("vehicle.registration_number", "Registration number", 474.9),
        _row("vehicle.engine_number", "Engine number", 511.9),
        _row("vehicle.chassis_number", "Chassis number", 536.1),
        _row("vehicle.manufacturing_year", "Year of manufacture", 560.5),
        _row("vehicle.previous_registration_number", "Previous registration", 584.7),
        _row("transfer.fee_bank_name", "Bank name", 654.2, rows=2),
    ],
)
