from typing import Any
from json import JSONEncoder
from .Serializable import Serializable


class Encoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, Serializable):
            return o.serialize()
        else:
            return super().default(o)
