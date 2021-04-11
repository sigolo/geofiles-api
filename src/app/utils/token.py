import os

import httpx
from fastapi import status
from .Exceptions import raise_404_exception


async def check_user_credentials(token: str):
    URL = os.getenv("CREDENTIALS_URL")
    async with httpx.AsyncClient() as client:
        try:
            result = await client.post(url=URL, headers={"access-token": token})
            if result.status_code == status.HTTP_200_OK:
                return result.json()
            return False
        except httpx.ConnectError as e:
            print(e)
            raise_404_exception("Oauth Service Unavailable")