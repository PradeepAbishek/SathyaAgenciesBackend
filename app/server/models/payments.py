from bson.objectid import ObjectId
from .dbmodel import IDModel
from typing import Optional, List
from pydantic import BaseModel


class pCustomer(BaseModel):
    customerName: str
    address: str
    phoneNumber: str
    gstNumber: str
    currentBalanceAmount: float
    isDealer: bool = False
    aadharNumber: str


class pCompany(BaseModel):
    companyName: str
    address: str
    phoneNumber: str
    gstNumber: str
    mailAddress: str
    currentBalanceAmount: float


class Payment(BaseModel):
    paymentFor: Optional[str] = "Customer"
    customerId: str
    paymentDate: str
    paidAmount: float
    balanceAmountAfterPayment: float
    balanceAmountBeforePayment: float
    paymentMode: str
    paymentNumber: Optional[int]
    financialYear: Optional[int]
    createdBy: str
    reference: str
    returnId: Optional[str] = ""


class PaymentCompany(BaseModel):
    paymentFor: Optional[str] = "Company"
    companyId: str
    paymentDate: str
    paidAmount: float
    balanceAmountAfterPayment: float
    balanceAmountBeforePayment: float
    paymentMode: str
    paymentNumber: Optional[int]
    financialYear: Optional[int]
    createdBy: str
    reference: str


class PaymentInResponse(IDModel, Payment):
    customerDetails: pCustomer


class PaymentInResponseCompany(IDModel, PaymentCompany):
    companyDetails: pCompany


class PaymentInDB(IDModel, Payment):
    pass


class PaymentInDBCompany(IDModel, PaymentCompany):
    pass
