from fastapi import FastAPI, APIRouter
from typing import List
from db import database
import models

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


user_router = APIRouter()
item_router = APIRouter()


@user_router.post("/users/", response_model=models.User)
async def create_user(user: models.UserIn):
    query = models.users.insert().values(name=user.name, email=user.email)
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}


@user_router.get("/users/", response_model=List[models.User])
async def read_users():
    query = models.users.select()
    return await database.fetch_all(query)


@user_router.get("/users/{user_id}", response_model=models.User)
async def read_user(user_id: int):
    query = models.users.select().where(models.users.c.id == user_id)
    return await database.fetch_one(query)


@user_router.put("/users/{user_id}", response_model=models.User)
async def update_user(user_id: int, new_user: models.UserIn):
    query = (
        models.users.update()
        .where(models.users.c.id == user_id)
        .values(**new_user.dict())
    )
    await database.execute(query)
    return {**new_user.dict(), "id": user_id}


@user_router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = models.users.delete().where(models.users.c.id == user_id)
    await database.execute(query)
    return {"message": "User deleted"}


@item_router.post("/items/", response_model=models.Item)
async def create_item(item: models.ItemIn):
    query = models.items.insert().values(
        name=item.name,
        price=item.price,
        description=item.description,
        tax=item.tax,
    )
    last_record_id = await database.execute(query)
    return {**item.dict(), "id": last_record_id}


@item_router.get("/items/", response_model=List[models.Item])
async def read_items():
    query = models.items.select()
    return await database.fetch_all(query)


@item_router.get("/items/{item_id}", response_model=models.Item)
async def read_item(item_id: int):
    query = models.items.select().where(models.items.c.id == item_id)
    return await database.fetch_one(query)


app.include_router(user_router, prefix="/api/users")
app.include_router(item_router, prefix="/api/items")


@app.get("/")
def home():
    return {"message": "Добро пожаловать в интернет-магазин!"}
