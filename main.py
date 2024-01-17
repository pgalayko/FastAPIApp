from asyncio import sleep
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, APIRouter, Depends
from starlette.background import BackgroundTasks
from starlette.requests import Request
from starlette.responses import Response, JSONResponse, FileResponse, StreamingResponse
from starlette.websockets import WebSocket
import logging

from models import User, ResponseExample
from api.users import user_router

logger = logging.Logger(__name__)

app = FastAPI()

v1_router = APIRouter(prefix='/v1', tags=['v1'])
v2_router = APIRouter(prefix='/v2', tags=['v2'])

# Роутеры помогают группировать эндпоинты по какому-то признаку
v1_router.include_router(user_router)
v2_router.include_router(user_router)

app.include_router(user_router)


@app.get("/")  # У get запроса отсутствует тело запроса. Допустимы только query params
async def root(name: str, age: int):  # name, age - query parameters
    return {"message": f"Hello, {name}. You are {age} years old"}


# @app.post("/post")
# async def post(user: User, user2: User, age: int):  # Передаем json в теле запроса с параметрами name, age
#     return {"message": f"Hello, {user.name}, {user2.name}, you are {age} years old"}
@app.post("/post")
async def post(users: list[User] = None):  # Задавая дефолтное значение, делаем параметр необязательным
    if users is None:
        users = []
    names = [user.name for user in users]
    return {"message": f"Hello, {','.join(names)}"}


# @app.get("/{name}")  # name - path parameter
# async def get_name(name: str):
#     return {"message": f"Hello {name}"}


def generator():
    yield b"some binary data"
    yield b"another binary data"
    yield b"more binary data"


@app.get("/hello/", response_model=ResponseExample)
async def say_hello():
    response = JSONResponse(content={"message": "hello world", "message3": "hello world3"},
                            status_code=201,
                            headers={"x-Cat": "meow"})
    response.set_cookie(key="fakesession", value="fake-cookie-session-value")  # Устанавливаем cookie
    return JSONResponse(content={"message": "hello world", "message3": "hello world3"},
                        status_code=201,
                        headers={"x-Cat": "meow"})  # Передача header явным образом


@app.get("/hello2/", response_model=ResponseExample)  # Второй вариант, как можно добавить куки/заголовок
async def say_hello(response: Response):
    response.headers["X-Cat-Dog"] = "alone in the world"
    response.set_cookie(key="fakesession", value="fake-cookie-session-value")  # Устанавливаем cookie
    return {"message": "hello world", "message3": "hello world3"}


# Примеры возвращаемых классов
# JSONResponse(content={"message": "hello world", "message3": "hello world3"},
#                         status_code=201,
#                         headers={"x-Cat": "meow"})  # Передача header явным образом
# Response(content=("message": "hello world", "message3": "hello world3"))
# FileResponse("/some/path")
# StreamingResponse(generator())

# Websockets
USERS: dict[str, WebSocket] = {}


@app.websocket("/ws")
async def ws(websocket: WebSocket):
    await websocket.accept()
    name = await websocket.receive_text()
    USERS[name] = websocket
    while True:
        data = await websocket.receive_text()
        if USERS['Vasya'] == websocket:
            await USERS['Kolya'].send_text(data)
        else:
            await USERS['Vasya'].send_text(data)
# Проверить работоспособность: https://jxy.me/websocket-debug-tool/


# Dependencies
def paginate(limit: Optional[int] = 10, offset: Optional[int] = 0) -> dict:
    return {
        'limit': limit,
        'offset': offset
    }


@app.get("/clients/")
async def get_clients(pagination: dict = Depends(paginate)):
    users = [
        {
            'name': 'Nikolay',
            'is_online': True
        },
        {
            'name': 'Vasya',
            'is_online': True
        }
    ]
    return users[pagination['offset']: pagination['offset'] + pagination['limit']]


# Middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    now = datetime.now()
    response = await call_next(request)
    response.headers["X=Process-Time"] = str(datetime.now() - now)
    return response


# Events
@app.on_event("startup")
async def startup_event():
    print("startup")


@app.on_event("shutdown")
async def startup_event():
    print("shutdown")


# Background tasks
async def very_slow_function():
    await sleep(3)


@app.get("/slow-function")
async def slow_function(background_tasks: BackgroundTasks):
    background_tasks.add_task(very_slow_function)
    # await very_slow_function() при обязательной выдаче результата
    return {"message": "Hello world"}
