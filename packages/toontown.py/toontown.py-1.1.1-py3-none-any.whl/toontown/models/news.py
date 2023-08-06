import re
from datetime import datetime
from typing import Iterator, Optional

from .base import BaseAPIModel


__all__ = ['News', 'NewsList']


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


class News:
    """Wrapper class for the news data
    
    Attributes
    ----------
    post_id : int
        the ID of the post

    title : str
        the title of the post

    author : str
        who wrote the post

    body_raw : str
        the raw body of the post containing HTML elements

    body : str
        a readable version of the body, with HTML elements stripped out

    date : datetime
        when the post was written

    image : str
        a link to the image of the post
    """

    __slots__ = ['post_id', 'title', 'author', 'body_raw', 'body', 'date', 'image']

    def __init__(self, **props) -> None:
        self.post_id: int = props.get('postId')
        self.title: str = props.get('title')
        self.author: str = props.get('author')
        self.date: datetime = datetime.strptime(props.get('date'), DATE_FMT)
        self.image: str = props.get('image')

        body_raw = props.get('body', None)
        self.body_raw: Optional[str] = body_raw
        self.body: Optional[str] = clean(body_raw)


class NewsList(BaseAPIModel):
    """Wrapper class for the /news response
    
    A tuple-like class containing `News` objects
    """
    def __init__(self, **payload) -> None:
        iterable = tuple(payload.get('iterable'))
        super().__init__(iterable)

    def __getitem__(self, index: int) -> News:
        return self._iterable.__getitem__(index)

    def __iter__(self) -> Iterator[News]:
        return self._iterable.__iter__()

    def __next__(self) -> News:
        return next(self._iterable)
