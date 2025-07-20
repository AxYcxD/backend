from fastapi import APIRouter, Request, Depends, UploadFile, File
import os
from utils import run_bot, stop_bot, restart_bot, get_user_by_token

router = APIRouter()

@router.post("/upload")
async def upload_bot_file(
    token: str,
    file: UploadFile = File(...)
):
    user = await get_user_by_token(token)
    if not user:
        return {"error": "Invalid token"}

    save_path = f"bots/{user['id']}"
    os.makedirs(save_path, exist_ok=True)
    contents = await file.read()

    with open(os.path.join(save_path, file.filename), "wb") as f:
        f.write(contents)

    return {"status": "uploaded"}

@router.post("/start")
async def start_bot(request: Request):
    data = await request.json()
    return await run_bot(data)

@router.post("/stop")
async def stop_bot(request: Request):
    data = await request.json()
    return await stop_bot(data)

@router.post("/restart")
async def restart_bot(request: Request):
    data = await request.json()
    return await restart_bot(data)