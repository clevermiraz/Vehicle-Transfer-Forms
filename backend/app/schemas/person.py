from typing import Literal

from pydantic import BaseModel, ConfigDict

from app.schemas.fields import Gender, Nid, PastDate, Phone, RequiredText, Text, Tin


class PersonBase(BaseModel):
    name: RequiredText(200)
    father_name: Text(200) = None
    mother_name: Text(200) = None
    spouse_name: Text(200) = None
    father_or_husband_pref: Literal["father", "husband"] = "father"
    guardian_name: Text(200) = None
    gender: Gender = None
    date_of_birth: PastDate = None
    nationality: Text(50) = None
    nid: Nid = None
    tin: Tin = None
    phone: Phone = None
    present_address: Text(500) = None
    permanent_address: Text(500) = None


class PersonIn(PersonBase):
    # Set when the employee picked an existing customer from search.
    id: int | None = None


class PersonOut(PersonBase):
    model_config = ConfigDict(from_attributes=True)

    id: int | None
