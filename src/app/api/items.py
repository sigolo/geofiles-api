import os
from typing import List

from ..db import items as items_repository
from .schemas import Item, PublicItem
from fastapi import APIRouter, HTTPException, status, Security, Depends

router = APIRouter()

@router.post("/", response_model=PublicItem, status_code=status.HTTP_201_CREATED)
async def create_item(payload: Item):
    item_id = await items_repository.create(payload)
    item = await items_repository.get_one(item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Problem occured during item creation")
    return item


@router.get("/{id}", response_model=PublicItem, status_code=status.HTTP_200_OK)
async def get_item(id: int):
    item = await items_repository.get_one(id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The item with id {id} was not found")
    return item

