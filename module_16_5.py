from fastapi import FastAPI, status, Body, HTTPException, Request, Form, Path
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Annotated
from fastapi.templating import Jinja2Templates

app = FastAPI()
users = []


class User(BaseModel):
    id: int
    username: str
    age: int


users.append(User(id=1, username="Qwerascal", age=24))
users.append(User(id=2, username="Deremy", age=25))
users.append(User(id=3, username="ZloyChel", age=100))
templates = Jinja2Templates(directory='templates')


@app.get('/')
async def get_all_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get('/users/{user_id}')
async def get_all_users(request: Request, user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example='1')]) -> HTMLResponse:
    try:
        return templates.TemplateResponse("users.html", {"request": request, "user": users[user_id]})
    except IndexError:
        raise HTTPException(status_code=404, detail='Message not found')


@app.post('/user/{username}/{age}')
async def create_users(username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='Xdkilza')],
                       age: Annotated[int, Path(ge=18, le=120, description='Enter age', example='18')]) -> User:
    user_id = 1
    if users:
        user_id = users[-1].id + 1
    user = User(id=user_id, username=username, age=age)
    users.append(user)
    return user


@app.put('/user/{user_id}/{username}/{age}')
async def update_users(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example='1')],
                       username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='Xdkilza')],
                       age: Annotated[int, Path(ge=18, le=120, description='Enter age', example='18')]):
    try:
        for user in users:
            if user.id == user_id:
                user.username, user.age = username, age
                return user
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')


@app.delete('/user/{user_id}')
async def delete_user(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example='1')]):
    try:
        for user in users:
            if user_id == user.id:
                users.remove(user)
                return user
    except IndexError:
        raise HTTPException(status_code=404, detail='Message not found')
