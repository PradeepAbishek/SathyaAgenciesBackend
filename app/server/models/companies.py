from bson.objectid import ObjectId
from .dbmodel import IDModel
from typing import Optional
from typing import List
from pydantic import BaseModel
from .payments import PaymentInDBCompany
from .purchases import PurchaseMaster


class Company(BaseModel):
    companyName: str
    address: str
    phoneNumber: str
    gstNumber: str
    mailAddress: str
    initialBalanceAmount: float
    currentBalanceAmount: float
    purchases: list
    payments: list
    createdBy: str


class CompanyInUpdate(BaseModel):
    companyName: str
    address: str
    phoneNumber: str
    gstNumber: str
    mailAddress: str
    initialBalanceAmount: float


class CompanyInResponse(IDModel):
    companyName: str
    address: str
    phoneNumber: str
    gstNumber: str
    mailAddress: str
    initialBalanceAmount: float
    currentBalanceAmount: float
    purchases: List[PurchaseMaster]
    payments: List[PaymentInDBCompany]
    createdBy: str


class PurchaseUpdate(BaseModel):
    purchaseId: str
    balancePurchaseAmount: float


class PaymentUpdate(BaseModel):
    paymentId: str
    paidAmount: float


class CompanyInDB(IDModel, Company):
    pass
