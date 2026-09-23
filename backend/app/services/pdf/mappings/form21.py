from app.services.pdf.generator import Box, FormSpec
from app.services.pdf.mappings import on_dots

# In Form 21 the buyer declares ("আমি/আমরা") and the seller is "জনাব".
FORM_21 = FormSpec(
    slug="form-21",
    title="Form 21 (Buyer's declaration)",
    template="form_21.pdf",
    boxes=[
        Box("transfer.registration_authority", "Registration authority", 166, 523, on_dots(148.2)),
        Box("buyer.name", "Buyer name", 130, 522, on_dots(172.7)),
        Box("buyer.nid", "Buyer NID", 178, 300, on_dots(197.2)),
        Box("buyer.tin", "Buyer TIN", 370, 524, on_dots(197.2)),
        Box("buyer.mother_name", "Buyer mother", 99, 522, on_dots(221.8)),
        Box("buyer.father_or_husband", "Buyer father/husband", 123, 522, on_dots(246.3)),
        Box("buyer.address", "Buyer address", 107, 523, on_dots(270.8)),
        Box("vehicle.registration_number", "Registration number", 148, 378, on_dots(319.7)),
        Box("vehicle.vehicle_type", "Vehicle type", 405, 524, on_dots(319.7)),
        Box("vehicle.chassis_number", "Chassis number", 130, 273, on_dots(344.3)),
        Box("vehicle.engine_number", "Engine number", 328, 524, on_dots(344.3)),
        Box("vehicle.manufacturer", "Manufacturer", 129, 275, on_dots(368.8)),
        Box("vehicle.manufacturing_year", "Manufacturing year", 325, 524, on_dots(368.8)),
        Box("seller.name", "Seller name", 105, 521, on_dots(417.8)),
        Box("seller.father_or_husband", "Seller father/husband", 126, 522, on_dots(442.4)),
        Box("seller.address", "Seller address", 72, 523, on_dots(466.9), rows=2, indent=38),
        # The dotted segment at y=515.8 before "উপরে বর্ণিত..." stays blank (decision #7).
        Box("transfer.sale_date", "Date", 115, 300, 663.0),
    ],
)
