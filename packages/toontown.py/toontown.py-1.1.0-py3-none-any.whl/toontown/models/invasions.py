from datetime import datetime

from .base import BaseAPIModel


__all__ = ['Invasion', 'Invasions']


class Invasion:
    """Wrapper class for invasion data
    
    Attributes
    ----------
    district : str
        the district the invasion is in

    as_of : datetime
        when the invasion started

    type : str
        the Cog type of the invasion

    progress : int
        how many cogs were defeated in this invasion

    total : int
        how many cogs that are invading

    is_mega_invasion : bool
        whether or not this is a mega invasion
    """

    __slots__ = ['district', 'as_of', 'type', 'progress', 'total', 'is_mega_invasion']

    def __init__(self, district, **payload) -> None:
        self.district: str = district
        self.as_of = datetime.fromtimestamp(payload.pop('asOf'))
        self.type: str = payload.pop('type')

        progress, total = payload.pop('progress').split('/')
        self.progress = int(progress)
        self.total = int(total)
        self.is_mega_invasion: bool = total == 1000000


class Invasions(BaseAPIModel):
    """"Wrapper class for /invasions response

    A tuple-like class containing `Invasion` objects

    Attributes
    ----------
    last_updated : datetime
        the time when the invasions were last updated
    """

    __slots__ = ['last_updated']
    
    def __init__(self, **payload) -> None:
        iterable = tuple(Invasion(**{'district': key} | item) for key, item in payload.pop('invasions').items())
        super().__init__(iterable)

        self.last_updated = datetime.fromtimestamp(payload.pop('lastUpdated'))
        