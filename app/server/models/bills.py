from datetime import date
from .dbmodel import IDModel
from pydantic import BaseModel
from typing import List
from typing import Optional


class bCustomer(BaseModel):
    customerName: str
    address: str
    phoneNumber: str
    gstNumber: str
    isActive: Optional[bool] = True
    initialBalanceAmount: float
    currentBalanceAmount: float
    aadharNumber: str


class BillDetails(BaseModel):
    stockId: str
    productName: str
    productGST: str
    productHSNCode: str
    productQuantity: int
    productPurchasePrice: float
    productUnitPrice: float
    productPrice: float
    productProfit: float
    gstAmount: float
    cgstAmount: Optional[float] = 0
    sgstAmount: Optional[float] = 0
    igstAmount: Optional[float] = 0
    productTotalPrice: float


class BillMaster(BaseModel):
    customerId: str
    billDate: str
    isIGSTBill: bool
    totalProductCount: str
    totalGSTAmount: float
    totalProductAmount: float
    totalBillAmount: float
    totalProfit: float
    freighCharge: Optional[float] = 0
    description: Optional[str]
    paymentMode: str
    paidBillAmount: float
    balanceBillAmount: float
    billDetails: List[BillDetails]
    financialYear: Optional[int]
    billNumber: Optional[int]
    createdBy: str


class BillMasterInResponse(IDModel, BillMaster):
    customerDetails: bCustomer


class Filter(BaseModel):
    startDate: str
    endDate: str
