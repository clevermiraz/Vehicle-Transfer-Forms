from datetime import date, datetime
from typing import Annotated

from pydantic import BaseModel, Field, model_validator

from app.schemas.fields import Phone, RequiredText, Text
from app.schemas.person import PersonIn, PersonOut
from app.schemas.vehicle import VehicleIn, VehicleOut


class WitnessIn(BaseModel):
    name: RequiredText(200)
    address: Text(500) = None
    phone: Phone = None


class WitnessOut(WitnessIn):
    position: int


class TransferBase(BaseModel):
    registration_authority: Text(200) = None
    sale_price: Annotated[int | None, Field(gt=0, le=100_000_000_000)] = None
    sale_price_words: Text(300) = None
    sale_date: date
    fee_bank_name: Text(200) = None
    notes: Text(2000) = None


class TransferIn(TransferBase):
    seller: PersonIn
    buyer: PersonIn
    vehicle: VehicleIn
    witnesses: Annotated[list[WitnessIn], Field(max_length=3)] = []

    @model_validator(mode="after")
    def _different_people(self) -> "TransferIn":
        same_record = self.seller.id is not None and self.seller.id == self.buyer.id
        same_nid = self.seller.nid is not None and self.seller.nid == self.buyer.nid
        if same_record or same_nid:
            raise ValueError("Seller and buyer cannot be the same person")
        return self


class TransferOut(TransferBase):
    id: int
    seller: PersonOut
    buyer: PersonOut
    vehicle: VehicleOut
    witnesses: list[WitnessOut]
    created_at: datetime
    updated_at: datetime
    created_by: str | None
    updated_by: str | None


class TransferListItem(BaseModel):
    id: int
    registration_number: str
    seller_name: str
    buyer_name: str
    sale_date: date
    created_at: datetime


class TransferDefaults(BaseModel):
    registration_authority: str | None
    fee_bank_name: str | None


class DocumentInfo(BaseModel):
    slug: str
    title: str
    error: str | None = None  # set when a value does not fit on the form
