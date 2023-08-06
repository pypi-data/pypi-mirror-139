from __future__ import annotations

from typing import Union


class Chat:
    def __init__(self, data: Union[str, dict]):
        if isinstance(data, str):
            self.data = {"text": data}
        else:
            self.data = data

    def __eq__(self, other: Chat) -> bool:
        return self.data == other.data
