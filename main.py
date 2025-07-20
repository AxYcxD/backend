from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from db import (
    init_db,
    create_user,
    verify_user,
    login_user,
    get_user_by_token,
)

from routes.auth import router as auth_router
from routes.bot import router as bot_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield  # Cleanup can be done after this line if needed

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can limit this to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(bot_router, prefix="/bot", tags=["bot"])

@app.get("/")
async def root():
    return {"message": "Bot Manager Backend is running."}
