from sqlalchemy import Column, Integer, String
from sqlmodel import SQLModel, Field

# 데이터베이스에서 사용할 기본 Menu 테이블
class MenuBase(SQLModel):
    pass

class Menu(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    menuname: str = Field(sa_column=Column(String(255), nullable=False))  # VARCHAR(255) 길이 지정
    one_time_offer: int = Field(sa_column=Column(Integer, default=0))
    is_delete: int = Field(sa_column=Column(Integer, default=0))

# 요청(Request)용 모델
class MenuCreate(SQLModel):
    menuname: str
    one_time_offer: int = 0

# 응답(Response)용 모델
class MenuResponse(SQLModel):
    id: int
    menuname: str
    one_time_offer: int
    is_delete: int
