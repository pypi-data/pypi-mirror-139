from dataclasses import dataclass
from datetime import datetime
from typing import Iterator

from .base import BaseAPIModel


__all__ = ['Population', 'District']


@dataclass
class District:
    """Wrapper class for district data
    
    Attributes
    ----------
    name : str
        the name of the district
        
    population : int
        the population of the district
        
    last_updated : datetime
        when the district's population was last updated by the server
    """
    name: str
    population: int
    last_updated: datetime


class Population(BaseAPIModel):
    """"Wrapper class for /population response

    A tuple-like class containing `District` objects, sorted by population

    Attributes
    ----------
    total : int
        the total population of Toontown Rewritten

    last_updated : datetime
        the time of the last population update
    """

    __slots__ = ['total', 'last_updated']

    def __init__(self, **payload) -> None:
        self.total: int = payload.get('totalPopulation')
        self.last_updated = last_updated = datetime.fromtimestamp(payload.get('lastUpdated'))

        iterable = tuple(sorted([
            District(name, population, last_updated)
            for name, population in payload.get('populationByDistrict').items()
        ], key=lambda district: district.population))
        
        super().__init__(iterable)

    def __getitem__(self, index: int) -> District:
        return self._iterable.__getitem__(index)

    def __iter__(self) -> Iterator[District]:
        return self._iterable.__iter__()

    def __next__(self) -> District:
        return next(self._iterable)
