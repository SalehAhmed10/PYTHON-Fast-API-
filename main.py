from fastapi import FastAPI, Path, Query , HTTPException, status
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None

class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None


@app.get('/')
def home():
    return {"Data": "Hell Worlds"}


@app.get('/about')
def about():
    return {"Data": "About Page"}


inventory = {
    1: {
        "name": "Milk",
        "price": 3.99,
        "brand": "Cow",
        "quantity": 1
    },
    2: {
        "name": "Bread",
        "price": 2.99,
        "brand": "Wonder",
        "quantity": 1

    }
}


# Single Parameter in the URL
# @app.get('/get-item/{item_id}')
# def get_item(item_id: int):
#     return inventory[item_id]

# Two Parameters in the URL
# @app.get('/get-item/{item_id}/{name}')
# def get_item(item_id: int, name: str):
#     return inventory[item_id]

# get-item route returns all items in the inventory
@app.get('/get-item/')
def get_items():
    return inventory


# get-item route returns the item with the specified ID
@app.get('/get-item/{item_id}')
def get_item(item_id: int = Path(description="The ID of the item you would like to view")):
    # check if inventory[item_id] exists
    if item_id in inventory:
        return inventory[item_id]
    # return {"Error": "Item ID not found"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item ID not found")




# http://127.0.0.1:8000/get-by-name?name=Milk&test=2
@app.get('/get-by-name')
def get_item(test=int, name: Optional[str] = None):
    for item_id in inventory:
        if inventory[item_id]["name"] == name:
            return inventory[item_id]
    # return {"Data": "Not Found"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item name not found")


# request body with destructuring the request body
@app.post('/create-item/{item_id}')
def create_item( item_id : int,item: Item):
    if item_id in inventory:
        # return {"Error": "Item ID already exists"}
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item ID already exists")
    inventory[item_id] = {"name": item.name, "price": item.price, "brand": item.brand}
    # return inventory[item_id]
    return inventory[item_id]


# PUT request to update an item

@app.put('update-item/{item_id}')
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        # return {"Error": "Item ID does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item ID does not exist")

    if item.name != None:
          inventory[item_id].name = item.name
    if item.price != None:
            inventory[item_id].price = item.price
    if item.brand != None:
            inventory[item_id].brand = item.brand
    return inventory[item_id]

# DELETE request to delete an item

@app.delete('/delete-item')
def delete_item(item_id: int = Query(..., description="The ID of the item to delete")):
    if item_id not in inventory:
        # return {"Error": "Item ID does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item ID does not exist")
    del inventory[item_id]
    # return {"Success": "Item deleted"}
    raise HTTPException(status_code=status.HTTP_200_OK, detail="Item deleted")