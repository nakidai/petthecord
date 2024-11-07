from logging import getLogger

from aiohttp.web import AppRunner, TCPSite
from discord import Intents
from discord.ext import commands

from .bot import PetTheCordCog
from .petter import CachedPetter, Petter
from .server import Server


class PetTheCord(commands.AutoShardedBot):
    def __init__(
        self,

        host: str = "127.0.0.1",
        port: int = 8080,
        origin: str = "https://ptc.pwn3t.ru",
        petter: Petter | None = None,
        shard_count: int = 1,
    ) -> None:
        super().__init__(
            command_prefix="!",
            intents=Intents.default(),
            shard_count=shard_count,
        )
        self._host = host
        self._port = port
        self._origin = origin
        self._petter = petter or Petter()

        self._logger = getLogger(__name__)

        self._petter.prepare(self)

    async def on_ready(self) -> None:
        await self.add_cog(PetTheCordCog(self._origin))
        await self.tree.sync()

        runner = AppRunner(Server(self._petter))
        await runner.setup()
        site = TCPSite(runner, self._host, self._port)
        await site.start()

        self._logger.info(f"Started serving on {self._host}:{self._port}")

        if isinstance(self._petter, CachedPetter):
            await self._petter.gc_loop()
