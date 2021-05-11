from .dbmodel import IDModel
from pydantic import BaseModel


class sCompany(BaseModel):
    companyName: str
    address: str
    phoneNumber: str
    gstNumber: str
    mailAddress: str
    initialBalanceAmount: float
    currentBalanceAmount: float

class Stock(BaseModel):
    companyId: str
    productName: str
    productHSNCode: str
    productGST: str
    unitPrice: float
    sellingPrice: list
    availableQuantity: int


class StockInResponse(IDModel, Stock):
    pass


class StockZeroResponse(IDModel, Stock):
    companyDetails: sCompany
