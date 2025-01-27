# Project warehouse-data-analyzer
This is a test task with REST API for processing and analysis warehouse data.
Developed on the [FastAPI](https://fastapi.tiangolo.com) framework.

![Static Badge](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=blue&labelColor=white)
![Static Badge](https://img.shields.io/badge/FastAPI-0.115.7-009485?logo=fastapi&labelColor=white)
![Static Badge](https://img.shields.io/badge/RabbitMQ-white?logo=rabbitmq)
![Static Badge](https://img.shields.io/badge/PyTest-8.3.4-009FE3?logo=pytest&labelColor=white)

## Installation

### Clone repository
```console
git clone https://github.com/AlexanderGolDeluxe/warehouse-data-analyzer.git
```

### Make a virtual environment with requirements

```console
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Manage environment variables

Rename file [`.env.dist`](/.env.dist) to `.env`
```console
mv .env.dist .env
```

#### Change variables according to your required parameters in `.env` file

Set your RabbitMQ variables
```
…
### RABBITMQ SETTINGS ###
RMQ_USER = "guest"
RMQ_PASSWORD = "*****"
RMQ_HOST = "localhost"
RMQ_PORT = 5672
…
```

## Launch

```console
uvicorn app:create_app --reload
```

## Testing

For settings use file [`pyproject.toml`](/pyproject.toml)
```console
pytest -v tests/
```

## Build via Docker compose

1. [Clone repository](#clone-repository)
2. [Rename file `.env.dist` to `.env`](#manage-environment-variables)
3. [Change variables according to your required parameters in `.env` file](#change-variables-according-to-your-required-parameters-in-env-file)
4.  Run following command in your console:
    ```console
    docker compose -f "docker-compose.yml" up -d --build
    ```

## API Request Examples
Obtaining the total costs of inventory for a specific period
```console
curl -X 'GET' \
  'http://localhost/api/v1/warehouse-inventory/total-expenses?from_order_date=01.01.2024&to_order_date=31.12.2024' \
  -H 'accept: application/json'
```
Getting the most popular products by order volume for the quarter (top 10)
```console
curl -X 'GET' \
  'http://localhost/api/v1/orders/most-popular?from_order_date=01.10.2024&to_order_date=31.12.2024&limit=10' \
  -H 'accept: application/json'
```
Getting the suppliers with the highest number of orders (top 5)
```console
curl -X 'GET' \
  'http://localhost/api/v1/suppliers/top-by-orders?limit=5' \
  -H 'accept: application/json'
```
Adding new inventory item
```console
curl -X 'POST' \
  'http://localhost/api/v1/warehouse-inventory/add' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
        "order": "Order 1",
        "supplier": "Supplier 1",
        "customer": "Customer 1",
        "quantity": 1,
        "price": 10,
        "order_date": "25.01.2025"
      }'
```
