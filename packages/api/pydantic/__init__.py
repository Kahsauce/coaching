from typing import Any

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


def Field(default: Any, **kwargs) -> Any:
    return default
