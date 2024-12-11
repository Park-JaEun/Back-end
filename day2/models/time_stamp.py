from sqlalchemy import Column, DateTime  # SQLAlchemy를 사용해 컬럼 타입 지정
from datetime import datetime  # 생성시간 및 수정시간 처리를 위해 사용
from sqlmodel import SQLModel, Field

'''
DB 공동 사용 모델
DB id, 생성 시간, 마지막 수정 시간을 공통적으로 사용하는 모델
'''
class TimeStamp(SQLModel):

    # 같은 성격이지만 다른 내용의 컬럼은 테이블 별로 따로 설정하는게 나음!
    # 상속 하지 말고..!
    id: int = Field(default=None, primary_key=True)  # DB ID (Primary Key)
    
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_type=DateTime
    )  # 생성 시간
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_type=DateTime
    )  # 마지막 수정 시간
