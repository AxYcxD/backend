import aiosqlite
import uuid

DB_FILE = "bots.db"

async def init_db():
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT,
                password TEXT,
                verified INTEGER,
                otp TEXT,
                token TEXT
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS bots (
                id TEXT PRIMARY KEY,
                owner_id TEXT,
                name TEXT,
                status TEXT
            )
        ''')
        await db.commit()

async def create_user(data):
    id = str(uuid.uuid4())
    token = str(uuid.uuid4())
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute("INSERT INTO users (id, email, password, verified, otp, token) VALUES (?, ?, ?, ?, ?, ?)",
                         (id, data["email"], data["password"], 0, "123456", token))
        await db.commit()
    return {"msg": "OTP sent to email"}

async def verify_user(data):
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute("SELECT * FROM users WHERE email=? AND otp=?", (data["email"], data["otp"])) as cursor:
            user = await cursor.fetchone()
        if user:
            await db.execute("UPDATE users SET verified=1 WHERE email=?", (data["email"],))
            await db.commit()
            return {"msg": "Verified"}
    raise Exception("Invalid OTP")

async def login_user(data):
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute("SELECT token FROM users WHERE email=? AND password=? AND verified=1",
                              (data["email"], data["password"])) as cursor:
            user = await cursor.fetchone()
        if user:
            return {"token": user[0]}
    raise Exception("Invalid credentials")

async def get_user_by_token(token):
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute("SELECT id, email FROM users WHERE token=?", (token,)) as cursor:
            user = await cursor.fetchone()
        if user:
            return {"id": user[0], "email": user[1]}
    raise Exception("Invalid token")