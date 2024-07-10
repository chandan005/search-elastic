from typing import Optional
from pydantic import BaseModel

class ABN(BaseModel):
    status: str
    statusFromDate: str
    value: str

class EntityType(BaseModel):
    type: str
    value: str

class NonIndividualName(BaseModel):
    type: str
    value: str

class AddressDetails(BaseModel):
    state: str
    postCode: str

class BusinessAddress(BaseModel):
    addressDetails: AddressDetails

class MainEntity(BaseModel):
    nonIndividualName: NonIndividualName
    businessAddress: BusinessAddress

class ASIC(BaseModel):
    type: str
    value: str

class GST(BaseModel):
    status: str
    statusFromDate: str

class OtherEntity(BaseModel):
    nonIndividualName: NonIndividualName

class Record(BaseModel):
    abn: ABN
    entityType: EntityType
    mainEntity: MainEntity
    asic: ASIC
    gst: GST
    otherEntity: OtherEntity
