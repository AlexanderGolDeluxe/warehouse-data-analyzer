from pprint import pprint

from httpx import AsyncClient

from app.config import API_PREFIX


async def test_get_most_popular_orders(ac: AsyncClient):
    response = await ac.get(
        API_PREFIX + "/orders/most-popular",
        params=dict(
            from_order_date="01.01.2024",
            to_order_date="31.01.2025",
            limit=100))

    pprint(response.json())
    assert response.status_code == 200


async def test_most_popular_orders_with_invalid_date(ac: AsyncClient):
    response = await ac.get(
        API_PREFIX + "/orders/most-popular",
        params=dict(
            from_order_date="2024",
            to_order_date="2025",
            limit=100))

    pprint(response.json())
    assert response.status_code == 422


async def test_most_popular_orders_with_invalid_limit(ac: AsyncClient):
    response = await ac.get(
        API_PREFIX + "/orders/most-popular", params=dict(limit=0))

    pprint(response.json())
    assert response.status_code == 422


async def test_index_redirect(ac: AsyncClient):
    response = await ac.get("/")

    assert response.status_code == 307
