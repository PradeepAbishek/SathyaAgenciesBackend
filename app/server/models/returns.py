from datetime import date
from .dbmodel import IDModel
from pydantic import BaseModel
from typing import List
from typing import Optional


class rPayment(BaseModel):
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


class rCustomer(BaseModel):
    customerName: str
    address: str
    phoneNumber: str
    gstNumber: str
    isActive: Optional[bool] = True
    initialBalanceAmount: float
    currentBalanceAmount: float
    aadharNumber: str


class ReturnDetails(BaseModel):
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
    cgstAmount: float
    sgstAmount: float
    productTotalPrice: float
    purchasedProductQuantity: int


class ReturnMaster(BaseModel):
    returnNumber: Optional[int]
    billNumber: str
    customerId: str
    returnDate: str
    isIGSTBill: bool
    totalProductCount: str
    totalGSTAmount: float
    totalProductAmount: float
    totalReturnAmount: float
    totalProfit: float
    returnDetails: List[ReturnDetails]
    financialYear: Optional[int]
    createdBy: str


class ReturnMasterInResponse(IDModel, ReturnMaster):
    customerDetails: rCustomer


class ReturnMasterInResponseWithPayment(IDModel, ReturnMaster):
    customerDetails: rCustomer
    paymentDetails: rPayment