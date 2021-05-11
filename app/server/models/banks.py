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


class Bank(BaseModel):
    companyId: str
    bankName: str
    accountNumber: str
    ifscCode: str
    branchName: str
    createdBy: str


class BankInUpdate(BaseModel):
    companyId: str
    bankName: str
    accountNumber: str
    ifscCode: str
    branchName: str


class BankInResponse(IDModel):
    companyId: str
    bankName: str
    accountNumber: str
    ifscCode: str
    branchName: str
    companyDetails: pCompany
    createdBy: str


class BankInDB(IDModel, Bank):
    pass
