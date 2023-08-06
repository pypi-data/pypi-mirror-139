from typing import Any, Tuple

from ..exceptions import FailedResponse


__all__ = ['BaseAPIModel']


class BaseAPIModel:
    def __new__(cls, *args, **payload):
        instance = super().__new__(cls)

        if payload.get('error', None):
            """Sometimes the server will send an error field when there is no cached response"""
            raise FailedResponse(payload['error'])
            
        return instance

    def __init__(self, iterable: Tuple[Any]) -> None:
        self._iterable = iterable

    def __len__(self) -> int:
        return self._iterable.__len__()

    def __str__(self) -> str:
        return self._iterable.__str__()

    def __repr__(self) -> str:
        return self._iterable.__str__()
