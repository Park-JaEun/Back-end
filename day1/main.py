from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from models.users import Menu
from database.connection import conn, get_session

app = FastAPI()

@app.on_event("startup")
def on_startup():
    conn()

@app.get("/")
async def get_user(session=Depends(get_session)):
	return session.exec(select(Menu)).all()

# 모든 메뉴 출력
@app.get("/menus/", response_model=list[Menu])
def get_all_menus(session: Session = Depends(get_session)):
    
    menus = session.exec(select(Menu)).all()
    return menus

# 특정 메뉴 검색
@app.get("/menus/{menu_id}", response_model=Menu)
def get_menu(menu_id: int, session: Session = Depends(get_session)):

    menu = session.get(Menu, menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail="no menu")
    return menu

# 메뉴 추가
@app.post("/menus/", response_model=Menu)
def create_menu(menu: Menu, session: Session = Depends(get_session)):
   
    session.add(menu)
    session.commit()
    session.refresh(menu)
    return menu

# 메뉴 삭제
@app.delete("/menus/{menu_id}", response_model=Menu)
def delete_menu(menu_id: int, session: Session = Depends(get_session)):
    # 삭제할 메뉴 검색
    db_menu = session.get(Menu, menu_id)
    if not db_menu:
        raise HTTPException(status_code=404, detail="no menu")
    
    # 메뉴 삭제
    session.delete(db_menu)
    session.commit()
    return db_menu  # 삭제한 메뉴 정보 반환

# 메뉴 수정
@app.put("/menus/{menu_id}", response_model=Menu)
def update_menu(menu_id: int, new_menu: Menu, session: Session = Depends(get_session)):
    # 수정할 메뉴 검색
    db_menu = session.get(Menu, menu_id)
    if not db_menu:
        raise HTTPException(status_code=404, detail="no menu")
    
    # 메뉴 정보 업데이트
    if new_menu is not None:
        db_menu.menuname = new_menu.menuname
    if new_menu.one_time_offer is not None:
        db_menu.one_time_offer = new_menu.one_time_offer
    
    session.add(db_menu)
    session.commit()
    session.refresh(db_menu)
    
    return db_menu  # 업데이트된 메뉴 리턴




if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
