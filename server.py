from fastapi import FastAPI, Path, Query, Depends, HTTPException, status
from typing import Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from passlib.hash import bcrypt
import jwt

app = FastAPI()

JWT_SECRET = "$ecretH@shP@ssw0rdTest"

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(128, null=False)
    email = fields.CharField(max_length=50, unique=True)
    is_active = fields.BooleanField(default=True)
    is_superuser = fields.BooleanField(default=False)

    @classmethod
    async def get_user(cls, username):
        return cls.get(username=username)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password)

User_Pydantic = pydantic_model_creator(User, name="User")
UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)

oath2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def authenticate_user(username: str, password: str):
    user = await User.get(username=username)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user

@app.post("/sign-in")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    user_obj = await User_Pydantic.from_tortoise_orm(user)

    token = jwt.encode(user_obj.dict(), JWT_SECRET)

    return {"access_token": token, "token_type": "bearer"}

@app.post("/create-user", response_model=User_Pydantic)
async def create_user(user: UserIn_Pydantic):
    user_obj = User(username=user.username, email=user.email, password=bcrypt.hash(user.password))
    await user_obj.save()
    return await User_Pydantic.from_tortoise_orm(user_obj)

async def get_current_user(token: str = Depends(oath2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = await User.get(id=payload.get("id"))
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    return await User_Pydantic.from_tortoise_orm(user)

@app.post("/user-details", response_model=User_Pydantic)
async def home(user: User_Pydantic = Depends(get_current_user)):
    return user

@app.post("/home")
async def home(user: User_Pydantic = Depends(get_current_user)):
    return {"message": "Welcome to home page"}

register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["server"]},
    generate_schemas=True,
    add_exception_handlers=True
)