from abc import abstractmethod, ABC
from pathlib import Path
from typing import Optional, Union

from .models import *
from .httpclient import BaseHTTPClient, SyncHTTPClient, AsyncHTTPClient, Route


class BaseToontownClient(ABC):
    @abstractmethod
    def __init__(self, httpclient: BaseHTTPClient) -> None:
        self.http = httpclient

    @abstractmethod
    def connect(self) -> None:
        """Connect to the HTTP client
        
        Must be called before using any other methods in this class
        """

    @abstractmethod
    def close(self) -> None:
        """Closes connection to the HTTP client"""

    @abstractmethod
    def doodles(self) -> Doodles:
        """Request Doodle data from the Toontown Rewritten API"""

    @abstractmethod
    def field_offices(self) -> FieldOffices:
        """Request Field Office data from the Toontown Rewritten API"""

    @abstractmethod
    def invasions(self) -> Invasions: 
        """Request Invasion data from the Toontown Rewritten API"""

    @abstractmethod
    def login(
        self, 
        *, 
        username: Optional[str] = None, 
        password: Optional[str] = None,
        response_token: Optional[str] = None,
        queue_token: Optional[str] = None,
    ) -> Login: 
        """Request to log into Toontown Rewritten's game server

        Must provide a username and password, a response token, or a queue token
        
        Parameters
        ----------
        username : Optional[str] = None
            optional username parameter, must also provide password if given

        password : Optional[str] = None
            optional password parameter, must also provide username if given

        response_token : Optional[str] = None
            optional response token parameter, obtained after initial login request with username and password 
            if you are required to authenticate with ToonGuard

        queue_token : Optional[str] = None
            optional queue token parameter, obtained after intial login request with username and password or 
            response token if you are required to wait in the login queue
        """

    @abstractmethod
    def population(self) -> Population: 
        """Request Population data from the Toontown Rewritten API"""

    @abstractmethod
    def silly_meter(self) -> SillyMeter: 
        """Request Silly Meter data from the Toontown Rewritten API"""

    @abstractmethod
    def news(self, *, id: Optional[int] = None, all: Optional[bool] = False) -> NewsList: 
        """Request News data from the Toontown Rewritten API"""

    @abstractmethod
    def release_notes(self, *, id: Optional[int] = None) -> ReleaseNotesList:
        """Request Release Notes data from the Toontown Rewritten API"""

    @abstractmethod
    def status(self) -> Status:
        """Request Status data from the Toontown Rewritten API"""

    @abstractmethod
    def update(self, path: Union[str, Path]) -> None:
        """Updates or creates the Toontown Rewritten files at the given Path"""


class SyncToontownClient(BaseToontownClient):
    """Synchronous client to interact with the Toontown Rewritten API"""

    def __init__(self) -> None:
        super().__init__(SyncHTTPClient())

    def connect(self) -> None:
        self.http.connect()

    def close(self) -> None:
        self.http.close()

    def status(self) -> Status:
        data = self.http.request(Route(
            'GET',
            '/status'
        ))

        return Status(**data)

    def release_notes(self, *, id: Optional[int] = None) -> ReleaseNotesList:
        if id is not None:
            path = f'/releasenotes/{id}'
        else:
            path = '/releasenotes'

        data = self.http.request(Route(
            'GET',
            path
        ))

        if not isinstance(data, list):
            data = dict(iterable=[data])
        else:
            data = dict(iterable=data)

        return ReleaseNotesList(**data)
        
    def news(self, *, id: Optional[int] = None, all: Optional[bool] = False) -> NewsList:
        if id is not None:
            path = f'/news/{id}'
        elif all is True:
            path = '/news/list'
        else:
            path = '/news'

        data = self.http.request(Route(
            'GET',
            path
        ))

        if not isinstance(data, list):
            data = dict(iterable=[data])
        else:
            data = dict(iterable=data)

        return NewsList(**data)

    def doodles(self) -> Doodles:
        data = self.http.request(Route(
            'GET',
            '/doodles'
        ))

        return Doodles(**data)

    def field_offices(self) -> FieldOffices:
        data = self.http.request(Route(
            'GET',
            '/fieldoffices'
        ))

        return FieldOffices(**data)

    def invasions(self) -> Invasions:
        data = self.http.request(Route(
            'GET',
            '/invasions'
        ))

        return Invasions(**data)

    def login(
        self, 
        *, 
        username: Optional[str] = None, 
        password: Optional[str] = None,
        app_token: Optional[str] = None,
        auth_token: Optional[str] = None,
        queue_token: Optional[str] = None,
    ) -> Login:
        params = {'format': 'json'}

        if app_token is not None and auth_token is not None:
            params['appToken'] = app_token
            params['authToken'] = auth_token
        elif queue_token is not None:
            params['queueToken'] = queue_token
        elif username is not None and password is not None:
            params['username'] = username
            params['password'] = password
        else:
            raise Exception('Please provide either a username and password, a queue token, or a auth token and app token to log in')

        data = self.http.request(Route(
            'POST',
            '/login',
            **params
        ))
        
        return Login(**data)

    def population(self) -> Population:
        data = self.http.request(Route(
            'GET',
            '/population'
        ))

        return Population(**data)

    def silly_meter(self) -> None:
        data = self.http.request(Route(
            'GET',
            '/sillymeter'
        ))

        return SillyMeter(**data)

    def update(self, path: Union[str, Path]) -> None:
        self.http.update(path)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args):
        self.close()


class AsyncToontownClient(BaseToontownClient):
    """Asynchronous client to interact with the Toontown Rewritten API"""

    def __init__(self) -> None:
        super().__init__(AsyncHTTPClient())

    async def connect(self) -> None:
        await self.http.connect()

    async def close(self) -> None:
        await self.http.close()

    async def status(self) -> Status:
        data = await self.http.request(Route(
            'GET',
            '/status'
        ))

        return Status(**data)

    async def release_notes(self, *, id: Optional[int] = None) -> ReleaseNotesList:
        if id is not None:
            path = f'/releasenotes/{id}'
        else:
            path = '/releasenotes'

        data = await self.http.request(Route(
            'GET',
            path
        ))

        if not isinstance(data, list):
            data = dict(iterable=[data])
        else:
            data = dict(iterable=data)

        return ReleaseNotesList(**data)
        
    async def news(self, *, id: Optional[int] = None, all: Optional[bool] = False) -> NewsList:
        if id is not None:
            path = f'/news/{id}'
        elif all is True:
            path = '/news/list'
        else:
            path = '/news'

        data = await self.http.request(Route(
            'GET',
            path
        ))

        if not isinstance(data, list):
            data = dict(iterable=[data])
        else:
            data = dict(iterable=data)

        return NewsList(**data)

    async def doodles(self) -> Doodles:
        data = await self.http.request(Route(
            'GET',
            '/doodles'
        ))

        return Doodles(**data)

    async def field_offices(self) -> FieldOffices:
        data = await self.http.request(Route(
            'GET',
            '/fieldoffices'
        ))

        return FieldOffices(**data)

    async def invasions(self) -> Invasions:
        data = await self.http.request(Route(
            'GET',
            '/invasions'
        ))

        return Invasions(**data)

    async def login(
        self, 
        *, 
        username: Optional[str] = None, 
        password: Optional[str] = None,
        app_token: Optional[str] = None,
        auth_token: Optional[str] = None,
        queue_token: Optional[str] = None,
    ) -> Login:
        params = {'format': 'json'}

        if app_token is not None and auth_token is not None:
            params['appToken'] = app_token
            params['authToken'] = auth_token
        elif queue_token is not None:
            params['queueToken'] = queue_token
        elif username is not None and password is not None:
            params['username'] = username
            params['password'] = password
        else:
            raise Exception('Please provide either a username and password, a queue token, or a auth token and app token to log in')

        data = await self.http.request(Route(
            'POST',
            '/login',
            **params
        ))
        
        return Login(**data)

    async def population(self) -> Population:
        data = await self.http.request(Route(
            'GET',
            '/population'
        ))

        return Population(**data)

    async def silly_meter(self) -> SillyMeter:
        data = await self.http.request(Route(
            'GET',
            '/sillymeter'
        ))

        return SillyMeter(**data)

    async def update(self, path: Union[str, Path]) -> None:
        await self.http.update(path)

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, *args):
        await self.close()
