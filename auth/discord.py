import os
from urllib.parse import urlencode
import httpx

CLIENT_ID = os.getenv("DISCORD_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET", "")
REDIRECT_URI = os.getenv("REDIRECT_URI", "")

def discord_login_url():
    params = urlencode({
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "identify email"
    })
    return f"https://discord.com/api/oauth2/authorize?{params}"

async def exchange_code(code: str):
    token_url = "https://discord.com/api/oauth2/token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    async with httpx.AsyncClient() as client:
        res = await client.post(token_url, data=data, headers=headers)
        return res.json()