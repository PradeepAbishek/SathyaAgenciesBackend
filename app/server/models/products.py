from bson.objectid import ObjectId
from .dbmodel import IDModel
from typing import Optional
from pydantic import BaseModel
from .companies import Company


class pCompany(BaseModel):
    companyName: str
    address: str
    phoneNumber: str
    gstNumber: str
    mailAddress: str
    initialBalanceAmount: float
    currentBalanceAmount: float


class Product(BaseModel):
    companyId: str
    productName: str
    gst: str
    hsnCode: str
    description: str
    isActive: Optional[bool] = True
    createdBy: str


class ProductInUpdate(BaseModel):
    companyId: str
    productName: str
    gst: str
    hsnCode: str
    description: str
    isActive: Optional[bool] = True


class ProductInResponse(IDModel):
    companyId: str
    productName: str
    gst: str
    hsnCode: str
    description: str
    companyDetails: pCompany
    createdBy: str


class ProductInDB(IDModel, Product):
    pass
