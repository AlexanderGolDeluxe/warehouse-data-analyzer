from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import API_PREFIX
from app.configuration.db_helper import db_helper
from app.core.crud.suppliers import find_top_supplier_by_orders
from app.core.schemas import DefaultAPIResponse
from app.core.schemas.supplier import (
    top_suppliers_by_orders_response_example)

router = APIRouter(prefix=API_PREFIX + "/suppliers", tags=["Suppliers"])


@router.get(
    "/top-by-orders", responses=top_suppliers_by_orders_response_example
)
async def get_top_suppliers_by_orders(
        limit: int | None = Query(5, ge=1),
        session: AsyncSession = Depends(db_helper.get_scoped_session)
    ):
    return DefaultAPIResponse(
        message="Top suppliers by orders finded successfully",
        data=await find_top_supplier_by_orders(
            session=session, limit=limit))
