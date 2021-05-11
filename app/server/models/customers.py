from bson.objectid import ObjectId
from .dbmodel import IDModel
from typing import Optional, List
from pydantic import BaseModel
from .bills import BillMaster
from .payments import PaymentInDB


class Customer(BaseModel):
    customerName: str
    address: str
    phoneNumber: str
    gstNumber: str
    isActive: Optional[bool] = True
    initialBalanceAmount: float
    currentBalanceAmount: float
    bills: list
    payments: list
    isDealer: bool = False
    aadharNumber: str
    createdBy: str


class CustomerInUpdate(BaseModel):
    customerName: str
    address: str
    phoneNumber: str
    gstNumber: str
    isDealer: bool
    aadharNumber: str
    isActive: Optional[bool] = True


class CustomerInResponse(IDModel):
    customerName: str
    address: str
    phoneNumber: str
    gstNumber: str
    initialBalanceAmount: float
    currentBalanceAmount: float
    isDealer: bool
    bills: List[BillMaster]
    payments: List[PaymentInDB]
    aadharNumber: str
    createdBy: str


class BillUpdate(BaseModel):
    billId: str
    balanceBillAmount: float


class PaymentUpdate(BaseModel):
    paymentId: str
    paidAmount: float


class CustomerInDB(IDModel, Customer):
    pass
