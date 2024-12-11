from datetime import datetime, timedelta
import jwt
from dotenv import load_dotenv
import os

from fastapi import  Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from argon2 import PasswordHasher  # argon2 사용
from sqlmodel import Session, select


from models.users import User    # 유저 모델
from database.connection import get_db

# .env 파일 로드
load_dotenv()

# 환경 변수에서 MySQL URL 가져오기
SECRET_KEY = os.getenv("SECRET_KEY")    # 비밀 키 (보안 유지)
ALGORITHM = os.getenv("ALGORITHM")      # 사용할 암호화 알고리즘
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")) # 액세스 토큰 만료 시간 (30분)


# 비밀번호 해싱 및 검증을 위한 설정
pwd_context = PasswordHasher()

# HTTPBearer 보안 스키마
security = HTTPBearer()

#  토큰 매니저 클래스를 만들어 밑의 함수들을 넣어두면 다른 곳에서 호출할 때, inculde 하기 간편!

def create_access_token(
        data: dict, 
        ):
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=15))  # 지원하지 않는 함수 수정
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: HTTPAuthorizationCredentials):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    
    # 에러에 따른 다른 에러 메세지 지정해야....
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    

# JWT 검증 의존성
def get_current_user(
        token: HTTPAuthorizationCredentials = Security(security), 
        session: Session = Depends(get_db)):
    
    try:
        if token is None:
            raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")

        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        
        # 유효한 토큰이면 유저 정보를 저장
        user = session.exec(select(User).where(User.user_id == user_id)).first()    
        if user is None:
            raise HTTPException(status_code=401, detail="유저를 찾을 수 없습니다.")
        return user
    
    # 에러에 따른 다른 에러 메세지 지정해야....
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")

