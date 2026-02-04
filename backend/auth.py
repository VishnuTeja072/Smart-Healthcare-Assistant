import jwt
import datetime
import os
import sqlite3
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from config import logger

# =========================
# ROUTER CONFIG
# =========================
router = APIRouter(prefix="/api/auth", tags=["Authentication"])
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# =========================
# JWT CONFIG
# =========================
SECRET_KEY = os.getenv("JWT_SECRET", "VIT_PROJECT_SUPER_SECRET_2026")
ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 24

# =========================
# DATABASE (SQLITE)
# =========================
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")
conn.commit()

# =========================
# SCHEMAS
# =========================
class UserSignup(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

# =========================
# JWT HELPERS
# =========================
def create_access_token(username: str):
    payload = {
        "sub": username,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=TOKEN_EXPIRE_HOURS)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized: No token provided")

    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Session expired. Please login again.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")

# =========================
# AUTH ENDPOINTS
# =========================
@router.post("/signup")
async def signup(user: UserSignup):
    hashed_password = pwd_context.hash(user.password)

    try:
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (user.username, user.email, hashed_password)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    logger.info(f"👤 New User Registered: {user.username}")
    return {
        "message": "User created successfully",
        "username": user.username
    }

@router.post("/login")
async def login(user: UserLogin):
    cursor.execute(
        "SELECT username, email, password FROM users WHERE username = ?",
        (user.username,)
    )
    db_user = cursor.fetchone()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    username, email, hashed_password = db_user

    if not pwd_context.verify(user.password, hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(username)

    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "username": username,
            "email": email
        }
    }
