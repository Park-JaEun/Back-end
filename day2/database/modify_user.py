from fastapi import Depends, Response
from sqlmodel import Session

from models.users import User, UserCreate
from database.connection import get_db
from auth.jwt import pwd_context
from database.search_user import get_user_id

def switch(key):
  admin = {0 : "no admin", 1: "admin"}.get(key, "non")
  return admin

# 회원 가입 정보 db 저장
def user_signup(
    user: UserCreate, 
    session: Session
    ):

    # 비밀번호 데이터베이스에 저장
    hashed_password = pwd_context.hash(user.user_pw)
    new_user = User(
        user_id=user.user_id, user_pw=hashed_password, is_admin=user.is_admin
    )  # 유저 데이터 생성
    # print(new_user.user_id)
    session.add(new_user)  # 데이터베이스에 추가
    session.commit()  # 변경사항 저장
    session.refresh(new_user)  # 새로 추가된 유저 데이터 반환을 위해 새로고침
    return Response(status_code=200, content="add user")

# 관리자 권한 수정
def modify_admin(
    user_id: str, 
    session: Session = Depends(get_db),
    grant: int=0
    ):
    
    # 유저 ID로 데이터베이스에서 유저 검색
    db_user = get_user_id(user_id, session)
    
    # 관리자 권한 부여
    db_user.is_admin = grant
    session.commit()  # 변경사항 저장
    session.refresh(db_user)  # 갱신된 데이터 반환
    
    return {"message": f"User {user_id} is {switch(grant)} now"}