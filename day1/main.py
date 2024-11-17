from fastapi import FastAPI, Depends, HTTPException, Response
from contextlib import asynccontextmanager
from sqlmodel import Session, select
from models.users import Menu
from database.connection import create_tables, get_mysql_session


from pydantic import BaseModel  # Pydantic 모델을 정의하는 데 필요


@asynccontextmanager
async def lifespan(app:FastAPI):
    create_tables()
    # 애플리케이션 실행 시 실행될 코드
    yield
    # 애플리케이션 종료 시 실행될 코드

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def get_user(session=Depends(get_mysql_session)):
	return session.exec(select(Menu)).all()

# is_delete가 0인 메뉴만 출력
@app.get("/menus/all", response_model=list[Menu])
def get_active_menus(session: Session = Depends(get_mysql_session)):
    menus = session.exec(select(Menu).where(Menu.is_delete == 0)).all()
    return menus

# 모든 메뉴 출력
@app.get("/menus/admin/all", response_model=list[Menu])
def get_all_menus(session: Session = Depends(get_mysql_session)):
    menus = session.exec(select(Menu)).all()
    return menus

# 특정 메뉴 검색
@app.get("/menus/{menu_id}", response_model=Menu)
def get_menu(menu_id: int, session: Session = Depends(get_mysql_session)):

    menu = session.get(Menu, menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail="no menu")
    return menu

# 메뉴 추가
@app.post("/menus/", response_model=Menu)
def create_menu(menu: Menu, session: Session = Depends(get_mysql_session)):
   
    session.add(menu)
    session.commit()
    
    session.refresh(menu)
    return menu

# 메뉴 완전히 삭제
@app.delete("/menus/admin/delete/{menu_id}", response_model=Menu)
def hard_delete_menu(menu_id: int, session: Session = Depends(get_mysql_session)):
    # 삭제할 메뉴 검색
    db_menu = session.get(Menu, menu_id)
    if not db_menu:
        raise HTTPException(status_code=404, detail="no menu")
    
    # 메뉴 삭제
    session.delete(db_menu)
    session.commit()
    return Response(status_code=200, content="hard delete menu")

# 메뉴 삭제
@app.delete("/menus/delete/{menu_id}", response_model=Menu)
def soft_delete_menu(menu_id: int, session: Session = Depends(get_mysql_session)):
    # 삭제할 메뉴 검색
    db_menu = session.get(Menu, menu_id)
    if not db_menu:
        raise HTTPException(status_code=404, detail="no menu")
    
    # soft delete: is_delete 값을 1로 설정
    db_menu.is_delete = 1

    # 변경 사항 커밋
    session.commit()
    
    return Response(status_code=200, content="delete menu")

# 메뉴 수정
@app.put("/menus/{menu_id}", response_model=Menu)
def update_menu(menu_id: int, new_menu: Menu, session: Session = Depends(get_mysql_session)):
    # 수정할 메뉴 검색
    db_menu = session.get(Menu, menu_id)
    if not db_menu:
        raise HTTPException(status_code=404, detail="no menu")
    
    # 메뉴 정보 업데이트
    if new_menu.menuname is not None:
        db_menu.menuname = new_menu.menuname
    if new_menu.one_time_offer is not None:
        db_menu.one_time_offer = new_menu.one_time_offer
       
    # exclude_unset=True 옵션: exclude_unset=True를 통해 new_menu에서 설정된 값만 딕셔너리에 포함
    menu_data = new_menu.model_dump(exclude_unset=True) 

    for key, value in menu_data.items():
        setattr(db_menu, key, value)    # 데이터베이스 객체의 각 속성에 새 값을 할당

    session.commit()
    
    return Response(status_code=200, content="update menu")



