from sqlalchemy import Column, Integer, String  # SQLAlchemy를 사용해 컬럼 타입 지정
from sqlmodel import SQLModel, Field

from models.time_stamp import TimeStamp

'''
메뉴
'''
# 데이터베이스에서 사용할 기본 Menu 테이블 dho dkseho...
class Menu(TimeStamp, table=True):
    menuname: str = Field(sa_column=Column(String(255), nullable=False))  # 메뉴 이름
    one_time_offer: int = Field(sa_column=Column(Integer, default=0))  # 단품 제공 여부
    is_delete: int = Field( default=0, sa_column=Column(Integer, default=0))  # 삭제 여부 (소프트 삭제)

# class Menu(SQLModel, table=True):
#     id: int = Field(default=None, primary_key=True)  # 메뉴 ID
#     menuname: str = Field(sa_column=Column(String(255), nullable=False))  # 메뉴 이름
#     one_time_offer: int = Field(sa_column=Column(Integer, default=0))  # 단품 제공 여부
#     is_delete: int = Field( default=0, sa_column=Column(Integer, default=0))  # 삭제 여부 (소프트 삭제)

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