import os
import uuid

import httpx
from fastapi import status, Request

from .singleton import SingletonMeta
from ..utils.Exceptions import raise_404_exception
from .logs import RestLogger

CREDENTIALS_URL = os.getenv("CREDENTIALS_URL")


class HTTPFactory(metaclass=SingletonMeta):
    def __init__(self):
        self._request_id = None

    @classmethod
    def set_request_id(cls, request: Request):
        request_id = str(uuid.uuid4()) if "X-Request-ID" not in request.headers else request.headers["X-Request-ID"]
        RestLogger.instance.request_id = request_id
        cls.instance.request_id = request_id
        return request_id

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

    async def check_user_credentials(self, request: Request):
        if not request.headers.get("access-token"):
            print("1")
            return None, None
        token = request.headers["access-token"]
        async with httpx.AsyncClient() as client:
            try:
                result = await client.post(url=CREDENTIALS_URL, headers={"access-token": token,
                                                                         "X-Request-ID": self.request_id})
                if result.status_code == status.HTTP_200_OK:
                    print("2")
                    return result.json(), result.headers["access-token"]
                return None, None
            except httpx.ConnectError as e:
                print(e)
                raise_404_exception("Users Service Unavailable")
