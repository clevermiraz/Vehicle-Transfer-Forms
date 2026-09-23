from datetime import date
from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict

from app.schemas.fields import RequiredText, Text


def _year(v: int | None) -> int | None:
    if v is not None and not 1950 <= v <= date.today().year + 1:
        raise ValueError("Enter a valid manufacturing year")
    return v


class VehicleBase(BaseModel):
    registration_number: RequiredText(50)
    vehicle_type: Text(100) = None
    chassis_number: Text(50) = None
    engine_number: Text(50) = None
    manufacturer: Text(100) = None
    manufacturing_year: Annotated[int | None, AfterValidator(_year)] = None
    previous_registration_number: Text(50) = None


class VehicleIn(VehicleBase):
    id: int | None = None


class VehicleOut(VehicleBase):
    model_config = ConfigDict(from_attributes=True)

    id: int | None
