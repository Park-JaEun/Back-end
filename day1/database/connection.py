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


'''
직관적인 함수 이름으로 변경
'''
def create_tables():
	# DB에 연결하여 선언된 테이블들이 존재하는지 확인하고
    # 없다면 테이블들을 생성해준다.
	SQLModel.metadata.create_all(SQLITE_ENGINE)
	SQLModel.metadata.create_all(MYSQL_ENGINE)

# def get_session():
#     # 세션을 제공하는 종속성 함수
#     with Session(ENGINE) as session:
#         yield session


'''
여러 상황에 따라 데이터베이스를 여러개 사용하게 된다면 
연결할 각 데이터베이스를 호출하는 함수들을 만들어두고 
api 호출에서 구분하는 방식을 사용할 수 있다.
'''
def get_sqlite_session():
    # sqlite와 연결할 세션을 제공하는 종속성 함수
    with Session(SQLITE_ENGINE) as session:
        yield session

def get_mysql_session():
    # MySQL과 연결할 세션을 제공하는 종속성 함수
    with Session(MYSQL_ENGINE) as session:
        yield session