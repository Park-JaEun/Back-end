from fastapi import HTTPException
from sqlmodel import Session

from models.menus import Menu, MenuCreate


def db_create_menu(
    menu: MenuCreate, 
    session: Session
    ):

    db_menu = Menu.model_validate(menu)
    session.add(db_menu)
    session.commit()
    session.refresh(db_menu)

    return db_menu

def db_hard_delete_menu(
    menu_id: int, 
    session: Session
   ):
    
    # 삭제할 메뉴 검색
    db_menu = session.get(Menu, menu_id)
    if not db_menu:
        raise HTTPException(status_code=404, detail="no menu")

    # 메뉴 삭제
    session.delete(db_menu)
    session.commit()

def db_soft_delete_menu(
    menu_id: int, 
    session: Session 
    ):
    
    db_menu = session.get(Menu, menu_id)
    if not db_menu:
        raise HTTPException(status_code=404, detail="no menu")

    db_menu.is_delete = 1

    session.commit()


def db_update_menu(
    menu_id: int, 
    new_menu: MenuCreate,   # 메뉴 업데이트 시에는 메뉴 이름과 offer만 입력하면 되니 Menu가 아닌 MenuCreate class
    session: Session
    ):

    db_menu = session.get(Menu, menu_id)
    if not db_menu:
        raise HTTPException(status_code=404, detail="no menu")

    menu_data = new_menu.model_dump(exclude_unset=True)

    for key, value in menu_data.items():
        setattr(db_menu, key, value)

    session.commit()

