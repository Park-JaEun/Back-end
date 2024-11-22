from fastapi import FastAPI, Depends, HTTPException, Response
from contextlib import asynccontextmanager
from sqlmodel import Session, select
from database.connection import create_tables, get_mysql_session
from models.users import Menu, MenuCreate, MenuResponse


@asynccontextmanager
async def lifespan(app:FastAPI):
    create_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def get_user(session=Depends(get_mysql_session)):
	return session.exec(select(Menu)).all()


# 특정 메뉴 검색
@app.get("/menus/search/{menu_id}", response_model=Menu)
def get_menu(menu_id: int, session: Session = Depends(get_mysql_session)):

    menu = session.get(Menu, menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail="no menu")
    return menu

# 모든 메뉴 출력
@app.get("/menus/admin/all", response_model=list[MenuResponse])
def get_all_menus(session: Session = Depends(get_mysql_session)):
    menus = session.exec(select(Menu)).all()
    return menus

# is_delete가 0인 메뉴만 출력
@app.get("/menus/all", response_model=list[MenuResponse])
def get_active_menus(session: Session = Depends(get_mysql_session)):
    menus = session.exec(select(Menu).where(Menu.is_delete == 0)).all()
    return menus

# 메뉴 추가
@app.post("/menus/add", response_model=MenuResponse)
def create_menu(menu: MenuCreate, session: Session = Depends(get_mysql_session)):
    db_menu = Menu.from_orm(menu)
    session.add(db_menu)
    session.commit()
    session.refresh(db_menu)
    return db_menu

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
    db_menu = session.get(Menu, menu_id)
    if not db_menu:
        raise HTTPException(status_code=404, detail="no menu")

    db_menu.is_delete = 1

    session.commit()

    return Response(status_code=200, content="delete menu")

# 메뉴 수정
@app.put("/menus/{menu_id}", response_model=Menu)
def update_menu(menu_id: int, new_menu: Menu, session: Session = Depends(get_mysql_session)):
    db_menu = session.get(Menu, menu_id)
    if not db_menu:
        raise HTTPException(status_code=404, detail="no menu")

    if new_menu.menuname is not None:
        db_menu.menuname = new_menu.menuname
    if new_menu.one_time_offer is not None:
        db_menu.one_time_offer = new_menu.one_time_offer

    menu_data = new_menu.model_dump(exclude_unset=True)

    for key, value in menu_data.items():
        setattr(db_menu, key, value)

    session.commit()

    return Response(status_code=200, content="update menu")
