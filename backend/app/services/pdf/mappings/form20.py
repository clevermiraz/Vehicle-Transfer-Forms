from app.services.pdf.generator import Box, FormSpec
from app.services.pdf.mappings import on_dots

FORM_20 = FormSpec(
    slug="form-20",
    title="Form 20 (Seller's declaration)",
    template="form_20.pdf",
    pages=[0],  # page 2 of the template is blank
    boxes=[
        Box("transfer.registration_authority", "Registration authority", 163, 517, on_dots(149.5)),
        Box("seller.name", "Seller name", 130, 522, on_dots(174.0)),
        Box("seller.nid", "Seller NID", 178, 301, on_dots(198.5)),
        Box("seller.tin", "Seller TIN", 371, 521, on_dots(198.5)),
        Box("seller.mother_name", "Seller mother", 99, 522, on_dots(223.1)),
        Box("seller.father_or_husband", "Seller father/husband", 123, 522, on_dots(247.6)),
        Box("seller.address", "Seller address", 72, 523, on_dots(272.1), rows=2, indent=35),
        Box("vehicle.registration_number", "Registration number", 149, 375, on_dots(345.6)),
        Box("vehicle.vehicle_type", "Vehicle type", 403, 518, on_dots(345.6)),
        Box("vehicle.chassis_number", "Chassis number", 130, 266, on_dots(370.1)),
        Box("vehicle.engine_number", "Engine number", 325, 517, on_dots(370.1)),
        Box("vehicle.manufacturer", "Manufacturer", 129, 272, on_dots(394.6)),
        Box("vehicle.manufacturing_year", "Manufacturing year", 326, 514, on_dots(394.6)),
        Box("buyer.name", "Buyer name", 105, 521, on_dots(443.7)),
        Box("buyer.father_or_husband", "Buyer father/husband", 126, 522, on_dots(468.2)),
        Box("buyer.address", "Buyer address", 72, 523, on_dots(492.7), rows=2, indent=38),
        Box("buyer.name", "Buyer name (transfer in favour of)", 159, 523, on_dots(541.6)),
        Box("transfer.sale_date", "Date", 110, 300, 688.8),
    ],
)
