from io import BytesIO
from logging import getLogger

import discord
from discord import Client, User
from petpetgif import petpet

from .exceptions import HTTPException, NotFound


class Petter:
    _client: Client

    def __init__(self) -> None:
        self._logger = getLogger(__name__)

    def prepare(self, client: Client) -> None:
        self._client = client

    async def _get_user(self, uid: int) -> User:
        try:
            user = await self._client.fetch_user(uid)
            return user
        except discord.NotFound:
            raise NotFound
        except discord.HTTPException:
            raise HTTPException

    async def _get_avatar(self, user: User) -> bytes:
        if not user.avatar:
            raise NotFound
        return await user.avatar.read()

    async def petpet(self, user: int | User) -> bytes:
        if isinstance(user, int):
            _user = await self._get_user(user)
        else:
            _user = user

        self._logger.debug(f"Generating gif for {_user.id}")

        with BytesIO() as f:
            petpet.make(BytesIO(await self._get_avatar(_user)), f)
            f.seek(0)
            return f.read()
