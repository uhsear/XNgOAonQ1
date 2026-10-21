# Vehicle Service App

A small Python CLI application that implements the **Vehicle Service API** using the
SDK generated from the `Vehicle Service Collection` Postman collection.

The SDK lives in this repo at:
`postman/sdks/Collections SDKs/Vehicle Service Collection/python`

## Endpoints

| Command                 | HTTP                     | SDK method            |
| ----------------------- | ------------------------ | --------------------- |
| `list`                  | `GET /vehicles`          | `get_all_vehicles`    |
| `get <id>`              | `GET /vehicles/{id}`     | `retrieve_a_vehicle`  |
| `create ...`            | `POST /vehicles`         | `create_a_vehicle`    |
| `update <id> ...`       | `PATCH /vehicles/{id}`   | `update_a_collection` |
| `delete <id>`           | `DELETE /vehicles/{id}`  | `delete_a_vehicle`    |

## Setup

From the `app/` directory:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

This installs the local SDK (editable) plus `python-dotenv`.

## Configuration

Copy `.env.example` to `.env` and adjust as needed:

```bash
cp .env.example .env
```

| Variable                   | Default                  | Description                          |
| -------------------------- | ------------------------ | ------------------------------------ |
| `VEHICLE_SERVICE_BASE_URL` | `http://localhost:4501`  | Base URL of the Vehicle Service API  |
| `VEHICLE_SERVICE_API_KEY`  | _(empty)_                | API key sent via `X-API-Key` header  |
| `VEHICLE_SERVICE_TIMEOUT`  | `30`                     | Request timeout in seconds           |

The default base URL matches the `baseUrl` Postman environment variable, which
points at the local Vehicle Service mock.

## Usage

```bash
# List all vehicles
python vehicle_service_app.py list

# Retrieve a single vehicle
python vehicle_service_app.py get 1

# Create a vehicle
python vehicle_service_app.py create \
  --nick-name "The Lisa Marie" \
  --vin 4M2DV11W4RDJ53329 \
  --make Mercury --model Villager \
  --year 1994 --miles 159864

# Update a vehicle (only pass the fields you want to change)
python vehicle_service_app.py update 1 --miles 160000

# Delete a vehicle
python vehicle_service_app.py delete 1
```
