from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI(
    title="PC Components Catalog API",
    description="REST API для управління каталогом комплектуючих ПК",
    version="1.0.0"
)

class ItemBase(BaseModel):
    name: str = Field(..., example="AMD Ryzen 5 5600X")
    category: str = Field(..., example="CPU")
    price: float = Field(..., gt=0, example=149.99)
    stock: int = Field(..., ge=0, example=12)
    description: Optional[str] = Field(None, example="6 ядер, 12 потоків, 3.7-4.6 ГГц")

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

# In-memory сховище
items_db: dict[int, Item] = {
    1: Item(id=1, name="AMD Ryzen 5 5600X", category="CPU", price=149.99, stock=12, description="6 ядер, 12 потоків"),
    2: Item(id=2, name="NVIDIA GeForce RTX 4060", category="GPU", price=299.99, stock=5, description="8GB GDDR6"),
}
current_id_counter = 2

@app.get("/api/items", response_model=List[Item], status_code=status.HTTP_200_OK)
def get_all_items():
    return list(items_db.values())

@app.get("/api/items/{id}", response_model=Item, status_code=status.HTTP_200_OK)
def get_item_by_id(id: int):
    if id not in items_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Товар не знайдено")
    return items_db[id]

@app.post("/api/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate):
    global current_id_counter
    current_id_counter += 1
    new_item = Item(id=current_id_counter, **item.model_dump())
    items_db[current_id_counter] = new_item
    return new_item

@app.put("/api/items/{id}", response_model=Item, status_code=status.HTTP_200_OK)
def update_item(id: int, item: ItemCreate):
    if id not in items_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Товар не знайдено")
    updated_item = Item(id=id, **item.model_dump())
    items_db[id] = updated_item
    return updated_item

@app.delete("/api/items/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(id: int):
    if id not in items_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Товар не знайдено")
    del items_db[id]
    return None

# check artifact upload
