from pprint import pprint

from httpx import AsyncClient

from app.config import API_PREFIX


async def test_get_top_suppliers_by_orders(ac: AsyncClient):
    response = await ac.get(
        API_PREFIX + "/suppliers/top-by-orders", params=dict(limit=10))

    response_json = response.json()
    pprint(response_json)
    assert len(response_json["data"]["top_supplier_by_orders"]) <= 10
    assert response.status_code == 200


async def test_get_top_suppliers_by_orders_with_invalid_limit(
        ac: AsyncClient
    ):
    response = await ac.get(
        API_PREFIX + "/suppliers/top-by-orders", params=dict(limit=0))

    pprint(response.json())
    assert response.status_code == 422


async def test_route_not_found(ac: AsyncClient):
    response = await ac.get(API_PREFIX + "/supplier")

    pprint(response.json())
    assert response.status_code == 404
