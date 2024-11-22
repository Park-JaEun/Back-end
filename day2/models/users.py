from sqlalchemy import Column, Integer, String, Boolean, DateTime  # SQLAlchemy를 사용해 컬럼 타입 지정
from datetime import datetime  # 생성시간 및 수정시간 처리를 위해 사용
from sqlmodel import SQLModel, Field

'''
메뉴
'''
# 데이터베이스에서 사용할 기본 Menu 테이블
class MenuBase(SQLModel):
    pass

class Menu(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)  # 메뉴 ID
    menuname: str = Field(sa_column=Column(String(255), nullable=False))  # 메뉴 이름
    one_time_offer: int = Field(sa_column=Column(Integer, default=0))  # 단품 제공 여부
    is_delete: int = Field(sa_column=Column(Integer, default=0))  # 삭제 여부 (소프트 삭제)

# 요청(Request)용 모델
class MenuCreate(SQLModel):
    menuname: str  # 메뉴 이름
    one_time_offer: int = 0  # 단품 제공 여부

# 응답(Response)용 모델
class MenuResponse(SQLModel):
    id: int  # 메뉴 ID
    menuname: str  # 메뉴 이름
    one_time_offer: int  # 단품 제공 여부
    is_delete: int  # 삭제 여부


'''
유저 정보
'''
# 유저 데이터의 기본 구조 정의
class UserBase(SQLModel):
    user_id: str = Field(sa_column=Column(String(255), unique=True, nullable=False))  # 유저 ID (고유 값)
    user_pw: str = Field(sa_column=Column(String(255), nullable=False))  # 유저 비밀번호 (해싱된 값)
    is_admin: bool = Field(sa_column=Column(Boolean, default=False))  # 관리자 여부

# 데이터베이스에서 사용할 유저 테이블
class UserDB(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)  # 유저 ID (Primary Key)
    created_at: datetime = Field(
        default_factory=datetime.utcnow, sa_column=Column(DateTime, nullable=False)
    )  # 생성 시간
    updated_at: datetime = Field(
        default_factory=datetime.utcnow, sa_column=Column(DateTime, nullable=False, onupdate=datetime.utcnow)
    )  # 마지막 수정 시간

# 유저 데이터 생성 시 사용할 모델 (클라이언트 요청)
class UserCreate(SQLModel):
    user_id: str  # 유저 ID
    user_pw: str  # 비밀번호
    is_admin: bool = False  # 기본값은 일반 유저

# 클라이언트 응답 시 반환할 유저 데이터 모델
class UserResponse(SQLModel):
    id: int  # 유저 ID (Primary Key)
    user_id: str  # 유저 ID
    is_admin: bool  # 관리자 여부
    created_at: datetime  # 생성 시간
    updated_at: datetime  # 마지막 수정 시간
