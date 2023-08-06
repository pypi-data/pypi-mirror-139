"""
The MIT License (MIT)

Copyright (c) 2022-present jaczerob

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from abc import ABC, abstractmethod
from multiprocessing.pool import ThreadPool
from pathlib import Path
from typing import (
    Any,
    Optional,
    Union
)
import asyncio
import bz2
import hashlib
import logging
import os
import platform
import sys
import time

import aiohttp
import requests
import requests.exceptions

from .exceptions import *


logger = logging.getLogger(__name__)


Session = Union[aiohttp.ClientSession, requests.Session]

BASE = 'https://www.toontownrewritten.com/api'
BASE_HEADERS = {
    'Content-Type': 'application/json',
    'User-Agent': 'toontown.py (https://github.com/jaczerob/toontown.py)'
}

LOGIN_HEADERS = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'toontown.py (https://github.com/jaczerob/toontown.py)'
}

MANIFEST = 'https://cdn.toontownrewritten.com/content/patchmanifest.txt'
PATCHES = 'https://download.toontownrewritten.com/patches'

CHUNK_SIZE = 10 * 10 * 1024


def get_platform():
    if sys.platform == 'win32' and platform.machine().endswith('64'):
        return 'win64' # for handling 64 bit files in the patch manifest
    return sys.platform


class Route:
    def __init__(self, method: str, path: str, **parameters: Any) -> None:
        self.method = method
        self.path = path
        self.parameters = parameters
        self.url = BASE + path

    @property
    def headers(self) -> dict[str, Any]:
        return LOGIN_HEADERS if self.path == '/login' else BASE_HEADERS


class BaseHTTPClient(ABC):
    @abstractmethod
    def __init__(self, *, session: Optional[Session] = None) -> None:
        self._session = session

    @abstractmethod
    def connect(self) -> None: ...

    @abstractmethod
    def close(self) -> None: ...

    @abstractmethod
    def request(self, route: Route) -> Any: ...

    @abstractmethod
    def update(self, path: Union[str, Path]) -> None: ...

    def get_outdated_files(self, manifest: dict[str, Any], path: Path) -> list[Tuple[str, Path]]:
        pf = get_platform()

        return [
            ('{0}/{1}'.format(PATCHES, props['dl']), (path / file))
            for file, props in manifest.items()
            if pf not in props['only'] and\
            (
                not (path / file).exists() or\
                props['hash'] != hashlib.sha1((path / file).open('rb').read()).hexdigest()
            )
        ]


class SyncHTTPClient(BaseHTTPClient):
    def __init__(self, *, session: Optional[requests.Session] = None) -> None:
        self._session: requests.Session = session
        self._is_closed = True

    @property
    def is_closed(self) -> bool:
        return self._is_closed

    @is_closed.setter
    def is_closed(self, value: bool) -> None:
        self._is_closed = bool(value)

    def connect(self) -> None:
        if self._session is None:
            self._session = requests.Session()
            
        self._is_closed = False

    def close(self) -> None:
        self._session.close()
        self._is_closed = True

    def request(self, route: Route) -> Any:
        if self.is_closed:
            raise SessionNotConnected

        method = route.method
        url = route.url
        headers = route.headers
        params = route.parameters

        for tries in range(5):
            try:
                logger.info('Attempting {0} request #{1}: {2}'.format(method, tries+1, url))

                with self._session.request(method, url, params=params, headers=headers) as response:
                    response.raise_for_status()

                    data = response.json()
                    status = response.status_code

                    if 300 > status >= 200:
                        return data

                    if status in {500, 502, 504}:
                        time.sleep(1 + tries * 2)
                        continue

            except requests.exceptions.HTTPError as e:
                message = str(e)
                exc_info = type(e), e, e.__traceback__
                logger.error(message, exc_info=exc_info)

            except OSError as e:
                if tries < 4 and e.errno in {54, 10054}:
                    time.sleep(1 + tries * 2)
                    continue

                logger.info('Exhausted attempts for {0} request: {1}'.format(method, url))
                raise

    def update(self, path: Union[str, Path]) -> None:
        if isinstance(path, str):
            path = Path(path)

        if not path.is_dir():
            raise Exception('Path does not exist or is not a directory')

        manifest = self._session.get(
            MANIFEST,
            headers=BASE_HEADERS,
        ).json()

        files = self.get_outdated_files(manifest, path)

        def download(args):
            url, file_path = args
            with self._session.get(url, stream=True) as resp:
                logger.info(f'Downloading {url} to {file_path}')
                resp.raise_for_status()
                decompressor = bz2.BZ2Decompressor()

                with open(file_path, 'wb') as file:
                    for chunk in resp.iter_content(chunk_size=CHUNK_SIZE):
                        file.write(decompressor.decompress(chunk))

        with ThreadPool(os.cpu_count()) as pool:
            pool.map(download, files)


class AsyncHTTPClient(BaseHTTPClient):
    def __init__(self, *, session: Optional[aiohttp.ClientSession] = None) -> None:
        self._session: aiohttp.ClientSession = session

    async def connect(self) -> None:
        if self._session is None:
            self._session = aiohttp.ClientSession(raise_for_status=True)

    async def close(self) -> None:
        await self._session.close()

    async def request(self, route: Route) -> Any:
        if self._session.closed:
            raise SessionNotConnected

        method = route.method
        url = route.url
        headers = route.headers
        params = route.parameters

        for tries in range(5):
            try:
                logger.info('Attempting {0} request #{1}: {2}'.format(method, tries+1, url))

                async with self._session.request(method, url, params=params, headers=headers) as response:
                    data = await response.json()
                    status = response.status

                    if 300 > status >= 200:
                        return data

                    if status in {500, 502, 504}:
                        await asyncio.sleep(1 + tries * 2)
                        continue

            except aiohttp.ClientResponseError as e:
                message = str(e)
                exc_info = type(e), e, e.__traceback__
                logger.error(message, exc_info=exc_info)
                raise

            except OSError as e:
                if tries < 4 and e.errno in {54, 10054}:
                    await asyncio.sleep(1 + tries * 2)
                    continue
                raise

    async def update(self, path: Union[str, Path]) -> None:
        if isinstance(path, str):
            path = Path(path)

        if not path.is_dir():
            raise Exception('Path does not exist or is not a directory')

        manifest = await (await self._session.get(
            MANIFEST,
            headers=BASE_HEADERS,
        )).json()

        files = self.get_outdated_files(manifest, path)

        async def download(args):
            url, file_path = args

            async with self._session.get(url) as resp:
                logger.info(f'Downloading {url} to {file_path}')

                resp.raise_for_status()
                decompressor = bz2.BZ2Decompressor()

                with open(file_path, 'wb') as file:
                    async for chunk in resp.content.iter_chunked(CHUNK_SIZE):
                        file.write(decompressor.decompress(chunk))

        await asyncio.gather(*map(download, files))
