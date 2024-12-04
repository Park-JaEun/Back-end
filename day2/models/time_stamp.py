from sqlalchemy import Column, DateTime  # SQLAlchemy를 사용해 컬럼 타입 지정
from datetime import datetime  # 생성시간 및 수정시간 처리를 위해 사용
from sqlmodel import SQLModel, Field

'''
DB 공동 사용 모델
DB id, 생성 시간, 마지막 수정 시간을 공통적으로 사용하는 모델
'''
class TimeStamp(SQLModel):
    id: int = Field(default=None, primary_key=True)  # DB ID (Primary Key)
    created_at: datetime = Field(
        default_factory=datetime.utcnow, sa_column=Column(DateTime, nullable=False)
    )  # 생성 시간
    updated_at: datetime = Field(
        default_factory=datetime.utcnow, sa_column=Column(DateTime, nullable=False, onupdate=datetime.utcnow)
    )  # 마지막 수정 시간
