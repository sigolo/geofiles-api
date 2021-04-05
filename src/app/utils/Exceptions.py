from typing import Optional

from fastapi import HTTPException, status


def raise_401_exception(msg: Optional[str] = "Incorrect Credentials"):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=msg,
        headers={"WWW-Authenticate": "Bearer"},
    )


def raise_404_exception(msg: Optional[str] = "Requested resource does not exist or has expired"):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=msg,
    )


def raise_422_exception(msg: Optional[str] = "Payload/file format not supported"):
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=msg,
    )


def raise_500_exception(msg: Optional[str] = "Internal Server Error"):
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=msg)
