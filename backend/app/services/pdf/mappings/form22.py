from app.services.pdf.generator import Box, FormSpec
from app.services.pdf.mappings import on_dots

# Witness slots: signature is handwritten right after "১।/২।/৩।"; printed details start at x=180.
_WITNESS = dict(rows=2, pitch=11, size=9, min_size=6.5)

FORM_22 = FormSpec(
    slug="form-22",
    title="Form 22 (Sale receipt)",
    template="form_22.pdf",
    boxes=[
        Box("seller.name", "Seller name", 130, 522, on_dots(134.7)),
        Box("seller.nid", "Seller NID", 178, 297, on_dots(159.3)),
        Box("seller.tin", "Seller TIN", 371, 522, on_dots(159.3)),
        Box("seller.mother_name", "Seller mother", 99, 522, on_dots(183.7)),
        Box("seller.father_or_husband", "Seller father/husband", 123, 522, on_dots(208.2)),
        Box("seller.address", "Seller address", 72, 523, on_dots(232.7), rows=3, indent=35),
        Box("vehicle.registration_number", "Registration number", 152, 372, on_dots(330.8)),
        Box("vehicle.vehicle_type", "Vehicle type", 399, 518, on_dots(330.8)),
        Box("vehicle.chassis_number", "Chassis number", 130, 273, on_dots(355.2)),
        Box("vehicle.engine_number", "Engine number", 329, 517, on_dots(355.2)),
        Box("vehicle.manufacturer", "Manufacturer", 129, 276, on_dots(379.9)),
        Box("vehicle.manufacturing_year", "Manufacturing year", 326, 518, on_dots(379.9)),
        Box("buyer.name", "Buyer name", 105, 521, on_dots(404.3)),
        Box("buyer.father_or_husband", "Buyer father/husband", 126, 522, on_dots(428.8)),
        Box("buyer.address", "Buyer address", 72, 523, on_dots(453.3), rows=2, indent=38),
        Box("transfer.sale_price_text", "Sale price", 119, 521, on_dots(502.4)),
        Box("transfer.sale_date", "Date", 110, 300, 596.8),
        # Revenue stamp box is at x 395-457, y 647-705: witnesses 1-2 stay left of it.
        Box("witnesses.1.details", "Witness 1", 180, 390, 662.3, **_WITNESS),
        Box("witnesses.2.details", "Witness 2", 180, 390, 699.6, **_WITNESS),
        Box("witnesses.3.details", "Witness 3", 180, 525, 735.8, **_WITNESS),
    ],
)
