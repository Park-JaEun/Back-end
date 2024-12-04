from fastapi import HTTPException
from sqlmodel import Session, select

from models.menus import Menu

def search_menu_by_id(
        menu_id: int, 
        session: Session
        ):
    menu = session.exec(select(Menu).where(Menu.is_delete == 0, Menu.id == menu_id)).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    return menu

def search_active_menus(
        session: Session
                        ):
    return session.exec(select(Menu).where(Menu.is_delete == 0)).all()

def search_all_menus(
        session: Session
                        ):
    return session.exec(select(Menu)).all()