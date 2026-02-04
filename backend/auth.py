

import jwt
import datetime
import os
from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from tinydb import TinyDB, Query
from config import logger

router = APIRouter(prefix="/api/auth", tags=["Authentication"])
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET", "VIT_PROJECT_SUPER_SECRET_2026")
ALGORITHM = "HS256"

db = TinyDB('users.json')
UserTable = Query()

class UserSignup(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

# Helper to create token
def create_access_token(username: str):
    payload = {
        "sub": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        "iat": datetime.datetime.utcnow()
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

@router.post("/signup")
async def signup(user: UserSignup):
    if db.search(UserTable.username == user.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_password = pwd_context.hash(user.password)
    db.insert({
        "username": user.username,
        "email": user.email,
        "password": hashed_password
    })
    
    logger.info(f"👤 New User Registered: {user.username}")
    return {"message": "User created successfully", "username": user.username}

@router.post("/login")
async def login(user: UserLogin):
    result = db.search(UserTable.username == user.username)
    if not result:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    db_user = result[0]
    if not pwd_context.verify(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Generate the JWT
    token = create_access_token(db_user["username"])
    
    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "username": db_user["username"],
            "email": db_user["email"]
        }
    }