from typing import Any, Iterator, Optional, Tuple

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
        self.__iterable = iterable

    def count(self, value: Any) -> int:
        return self.__iterable.count(value)
        
    def index(self, value: Any, start: Optional[int] = None, stop: Optional[int] = None) -> int:
        return self.__iterable.index(value, start, stop)

    def __getitem__(self, index: int) -> Any:
        return self.__iterable.__getitem__(index)

    def __len__(self) -> int:
        return self.__iterable.__len__()

    def __iter__(self) -> Iterator[Any]:
        return self.__iterable.__iter__()

    def __next__(self) -> Any:
        return next(self.__iterable)

    def __str__(self) -> str:
        return self.__iterable.__str__()

    def __repr__(self) -> str:
        return self.__iterable.__str__()
