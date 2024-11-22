from sqlmodel import create_engine, Session
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

# 환경 변수에서 MySQL URL 가져오기
MYSQL_URL = os.getenv("MYSQL_URL")
if not MYSQL_URL:
    raise ValueError("MYSQL_URL 환경 변수가 설정되지 않았습니다.")

# SQLAlchemy 엔진 생성
engine = create_engine(MYSQL_URL, echo=True)

# 데이터베이스 세션 제공
def get_mysql_session():
    with Session(engine) as session:
        yield session

# 데이터베이스 테이블 생성
def create_tables():
    from sqlmodel import SQLModel
    from models.users import Menu, UserDB
    SQLModel.metadata.create_all(engine)
