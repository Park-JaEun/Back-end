from fastapi import APIRouter, Depends, HTTPException 
from sqlmodel import Session

from models.users import UserCreate, UserResponse
from database.connection import get_db
from auth.jwt import create_access_token, pwd_context
from database.search_user import get_all_user, get_user_id, already_user_id 
from database.modify_user import user_signup, modify_admin

router = APIRouter()

# 모든 유저 출력
@router.get("/user/all", response_model=list[UserResponse])
def get_all_users(
    session: Session = Depends(get_db)):

    users = get_all_user(session)
    return users

# 회원가입
@router.post("/signup")
def signup(
    user: UserCreate, 
    session: Session = Depends(get_db)):

    already_user_id(user.user_id, session)
    
    return user_signup(user, session)

# 로그인
@router.post("/login")
def login(
    user_id: str, 
    user_pw: str, 
    session: Session = Depends(get_db)
    ):

    # 유저 ID로 데이터베이스에서 유저 검색
    db_user = get_user_id(user_id, session)
    
    # 비밀번호가 틀린 경우
    if not pwd_context.verify(db_user.user_pw, user_pw):
        raise HTTPException(status_code=400, detail="wrong password")
    
    # JWT 액세스 토큰 생성
    access_token = create_access_token(data={"sub": db_user.user_id})

    return {"access_token": access_token, "token_type": "bearer"}  # 토큰 반환

# 관리자 권한 부여
@router.put("/admin/grant/{user_id}")
def grant_admin(
    user_id: str, 
    session: Session = Depends(get_db)
    ):
    
    return modify_admin(user_id, session, 1)

# 관리자 권한 제거
@router.put("/admin/revoke/{user_id}")
def revoke_admin(
    user_id: str, 
    session: Session = Depends(get_db)
    ):

    return modify_admin(user_id, session, 0)