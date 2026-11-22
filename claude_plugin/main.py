from itertools import count

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    name: str = Field(min_length=1)
    description: str | None = None
    price: float = Field(gt=0)


class Item(ItemCreate):
    id: int


class Message(BaseModel):
    detail: str


app = FastAPI(title="Items API")

items_db: dict[int, Item] = {}
_id_counter = count(1)


@app.get("/items", response_model=list[Item])
def list_items() -> list[Item]:
    return list(items_db.values())


@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate) -> Item:
    item = Item(id=next(_id_counter), **payload.model_dump())
    items_db[item.id] = item
    return item


@app.get(
    "/items/{item_id}",
    response_model=Item,
    responses={404: {"model": Message, "description": "Item not found"}},
)
def get_item(item_id: int) -> Item:
    item = items_db.get(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item
