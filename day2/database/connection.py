from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv
import os


load_dotenv()       # .env 파일 로드

DATABASE_FILE = os.getenv("DATABASE_FILE")
SQLITE_URL = os.getenv("SQLITE_URL")
SQLITE_ENGINE = create_engine(SQLITE_URL, echo=True)

# MySQL URL을 환경 변수에서 가져오기
MYSQL_URL = os.getenv("MYSQL_URL")
MYSQL_ENGINE = create_engine(MYSQL_URL, echo=True)


def create_tables():
	SQLModel.metadata.create_all(SQLITE_ENGINE)
	SQLModel.metadata.create_all(MYSQL_ENGINE)

# sqlite와 연결할 세션을 제공하는 종속성 함수
def get_sqlite_session():
    with Session(SQLITE_ENGINE) as session:
        yield session

# MySQL과 연결할 세션을 제공하는 종속성 함수
# MySQL의 day1 DB와 연결
def get_mysql_session():
    with Session(MYSQL_ENGINE) as session:
        yield session