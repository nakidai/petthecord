from asyncio import sleep
from json import load, dumps
from io import BytesIO
from logging import getLogger
from os import listdir, makedirs, remove
from os.path import getmtime
from pathlib import Path
from time import time
from typing import NoReturn

from aiohttp.web import Application, StreamResponse, get, HTTPFound, Request, Response
from discord import NotFound, HTTPException
from discord.ext import commands
from petpetgif import petpet


class Server(Application):
    def __init__(
        self,

        client: commands.Bot,
        caching: bool = True,
        cache_path: str = "/var/cache/petthecord",
        cache_lifetime: int = 86400,
        cache_gc_delay: int = 14400,
    ) -> None:
        self.client = client
        self.caching = caching
        self.cache_path = Path(cache_path).resolve()
        self.cache_lifetime = cache_lifetime
        self.cache_gc_delay = cache_gc_delay
        super().__init__()

        self._logger = getLogger("petthecord.server")
        self._cache_logger = getLogger("petthecord.cache")

        if self.caching:
            index_path = self.cache_path / "index.json"
            try:
                if not index_path.exists():
                    self._cache_logger.warning("index.json doesn't exist, creating...")
                    if not self.cache_path.exists():
                        self._cache_logger.warning(f"{self.cache_path} doesn't exist, creating..")
                        makedirs(self.cache_path, mode=0o755, exist_ok=True)
                    with open(index_path, "w") as f:
                        f.write("{}")
            except OSError:
                self._cache_logger.error("Cannot create environment, turning caching off")
                self.caching = False

            with open(index_path, "r") as f:
                self.cache = load(f)

        self.add_routes(
            [
                get("/{uid}", self.petpet),
                get("/", self.root)
            ]
        )

    async def root(self, _: Request) -> NoReturn:
        raise HTTPFound("https://github.com/nakidai/petthecord")

    async def petpet(self, request: Request) -> StreamResponse:
        self._logger.info(f"Incoming '{request.rel_url}' request from {request.remote}")
        try:
            uid = int(request.match_info["uid"][:request.match_info["uid"].find('.')])
        except ValueError:
            return Response(status=400)

        try:
            user = await self.client.fetch_user(uid)
        except NotFound:
            return Response(status=404)
        except HTTPException:
            return Response(status=403)

        if user.avatar is None:
            return Response(status=404)

        avatar_path = str(self.cache_path / f"{user.id}_{user.avatar.key}.gif")
        if self.caching:
            if (path := self.cache.get(user.id)) != avatar_path:
                self._cache_logger.debug("Regenerating cached avatar {user.id}")
                if path:
                    remove(path)
                self.cache[user.id] = avatar_path
                with open(self.cache_path / "index.json", "w") as f:
                    f.write(dumps(self.cache))

            if not Path(avatar_path).exists():
                with open(avatar_path, "wb") as f:
                    image = await user.avatar.read()
                    petpet.make(BytesIO(image), f)

            Path(avatar_path).touch()

            with open(avatar_path, "rb") as f:
                return Response(body=f.read(), content_type="image/gif")
        else:
            with BytesIO() as f:
                image = await user.avatar.read()
                petpet.make(BytesIO(image), f)

                f.seek(0)

                return Response(body=f.read(), content_type="image/gif")

    async def clean_cache(self) -> None:
        while True:
            if self.caching:
                self._cache_logger.info("Starting new cache's gc iteration")

                for filename in listdir(self.cache_path):
                    path = (self.cache_path / filename)
                    if path.is_file() and filename != "index.json":
                        if (time() - getmtime(path) > self.cache_lifetime):
                            self._cache_logger.debug(f"Removing {filename}")
                            del self.cache[filename.split('_')[0]]
                            remove(path)
                with open(self.cache_path / "index.json", "w") as f:
                    f.write(dumps(self.cache))

                self._cache_logger.debug("Finished collecting old cache")

            await sleep(self.cache_gc_delay)
