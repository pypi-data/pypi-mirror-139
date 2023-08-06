import re
from datetime import datetime
from typing import Iterator, Optional

from .base import BaseAPIModel


__all__ = ['ReleaseNotes', 'ReleaseNotesList']


DATE_FMT = '%B %-d, %Y at %-I:%M %p'

cleaner = re.compile(r'(<.*?>|\r)')
encode_cleaner = re.compile(r'&nbsp;')
newline_cleaner = re.compile(r'\n{2,}')


def clean(string: Optional[str]):
    if string is None:
        return string

    string = cleaner.sub('', string)
    string = encode_cleaner.sub(' ', string)
    string = newline_cleaner.sub('\n\n', string)

    return string


class ReleaseNotes:
    """Wrapper class for the release note data
    
    Attributes
    ----------
    note_id : int
        the ID of the post
        
    slug : str
        the slug of the post

    date : datetime
        when the post was written

    body_raw : str
        the raw body of the post containing HTML elements

    body : str
        a readable version of the body, with HTML elements stripped out
    """

    __slots__ = ['note_id', 'slug', 'date', 'body_raw', 'body']

    def __init__(self, **props) -> None:
        self.note_id: int = props.get('noteId')
        self.slug: str = props.get('slug')
        self.date: datetime = datetime.strptime(props.get('date'), DATE_FMT)

        body_raw = props.get('body', None)
        self.body_raw: Optional[str] = body_raw
        self.body: Optional[str] = clean(body_raw)


class ReleaseNotesList(BaseAPIModel):
    """Wrapper class for the /releasenotes response
    
    A tuple-like class containing `ReleaseNote` objects
    """
    def __init__(self, **payload) -> None:
        iterable: tuple[ReleaseNotes] = tuple(payload.get('iterable'))
        super().__init__(iterable)

    def __getitem__(self, index: int) -> ReleaseNotes:
        return self._iterable.__getitem__(index)

    def __iter__(self) -> Iterator[ReleaseNotes]:
        return self._iterable.__iter__()

    def __next__(self) -> ReleaseNotes:
        return next(self._iterable)
