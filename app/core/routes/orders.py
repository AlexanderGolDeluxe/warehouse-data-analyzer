from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import API_PREFIX
from app.configuration.db_helper import db_helper
from app.core.crud.orders import get_most_popular_orders_by_qty
from app.core.schemas import DefaultAPIResponse
from app.core.schemas.order import most_popular_orders_response_example

router = APIRouter(prefix=API_PREFIX + "/orders", tags=["Orders"])


@router.get(
    "/most-popular", responses=most_popular_orders_response_example
)
async def get_most_popular_orders(
        from_order_date: str | None = None,
        to_order_date: str | None = None,
        limit: int | None = Query(10, ge=1),
        session: AsyncSession = Depends(db_helper.get_scoped_session)
    ):
    return DefaultAPIResponse(
        message="Most popular orders finded successfully",
        data=await get_most_popular_orders_by_qty(
            session=session,
            from_order_date=from_order_date,
            to_order_date=to_order_date,
            limit=limit))
