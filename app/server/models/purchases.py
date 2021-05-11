from datetime import date
from .dbmodel import IDModel
from pydantic import BaseModel
from typing import List
from typing import Optional


class pCompany(BaseModel):
    companyName: str
    address: str
    phoneNumber: str
    gstNumber: str
    mailAddress: str
    initialBalanceAmount: float
    currentBalanceAmount: float


class PurchaseDetails(BaseModel):
    productName: str
    productGST: str
    productQuantity: int
    unitPrice: float
    sellingPrice: list
    gstAmount: float
    cgstAmount: Optional[float] = 0
    sgstAmount: Optional[float] = 0
    igstAmount: Optional[float] = 0
    productPrice: float
    productTotalPrice: float
    productHSNCode: str


class PurchaseMaster(BaseModel):
    companyId: str
    purchaseDate: str
    isIGSTBill: bool
    totalProductCount: str
    totalGSTAmount: float
    totalProductAmount: float
    totalPurchaseAmount: float
    freighCharge: Optional[float] = 0
    description: Optional[str]
    purchaseDetails: List[PurchaseDetails]
    paymentMode: str
    paidPurchaseAmount: float
    balancePurchaseAmount: float
    otherAmount: Optional[float] = 0
    createdBy: str


class PurchaseMasterInResponse(IDModel, PurchaseMaster):
    companyDetails: pCompany
