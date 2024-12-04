
from fastapi import HTTPException
from sqlmodel import Session, select
from models.users import User

# 모든 유저 검색
def get_all_user(
    session: Session
    ):

    users = session.exec(select(User)).all()
    return users

# 유저 id로 검색
def get_user_id(
    user_id: str, 
    session: Session
):
    # 유저 ID로 데이터베이스에서 유저 검색
    db_user = session.exec(select(User).where(User.user_id == user_id)).first()
    if not db_user:  # 유저가 존재하지 않으면 예외 발생
        raise HTTPException(status_code=404, detail="User not found")
    
    return db_user

# id로 등록된 유저인지 검색
def already_user_id(
    user_id: str, 
    session: Session
):
    # 유저 ID로 데이터베이스에서 유저 검색
    db_user = session.exec(select(User).where(User.user_id == user_id)).first()
    if db_user:  # 중복된 유저 ID인 경우 예외 발생
        raise HTTPException(status_code=409, detail="User already registered")
    
    return db_user
    
