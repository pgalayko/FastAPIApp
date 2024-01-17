from fastapi import APIRouter

from models import User

# Роутеры позволяют переиспользовать префиксы, логически разделять приложение
user_router = APIRouter(prefix='/users', tags=['users'])


@user_router.get("/{user_id}")  # name - path parameter
async def get_user(user_id: int):
    return {"message": f"Hello {user_id}"}


@user_router.post("/")
async def create_user(user: User):
    return {"message": f"Hello {user.name}"}


@user_router.delete("/{user_id}")
async def delete_user(user_id: int):
    return {"message": f"Hello {user_id}"}


@user_router.put("/{user_id}")
async def update_user(user_id: int):
    return {"message": f"Hello {user_id}"}


@user_router.get("/users/")
async def get_user():
    return {"message": f"Hello"}
