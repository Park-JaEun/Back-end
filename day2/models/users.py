from datetime import datetime  # 생성시간 및 수정시간 처리를 위해 사용
from sqlmodel import SQLModel, Field
from models.time_stamp import TimeStamp

'''
유저
'''
# 유저 데이터의 기본 구조 정의
class User(TimeStamp, table=True):
    user_id: str  # 유저 ID
    user_pw: str  # 비밀번호
    is_admin: int = 0  # 기본값은 일반 유저

    # user_id: str = Field(sa_column=Column(String(255), nullable=False))  # 유저 ID
    # user_pw: str = Field(sa_column=Column(String(255), nullable=False)) # 비밀번호
    # is_admin: int = Field(sa_column=Column(Integer, default=0))  # 기본값은 일반 유저


# 클라이언트 응답 시 반환할 유저 데이터 모델
class UserResponse(SQLModel):
    id: int  # 유저 ID (Primary Key)
    user_id: str  # 유저 ID
    is_admin: int  # 관리자 여부
    created_at: datetime  # 생성 시간
    updated_at: datetime  # 마지막 수정 시간


# 유저 데이터 생성 시 사용할 모델 (클라이언트 요청)
class UserCreate(SQLModel):
    user_id: str  # 유저 ID
    user_pw: str  # 비밀번호
    is_admin: int = 0  # 기본값은 일반 유저