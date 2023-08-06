from typing import Iterator, List

from .base import BaseAPIModel


__all__ = ['Doodle', 'Doodles']


class Doodle:
    """Wrapper class for doodle data

    Attributes
    ----------
    district : str
        the district the doodle is in

    playground : str
        the playground the doodle is in

    dna : str
        the doodle's DNA string

    rendition : str
        a link to a 256x256 png of the doodle's rendition

    traits : List[str]
        the list of the doodle's traits

    cost : int
        how much the doodle costs to purchase
    """

    __slots__ = ['district', 'playground', 'dna', 'rendition', 'traits', 'cost']

    def __init__(self, district, playground, *, dna, traits, cost) -> None:
        self.district: str = district
        self.playground: str = playground
        self.dna: str = dna
        self.rendition: str = f'https://rendition.toontownrewritten.com/render/{dna}/doodle/256x256.png'
        self.traits: List[str] = traits
        self.cost: int = cost


class Doodles(BaseAPIModel):
    """Wrapper class for the /doodles response
    
    A tuple-like class containing `Doodle` objects, sorted by district and playground
    """
    def __init__(self, **payload) -> None:
        iterable: tuple[Doodle] = tuple(
            sorted([
                Doodle(district, playground, **doodle)
                for district, playgrounds in payload.items()
                for playground, doodles in playgrounds.items()
                for doodle in doodles
            ], key = lambda doodle: (doodle.district, doodle.playground))
        )

        super().__init__(iterable)

    def __getitem__(self, index: int) -> Doodle:
        return self._iterable.__getitem__(index)

    def __iter__(self) -> Iterator[Doodle]:
        return self._iterable.__iter__()

    def __next__(self) -> Doodle:
        return next(self._iterable)
