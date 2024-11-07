from asyncio import sleep
from json import load, dump
from logging import getLogger
from os import PathLike, makedirs, remove, listdir
from os.path import getmtime
from pathlib import Path
from time import time
from typing import NoReturn

from discord import User

from ..defaults import Defaults
from .exceptions import CacheEnvironmentFail, NotFound
from .petter import Petter


class CachedPetter(Petter):
    def __init__(
        self,

        path: str | PathLike = Defaults.Cache.PATH,
        lifetime: int = Defaults.Cache.LIFETIME,
        gc_delay: int = Defaults.Cache.GC_DELAY,
    ) -> None:
        super().__init__()

        self._path = Path(path).resolve()
        self._lifetime = lifetime
        self._gc_delay = gc_delay

        self._logger = getLogger(__name__)

        index_path = self._path / "index.json"
        try:
            if not index_path.exists():
                self._logger.warning("`index.json` doesn't exist, trying to create...")
                if not self._path.exists():
                    self._logger.warning("Cache folder doesnt exist, trying to create...")
                    makedirs(self._path, mode=0o755, exist_ok=True)
                with open(index_path, "w") as f:
                    f.write("{}")
        except OSError:
            self._logger.error("Cannot create environment")
            raise CacheEnvironmentFail

        with open(index_path, "r") as f:
            self._cache = load(f)

    async def petpet(self, user: int | User) -> bytes:
        if isinstance(user, int):
            _user = await self._get_user(user)
        else:
            _user = user
        if not _user.avatar:
            raise NotFound

        avatar_path = self._path / f"{_user.id}_{_user.avatar.key}.gif"
        if (path := self._cache.get(_user.id)) != str(avatar_path):
            self._logger.debug(f"Generating new cached gif for {_user.id}")
            if path:
                try:
                    remove(path)
                except OSError:
                    self._logger.warning("no {path} was found when replacing avatar")
            self._cache[_user.id] = str(avatar_path)
            with open(self._path / "index.json", "w") as f:
                dump(self._cache, f)

        if not avatar_path.exists():
            with open(avatar_path, "wb") as f:
                f.write(await super().petpet(user))

        avatar_path.touch()

        with open(avatar_path, "rb") as f:
            return f.read()

    async def gc_loop(self) -> NoReturn:
        while True:
            self._logger.info("Starting new cache's gc iteration")

            for filename in listdir(self._path):
                path = (self._path / filename)
                if path.is_file() and filename != "index.json":
                    if (time() - getmtime(path) > self._lifetime):
                        self._logger.debug(f"Removing {filename}")
                        to_delete = filename.split('_')[0]
                        try:
                            del self._cache[to_delete]
                        except KeyError:
                            self._logger.warning(f"{to_delete} has been already removed from the index")
                        remove(path)
            with open(self._path / "index.json", "w") as f:
                dump(self._cache, f)

            self._logger.debug("Finished collecting old cache")

            await sleep(self._gc_delay)
