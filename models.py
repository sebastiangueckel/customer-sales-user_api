from datetime import date
from pydantic import BaseModel
from typing import Optional

class CustomerCreate(BaseModel):
    customerkey: int
    givenname: Optional[str] = None
    surname: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    age: Optional[int] = None
    occupation: Optional[str] = None

class AuftragCreate(BaseModel):
    orderkey: int
    linenumber: int
    orderdate: Optional[date] = None
    deliverydate: Optional[date] = None
    customerkey: Optional[int] = None
    quantity: Optional[int] = None
    unitprice: Optional[float] = None
    netprice: Optional[float] = None
    unitcost: Optional[float] = None

class Geo(BaseModel):
    lat: str
    lng: str

class Address(BaseModel):
    street: str
    suite: str
    city: str
    zipcode: str
    geo: Geo

class ExternalBenutzer(BaseModel):
    id: int
    name: int
    username: str
    email: str
    phone: str
    website: str
    address: Address

