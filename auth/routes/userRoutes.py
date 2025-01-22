from fastapi import APIRouter, HTTPException, Depends
from config.database import user_collection
from schemas.user_schema import user_list_serialiser, user_serialiser
from models.user import User
from bson import ObjectId
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from middleware.auth import JWTBearer

load_dotenv()
userRouter = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 90


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@userRouter.get("/", dependencies=[Depends(JWTBearer())])
async def get_users():
    users = user_collection.find()
    return user_list_serialiser(users)


@userRouter.post("/signup")
async def signup(user: User):
    existing_user = user_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    user.password = get_password_hash(user.password)
    inserted = user_collection.insert_one(dict(user))
    new_user = user_collection.find_one({"_id": ObjectId(inserted.inserted_id)})
    return user_serialiser(new_user)


@userRouter.post("/login")
async def login(user: User):
    existing_user = user_collection.find_one({"email": user.email})
    if not existing_user or not verify_password(
        user.password, existing_user["password"]
    ):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token_expires = timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    token = create_token(
        data={"sub": existing_user["email"]}, expires_delta=token_expires
    )
    return {"token": token}
