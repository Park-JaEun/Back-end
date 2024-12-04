from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import Session

from models.menus import MenuCreate, MenuResponse
from models.users import User  # 유저 모델
from database.connection import get_db
from auth.jwt import get_current_user
from database.search_menu import search_menu_by_id, search_active_menus,search_all_menus
from database.modify_menu import db_create_menu, db_hard_delete_menu, db_soft_delete_menu,db_update_menu

router = APIRouter()

@router.get("/menus/search/{menu_id}", response_model=MenuResponse)
def get_menu_by_id(menu_id: int, session: Session = Depends(get_db)):
    return search_menu_by_id(menu_id, session)

# 모든 메뉴 출력
@router.get("/menus/all", response_model=list[MenuResponse])
def get_active_menus(session: Session = Depends(get_db)):
    return search_active_menus(session)

# 모든 메뉴 출력 +)JWT 검증
@router.get("/menus/admin/all", response_model=list[MenuResponse])
def get_menu(
    session: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
    ):

    # admin인지 확인 후 아니면 에러반환
    if current_user.is_admin != 1:
        raise HTTPException(status_code=403, detail="관리자 권환이 필요합니다.")
    
    return search_all_menus(session)


# 메뉴 추가 +)JWT 검증, admin 확인
@router.post("/menus/admin/add", response_model=MenuResponse)
def create_menu(
    menu: MenuCreate, 
    session: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)):

    # admin인지 확인 후 아니면 에러반환
    if current_user.is_admin != 1:
        raise HTTPException(status_code=403, detail="관리자 권환이 필요합니다.")

    return db_create_menu(menu, session)

# 메뉴 완전히 삭제 +)JWT 검증, admin 확인
@router.delete("/menus/admin/delete/hard/{menu_id}")
def hard_delete_menu(
    menu_id: int, 
    session: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)):

    # admin인지 확인 후 아니면 에러반환
    if current_user.is_admin != 1:
        raise HTTPException(status_code=403, detail="관리자 권환이 필요합니다.")

    db_hard_delete_menu(menu_id,session)

    return Response(status_code=200, content="hard delete menu")

# 메뉴 삭제 +)JWT 검증, admin 확인
@router.delete("/menus/admin/delete/soft/{menu_id}")
def soft_delete_menu(
    menu_id: int, session: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)):
    
    # admin인지 확인 후 아니면 에러반환
    if current_user.is_admin != 1:
        raise HTTPException(status_code=403, detail="관리자 권환이 필요합니다.")
    
    db_soft_delete_menu(menu_id,session)

    return Response(status_code=200, content="delete menu")


# 메뉴 수정 +)JWT 검증, admin 확인
@router.patch("/menus/admin/{menu_id}")
def update_menu(
    menu_id: int, 
    new_menu: MenuCreate,   # 메뉴 업데이트 시에는 메뉴 이름과 offer만 입력하면 되니 Menu가 아닌 MenuCreate class
    session: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)):

    # admin인지 확인 후 아니면 에러반환
    if current_user.is_admin != 1:
        raise HTTPException(status_code=403, detail="관리자 권환이 필요합니다.")
    
    db_update_menu(menu_id, new_menu, session)

    return Response(status_code=200, content="update menu")