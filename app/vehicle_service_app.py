"""Vehicle Service CLI app.

A thin command-line application that implements the Vehicle Service API using
the SDK generated from the "Vehicle Service Collection" Postman collection.

Endpoints implemented:
  - list            -> GET    /vehicles          (get_all_vehicles)
  - get <id>        -> GET    /vehicles/{id}     (retrieve_a_vehicle)
  - create ...      -> POST   /vehicles          (create_a_vehicle)
  - update <id> ... -> PATCH  /vehicles/{id}     (update_a_collection)
  - delete <id>     -> DELETE /vehicles/{id}     (delete_a_vehicle)

Usage examples:
  python vehicle_service_app.py list
  python vehicle_service_app.py get 1
  python vehicle_service_app.py create --nick-name "The Lisa Marie" \\
      --vin 4M2DV11W4RDJ53329 --make Mercury --model Villager \\
      --year 1994 --miles 159864
  python vehicle_service_app.py update 1 --miles 160000
  python vehicle_service_app.py delete 1
"""

from __future__ import annotations

import argparse
import json
import sys

from config import Settings, build_client
from vehicle_service_collection_sdk import VehicleServiceCollectionSdk
from vehicle_service_collection_sdk.models import CreateAVehicleRequest
from vehicle_service_collection_sdk.net.transport.api_error import ApiError


def _print(result) -> None:
    """Pretty-print an SDK result (dict/list/str) as JSON when possible."""
    if result is None or result == "":
        print("(no content)")
        return
    try:
        print(json.dumps(result, indent=2, default=str))
    except (TypeError, ValueError):
        print(result)


def _build_vehicle_body(args) -> CreateAVehicleRequest:
    """Build a request body from CLI args, omitting values that weren't provided."""
    fields = {
        "nick_name": args.nick_name,
        "vin": args.vin,
        "make": args.make,
        "model": args.model,
        "year": args.year,
        "miles": args.miles,
    }
    provided = {k: v for k, v in fields.items() if v is not None}
    return CreateAVehicleRequest(**provided)


# --- Command handlers --------------------------------------------------------


def cmd_list(client: VehicleServiceCollectionSdk, args) -> None:
    _print(client.vehicle_service_collection_sdk.get_all_vehicles())


def cmd_get(client: VehicleServiceCollectionSdk, args) -> None:
    _print(client.vehicle_service_collection_sdk.retrieve_a_vehicle(args.id))


def cmd_create(client: VehicleServiceCollectionSdk, args) -> None:
    body = _build_vehicle_body(args)
    _print(client.vehicle_service_collection_sdk.create_a_vehicle(body))


def cmd_update(client: VehicleServiceCollectionSdk, args) -> None:
    body = _build_vehicle_body(args)
    # SDK signature: update_a_collection(request_body, id_)
    _print(client.vehicle_service_collection_sdk.update_a_collection(body, args.id))


def cmd_delete(client: VehicleServiceCollectionSdk, args) -> None:
    client.vehicle_service_collection_sdk.delete_a_vehicle(args.id)
    print(f"Deleted vehicle {args.id}")


# --- Argument parsing --------------------------------------------------------


def _add_vehicle_fields(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--nick-name", dest="nick_name", help="Vehicle nickname")
    parser.add_argument("--vin", help="Vehicle identification number")
    parser.add_argument("--make", help="Vehicle make")
    parser.add_argument("--model", help="Vehicle model")
    parser.add_argument("--year", help="Vehicle year")
    parser.add_argument("--miles", type=int, help="Vehicle mileage")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="vehicle_service_app",
        description="CLI for the Vehicle Service API (uses the generated SDK).",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list", help="List all vehicles").set_defaults(func=cmd_list)

    p_get = sub.add_parser("get", help="Retrieve a vehicle by id")
    p_get.add_argument("id", help="Vehicle id")
    p_get.set_defaults(func=cmd_get)

    p_create = sub.add_parser("create", help="Create a new vehicle")
    _add_vehicle_fields(p_create)
    p_create.set_defaults(func=cmd_create)

    p_update = sub.add_parser("update", help="Update a vehicle by id")
    p_update.add_argument("id", help="Vehicle id")
    _add_vehicle_fields(p_update)
    p_update.set_defaults(func=cmd_update)

    p_delete = sub.add_parser("delete", help="Delete a vehicle by id")
    p_delete.add_argument("id", help="Vehicle id")
    p_delete.set_defaults(func=cmd_delete)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    settings = Settings.from_env()
    client = build_client(settings)

    try:
        args.func(client, args)
    except ApiError as exc:
        status = getattr(exc, "status", None)
        print(f"API error (status {status}): {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # noqa: BLE001 - surface any failure to the user
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
