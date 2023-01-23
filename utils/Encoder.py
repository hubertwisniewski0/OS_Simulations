from json import JSONEncoder
from typing import Any

from .Serializable import Serializable


class Encoder(JSONEncoder):
    """
    Extends `JSONEncoder` class with support for `Serializable` type objects
    """

    def default(self, o: Any) -> Any:
        if isinstance(o, Serializable):
            return o.serialize()
        else:
            return super().default(o)
