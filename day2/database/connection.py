from sqlmodel import create_engine, Session, SQLModel
from dotenv import load_dotenv
import os
import mysql.connector  # MySQL 데이터베이스 연결용

# .env 파일 로드
load_dotenv()

# 환경 변수에서 구성 정보 가져오기
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

# 데이터베이스 URL
MYSQL_URL = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

# mysql 데이터베이스 연결용 URL
BASE_DB_URL = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/mysql"

# 데이터베이스 생성
def create_database():
    connection = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        port=MYSQL_PORT
    )
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE};")
    cursor.close()
    connection.close()

# 데이터베이스 생성 호출
create_database()

# SQLAlchemy 엔진 생성
# DB 연결 설정 더 상세하게//
engine = create_engine(MYSQL_URL, echo=True)

# 데이터베이스 세션 제공
def get_db():
    with Session(engine) as session:
        yield session

# 데이터베이스 테이블 생성
def create_tables():
    from models.users import User
    from models.menus import Menu

    SQLModel.metadata.create_all(engine)
