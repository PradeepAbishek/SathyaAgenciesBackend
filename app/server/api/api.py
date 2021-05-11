from fastapi import APIRouter

from .router.users import router as user_router
from .router.auth import router as auth_router
from .router.customers import router as customer_router
from .router.companies import router as company_router
from .router.banks import router as bank_router
from .router.products import router as product_router
from .router.purchases import router as purchase_router
from .router.stocks import router as stock_router
from .router.bills import router as bill_router
from .router.payments import router as payment_router
from .router.returns import router as return_router


router = APIRouter()
router.include_router(auth_router, tags=["Authentication"], prefix="/token")
router.include_router(user_router, tags=["User"], prefix="/users")
router.include_router(customer_router, tags=["Customer"], prefix="/customers")
router.include_router(company_router, tags=["Company"], prefix="/companies")
router.include_router(bank_router, tags=["Bank"], prefix="/banks")
router.include_router(product_router, tags=["Product"], prefix="/products")
router.include_router(purchase_router, tags=[
                      "Purchase"], prefix="/purchases")
router.include_router(stock_router, tags=["Stock"], prefix="/stocks")
router.include_router(bill_router, tags=["Bill"], prefix="/bills")
router.include_router(payment_router, tags=["Payments"], prefix="/payments")
router.include_router(return_router, tags=["Returns"], prefix="/returns")
