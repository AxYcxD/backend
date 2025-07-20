from fastapi import APIRouter, HTTPException, Request
from db import create_user, login_user

router = APIRouter()

@router.post("/register")
async def register(request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    
    if not all([username, password, email]):
        raise HTTPException(status_code=400, detail="Missing fields")

    return await create_user(username, password, email)

@router.post("/login")
async def login(request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")

    if not all([username, password]):
        raise HTTPException(status_code=400, detail="Missing fields")

    return await login_user(username, password)