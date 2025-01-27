from app.configuration.routes.routes import Routes
from app.core.routes import base, orders, suppliers, warehouse_inventory

__routes__ = Routes(
    routers=(
        base.router,
        orders.router,
        suppliers.router,
        warehouse_inventory.router))
