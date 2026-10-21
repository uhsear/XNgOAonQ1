from .sdk import VehicleServiceCollectionSdk
from .sdk_async import VehicleServiceCollectionSdkAsync
from .net.environment import Environment

from . import models as _models


def __getattr__(name):
    """Falls back to the lazy ``.models`` registry for any name not re-exported above."""
    try:
        return getattr(_models, name)
    except AttributeError:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from None


def __dir__():
    return sorted(set(globals()) | set(dir(_models)))
