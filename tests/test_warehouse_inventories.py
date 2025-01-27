from pprint import pprint

from httpx import AsyncClient

from app.config import API_PREFIX
from tests.conftest import test_orders


async def test_create_warehouse_inventory(ac: AsyncClient):
    for test_order in test_orders:
        response = await ac.post(
            API_PREFIX + "/warehouse-inventory/create", json=test_order)

        pprint(response.json())
        assert response.status_code == 201


async def test_add_warehouse_inventory_short_name(ac: AsyncClient):
    local_test_orders = test_orders.copy()
    for test_order in local_test_orders:
        test_order["order"] = test_order.get("order", "A")[:1]
        response = await ac.post(
            API_PREFIX + "/warehouse-inventory/add", json=test_order)

        pprint(response.json())
        assert response.status_code == 422


async def test_add_warehouse_inventory_invalid_qty(ac: AsyncClient):
    local_test_orders = test_orders.copy()
    for test_order in local_test_orders:
        test_order["quantity"] = 1.1
        response = await ac.post(
            API_PREFIX + "/warehouse-inventory/add", json=test_order)

        pprint(response.json())
        assert response.status_code == 422


async def test_add_warehouse_inventory_invalid_price(ac: AsyncClient):
    local_test_orders = test_orders.copy()
    for test_order in local_test_orders:
        test_order["price"] = "USD"
        response = await ac.post(
            API_PREFIX + "/warehouse-inventory/add", json=test_order)

        pprint(response.json())
        assert response.status_code == 422


async def test_add_warehouse_inventory_invalid_order_date(
        ac: AsyncClient
    ):
    local_test_orders = test_orders.copy()
    for test_order in local_test_orders:
        test_order["order_date"] = test_order.get("order_date", "1")[:2]
        response = await ac.post(
            API_PREFIX + "/warehouse-inventory/add", json=test_order)

        pprint(response.json())
        assert response.status_code == 422


async def test_add_warehouse_inventory_empty_json_data(ac: AsyncClient):
    response = await ac.post(
        API_PREFIX + "/warehouse-inventory/add", json=dict())

    pprint(response.json())
    assert response.status_code == 422
