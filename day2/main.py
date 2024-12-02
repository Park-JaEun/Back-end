from datetime import timedelta, datetime  # JWT 만료시간
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, Response, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt  # JWT 생성 및 인증
from passlib.context import CryptContext  # 비밀번호 해싱 및 검증
from sqlmodel import Session, select
from dotenv import load_dotenv
import os

from models.users import UserDB, UserCreate, UserResponse  # 유저 모델
from database.connection import create_tables, get_db
from models.users import Menu, MenuCreate, MenuResponse

# .env 파일 로드
load_dotenv()

# 환경 변수에서 MySQL URL 가져오기
SECRET_KEY = os.getenv("SECRET_KEY")    # 비밀 키 (보안 유지)
ALGORITHM = os.getenv("ALGORITHM")      # 사용할 암호화 알고리즘
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")) # 액세스 토큰 만료 시간 (30분)

# 비밀번호 해싱 및 검증을 위한 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTPBearer 보안 스키마
security = HTTPBearer()

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
        user = session.exec(select(UserDB).where(UserDB.user_id == user_id)).first()    
        if user is None:
            raise HTTPException(status_code=401, detail="유저를 찾을 수 없습니다.")
        return user
    
    except JWTError:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")


@asynccontextmanager
async def lifespan(app:FastAPI):
    create_tables()
    yield

app = FastAPI(lifespan=lifespan)


''' 메뉴와 관련된 api는 모두 login 체크 '''
''' 일반 유저 '''
# 특정 메뉴 검색 +)JWT 검증
@app.get("/menus/search/{menu_id}", response_model=Menu)
def get_menu_by_id(
    menu_id: int, 
    session: Session = Depends(get_db)
    ):

    # menu = session.get(Menu, menu_id)
    # menu = session.exec(select(Menu).where(Menu.is_delete == 0, Menu.id == 0)).first()
    menu = session.exec(Menu).filter(Menu.menu_id == menu_id, Menu.is_delete == 0).first()

    if not menu:
        raise HTTPException(status_code=404, detail="메뉴를 찾을 수 없습니다.")
    return menu

# is_delete가 0인 메뉴만 출력 +)JWT 검증
@app.get("/menus/all", response_model=list[MenuResponse])
def get_active_menus(
    session: Session = Depends(get_db)
    ):

    # menus = session.exec(select(Menu).where(Menu.is_delete == 0)).all()
    menus = session.exec(Menu).filter(Menu.is_delete == 0).all()

    return menus

''' 관리자 유저'''
# 모든 메뉴 출력 +)JWT 검증
@app.get("/menus/admin/all", response_model=list[MenuResponse])
def get_menu(
    session: Session = Depends(get_db), 
    current_user: UserDB = Depends(get_current_user)
    ):

    # admin인지 확인 후 아니면 에러반환
    if current_user.is_admin != 1:
        raise HTTPException(status_code=403, detail="관리자 권환이 필요합니다.")
    
    return session.exec(select(Menu)).all()

# 메뉴 추가 +)JWT 검증, admin 확인
@app.post("/menus/admin/add", response_model=MenuResponse)
def create_menu(
    menu: MenuCreate, 
    session: Session = Depends(get_db), 
    current_user: UserDB = Depends(get_current_user)):

    # admin인지 확인 후 아니면 에러반환
    if current_user.is_admin != 1:
        raise HTTPException(status_code=403, detail="관리자 권환이 필요합니다.")

    db_menu = Menu.model_validate(menu)
    session.add(db_menu)
    session.commit()
    session.refresh(db_menu)
    return db_menu

# 메뉴 완전히 삭제 +)JWT 검증
@app.delete("/menus/admin/delete/{menu_id}")
def hard_delete_menu(
    menu_id: int, 
    session: Session = Depends(get_db), 
    current_user: UserDB = Depends(get_current_user)):

    # admin인지 확인 후 아니면 에러반환
    if current_user.is_admin != 1:
        raise HTTPException(status_code=403, detail="관리자 권환이 필요합니다.")

    # 삭제할 메뉴 검색
    db_menu = session.get(Menu, menu_id)
    if not db_menu:
        raise HTTPException(status_code=404, detail="no menu")

    # 메뉴 삭제
    session.delete(db_menu)
    session.commit()
    return Response(status_code=200, content="hard delete menu")

# 메뉴 삭제 +)JWT 검증
@app.delete("/menus/admin/delete/{menu_id}")
def soft_delete_menu(
    menu_id: int, session: Session = Depends(get_db), 
    current_user: UserDB = Depends(get_current_user)):
    
    # admin인지 확인 후 아니면 에러반환
    if current_user.is_admin != 1:
        raise HTTPException(status_code=403, detail="관리자 권환이 필요합니다.")
    
    db_menu = session.get(Menu, menu_id)
    if not db_menu:
        raise HTTPException(status_code=404, detail="no menu")

    db_menu.is_delete = 1

    session.commit()

    return Response(status_code=200, content="delete menu")


# 메뉴 수정 +)JWT 검증
@app.patch("/menus/admin/{menu_id}")
def update_menu(
    menu_id: int, 
    new_menu: MenuCreate,   # 메뉴 업데이트 시에는 메뉴 이름과 offer만 입력하면 되니 Menu가 아닌 MenuCreate class
    session: Session = Depends(get_db), 
    current_user: UserDB = Depends(get_current_user)):

    # admin인지 확인 후 아니면 에러반환
    if current_user.is_admin != 1:
        raise HTTPException(status_code=403, detail="관리자 권환이 필요합니다.")
    
    db_menu = session.get(Menu, menu_id)
    if not db_menu:
        raise HTTPException(status_code=404, detail="no menu")

    menu_data = new_menu.model_dump(exclude_unset=True)

    for key, value in menu_data.items():
        setattr(db_menu, key, value)

    session.commit()

    return Response(status_code=200, content="update menu")



''' user 관련 '''
# JWT 생성 함수
def create_access_token(
    data: dict, 
    expires_delta: timedelta | None = None):

    to_encode = data.copy()  # JWT에 포함할 데이터를 복사
    if expires_delta:  # 만료 시간이 지정된 경우
        expire = datetime.now() + expires_delta
    else:  # 기본 만료 시간 설정
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})  # 만료 시간 추가
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # JWT 생성 및 반환


# 모든 유저 출력
@app.get("/user/all", response_model=list[UserResponse])
def get_all_users(
    session: Session = Depends(get_db)):

    users = session.exec(select(UserDB)).all()
    return users

# 회원가입
@app.post("/signup")
def signup(
    user: UserCreate, 
    session: Session = Depends(get_db)):

    # 이미 등록된 유저인지 확인
    db_user = session.exec(select(UserDB).where(UserDB.user_id == user.user_id)).first()
    if db_user:  # 중복된 유저 ID인 경우 예외 발생
        raise HTTPException(status_code=409, detail="User already registered")
    
    # 비밀번호 데이터베이스에 저장
    hashed_password = pwd_context.hash(user.user_pw)
    new_user = UserDB(
        user_id=user.user_id, user_pw=hashed_password, is_admin=user.is_admin
    )  # 유저 데이터 생성
    print(new_user.user_id)
    session.add(new_user)  # 데이터베이스에 추가
    session.commit()  # 변경사항 저장
    session.refresh(new_user)  # 새로 추가된 유저 데이터 반환을 위해 새로고침
    return Response(status_code=200, content="add user")

# 로그인
@app.post("/login")
def login(
    user_id: str, 
    user_pw: str, 
    session: Session = Depends(get_db)
    ):

    # 유저 ID로 데이터베이스에서 유저 검색
    db_user = session.exec(select(UserDB).where(UserDB.user_id == user_id)).first()
    # 유저가 존재하지 않거나 비밀번호가 틀린 경우
    if not db_user or not pwd_context.verify(user_pw, db_user.user_pw):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    # JWT 액세스 토큰 생성
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.user_id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}  # 토큰 반환

# 관리자 권한 부여
@app.put("/admin/grant/{user_id}")
def grant_admin(
    user_id: str, 
    session: Session = Depends(get_db)
    ):
    
    # 유저 ID로 데이터베이스에서 유저 검색
    db_user = session.exec(select(UserDB).where(UserDB.user_id == user_id)).first()
    if not db_user:  # 유저가 존재하지 않으면 예외 발생
        raise HTTPException(status_code=404, detail="User not found")
    
    # 관리자 권한 부여
    db_user.is_admin = True
    session.commit()  # 변경사항 저장
    session.refresh(db_user)  # 갱신된 데이터 반환
    return {"message": f"User {user_id} is admin now"}

# 관리자 권한 제거
@app.put("/admin/revoke/{user_id}")
def revoke_admin(
    user_id: str, 
    session: Session = Depends(get_db)
    ):

    # 유저 ID로 데이터베이스에서 유저 검색
    db_user = session.exec(select(UserDB).where(UserDB.user_id == user_id)).first()
    if not db_user:  # 유저가 존재하지 않으면 예외 발생
        raise HTTPException(status_code=404, detail="User not found")
    
    # 관리자 권한 제거
    db_user.is_admin = False
    session.commit()  # 변경사항 저장
    session.refresh(db_user)  # 갱신된 데이터 반환
    return {"message": f"User {user_id} is not admin now"}



