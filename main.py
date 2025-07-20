from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from auth.mailer import send_otp
from auth.discord import discord_login_url, exchange_code
from db import init_db, create_user, verify_user, login_user, get_user_by_token
from bots.controller import start_bot, stop_bot, restart_bot, upload_bot
import os

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await init_db()

@app.get("/")
def root():
    return {"status": "API running"}

@app.post("/register")
async def register_user(data: dict):
    return await create_user(data)

@app.post("/verify-otp")
async def verify(data: dict):
    return await verify_user(data)

@app.post("/login")
async def login(data: dict):
    return await login_user(data)

@app.get("/me")
async def me(token: str):
    return await get_user_by_token(token)

@app.get("/auth/discord")
def discord_auth():
    return {"url": discord_login_url()}

@app.get("/auth/discord/callback")
async def discord_callback(code: str):
    return await exchange_code(code)

@app.post("/bots/upload")
async def upload(data: dict):
    return await upload_bot(data)

@app.post("/bots/start")
async def start(data: dict):
    return await start_bot(data)

@app.post("/bots/stop")
async def stop(data: dict):
    return await stop_bot(data)

@app.post("/bots/restart")
async def restart(data: dict):
    return await restart_bot(data)