import os
import uuid

import httpx
from fastapi import status

from .singleton import SingletonMeta
from ..utils.Exceptions import raise_404_exception

CREDENTIALS_URL = os.getenv("CREDENTIALS_URL")


class HTTPFactory(metaclass=SingletonMeta):
    def __init__(self):
        self._request_id = None

    @property
    def request_id(self):
        if not self._request_id:
            return None
        return str(self._request_id)

    @request_id.setter
    def request_id(self, request_id):
        try:
            self._request_id = uuid.UUID(str(request_id))
        except ValueError:
            raise ValueError("request id must be a UUID string")

    async def check_user_credentials(self, token: str):
        async with httpx.AsyncClient() as client:
            try:
                result = await client.post(url=CREDENTIALS_URL, headers={"access-token": token,
                                                                         "X-Request-ID": self.request_id})
                if result.status_code == status.HTTP_200_OK:
                    return result.json()
                return False
            except httpx.ConnectError as e:
                print(e)
                raise_404_exception("Users Service Unavailable")
