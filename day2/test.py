from datetime import timedelta, datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, Response, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt  # PyJWT 사용
from argon2 import PasswordHasher  # argon2 사용
from sqlmodel import Session, select
from dotenv import load_dotenv
import os

from models.users import UserDB, UserCreate, UserResponse
from database.connection import create_tables, get_db
from models.users import Menu, MenuCreate, MenuResponse

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# 비밀번호 해싱 및 검증을 위한 설정 (argon2 사용)
ph = PasswordHasher()

security = HTTPBearer()

def get_current_user(
        token: HTTPAuthorizationCredentials = Security(security), 
        session: Session = Depends(get_db)):
    
    try:
        if token is None:
            raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")

        # PyJWT로 JWT 디코딩
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        
        user = session.exec(select(UserDB).where(UserDB.user_id == user_id)).first()    
        if user is None:
            raise HTTPException(status_code=401, detail="유저를 찾을 수 없습니다.")
        return user
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield

app = FastAPI(lifespan=lifespan)

def create_access_token(
    data: dict, 
    expires_delta: timedelta | None = None):

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    # PyJWT로 JWT 생성
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/signup")
def signup(
    user: UserCreate, 
    session: Session = Depends(get_db)):

    db_user = session.exec(select(UserDB).where(UserDB.user_id == user.user_id)).first()
    if db_user:
        raise HTTPException(status_code=409, detail="User already registered")
    
    # 비밀번호 해싱 (argon2 사용)
    hashed_password = ph.hash(user.user_pw)
    new_user = UserDB(
        user_id=user.user_id, user_pw=hashed_password, is_admin=user.is_admin
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return Response(status_code=200, content="add user")

@app.post("/login")
def login(
    user_id: str, 
    user_pw: str, 
    session: Session = Depends(get_db)):

    db_user = session.exec(select(UserDB).where(UserDB.user_id == user_id)).first()
    if not db_user or not ph.verify(db_user.user_pw, user_pw):  # argon2 검증
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.user_id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}



class TimeStamp(SQLModel):
    id: int = Field(default=None, primary_key=True)  # DB ID (Primary Key)
    created_at: datetime = Field(default_factory=datetime.utcnow)  # 생성 시간
    updated_at: datetime = Field(default_factory=datetime.utcnow, onupdate=datetime.utcnow)  # 마지막 수정 시간

class Menu(TimeStamp, table=True):
    menuname: str = Field(sa_column=Column(String(255), nullable=False))  # 메뉴 이름
    one_time_offer: int = Field(sa_column=Column(Integer, default=0))  # 단품 제공 여부
    is_delete: int = Field(default=0, sa_column=Column(Integer, default=0))  # 삭제 여부 (소프트 삭제)
