"""Mini implémentation de Pydantic pour les tests hors ligne."""

from typing import Any, Dict, Tuple, Type

from .version import VERSION

class BaseModel:
    def __init__(self, **data: Any):
        ann = getattr(self, '__annotations__', {})
        for field in ann:
            if field in data:
                setattr(self, field, data[field])
            else:
                setattr(self, field, getattr(self.__class__, field, None))

    def dict(self):
        return self.__dict__


class BaseSettings(BaseModel):
    """Placeholder de ``BaseSettings`` compatible avec Pydantic."""

    pass


class AnyUrl(str):
    """Type de chaîne représentant une URL quelconque."""

    pass


class HttpUrl(AnyUrl):
    """Alias simple pour ``AnyUrl``."""

    pass


AnyHttpUrl = HttpUrl


def Field(default: Any, **kwargs) -> Any:
    return default


def create_model(name: str, **fields: Tuple[type, Any]) -> Type[BaseModel]:
    """Create a simple Pydantic-like model.

    Parameters
    ----------
    name: str
        Name of the generated class.
    fields: mapping of field names to a ``(type, default)`` tuple.

    Returns
    -------
    Type[BaseModel]
        Newly created model class inheriting from ``BaseModel``.
    """
    annotations: Dict[str, type] = {}
    namespace: Dict[str, Any] = {}
    for field_name, value in fields.items():
        if isinstance(value, tuple) and len(value) == 2:
            field_type, default = value
        else:
            field_type, default = value, None
        annotations[field_name] = field_type
        namespace[field_name] = default
    namespace["__annotations__"] = annotations
    return type(name, (BaseModel,), namespace)
