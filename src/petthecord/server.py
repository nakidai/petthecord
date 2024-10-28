from logging import getLogger
from typing import NoReturn

from aiohttp.web import Application, StreamResponse, get, HTTPFound, Request, Response

from .cache import CachedPet, HTTPException, NotFound


class Server(Application):
    def __init__(self, petter: CachedPet) -> None:
        self._petter = petter
        super().__init__()

        self._logger = getLogger(__name__)

        self.add_routes(
            [
                get("/{uid}", self.petpet),
                get("/", self.root)
            ]
        )

    async def root(self, _: Request) -> NoReturn:
        raise HTTPFound("https://github.com/nakidai/petthecord")

    async def petpet(self, request: Request) -> StreamResponse:
        try:
            uid = int(request.match_info["uid"][:request.match_info["uid"].find('.')])
        except ValueError:
            return Response(status=400)

        self._logger.info(f"Petting {uid} for {request.remote}")

        try:
            return Response(body=await self._petter.petpet(uid), content_type="image/gif")
        except NotFound:
            return Response(status=404)
        except HTTPException:
            return Response(status=403)
