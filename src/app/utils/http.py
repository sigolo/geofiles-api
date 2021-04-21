import uuid
import httpx
from fastapi import status, Request
from .singleton import SingletonMeta
from ..utils.Exceptions import raise_404_exception
from .logs import RestLogger
from .env import REQUEST_ID_KEY, ACCESS_TOKEN_KEY, CREDENTIALS_URL


class HTTPFactory(metaclass=SingletonMeta):
    def __init__(self):
        self._request_id = None

    @classmethod
    def set_request_id(cls, request: Request):
        request_id = str(uuid.uuid4()) if REQUEST_ID_KEY not in request.headers else request.headers[REQUEST_ID_KEY]
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
        if not request.headers.get(ACCESS_TOKEN_KEY):
            return None, None
        token = request.headers[ACCESS_TOKEN_KEY]
        async with httpx.AsyncClient() as client:
            try:
                result = await client.post(url=CREDENTIALS_URL, headers={ACCESS_TOKEN_KEY: token,
                                                                         REQUEST_ID_KEY: self.request_id})
                if result.status_code == status.HTTP_200_OK:
                    return result.json(), result.headers[ACCESS_TOKEN_KEY]
                return None, None
            except httpx.ConnectError as e:
                print(e)
                raise_404_exception("Users Service Unavailable")
