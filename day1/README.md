# day1 실습

## SQLite과 FastAPI 연결하기 
2024-11-9
- 데이터 넣기 C
- 데이터 불러오기 R
- 데이터 수정하기 U
- 데이터 삭제하기 D

## MySQL을 FastAPI와 연결하기, DB 연결 함수 여러개로 나누기
2024-11-12

여러 상황에서 여러 개의 데이터베이스를 사용해야 하는 경우, 각 데이터베이스에 접근하는 함수를 별도로 정의하여 API 호출에서 데이터베이스를 구분하는 방식으로 사용할 수 있다. 이를 통해 특정 요청이 특정 데이터베이스와 상호작용하도록 관리할 수 있다.
- 데이터베이스 연결 함수 분리: 각 데이터베이스에 대해 개별적인 연결 함수를 정의한다.
- API에서 데이터베이스 구분: API 호출 시 요청에 따라 적절한 데이터베이스 연결 함수를 선택한다.
- 유연한 데이터베이스 사용: 요청에 따라 각기 다른 데이터베이스와 연결해서 다양한 데이터베이스를 유연하게 사용할 수 있다. 

--> 다중 데이터베이스 구조를 관리할 수 있다.

## update_menu api 수정
2024-11-12

- `model_dump(exclude_unset=True)` 사용
    
    `model_dump(exclude_unset=True)`를 사용하여 `new_menu`에서 설정된 값만 딕셔너리로 가져온 후, 자동으로 필드에 할당한다. `model_dump(exclude_unset=True)`는 `new_menu`에 설정된 필드만 가져오기 때문에 매번 모든 필드를 수동으로 확인할 필요가 없다.
    
- `session.add()` 생략
    
    `session.get()`으로 가져온 객체는 이미 세션에 연결되어 있어 `add()`가 필요하지 않다.

## hard_delete_menu api, hard_delete_menu api 구분
2024-11-13

삭제 방식을 구분함으로써 시스템은 데이터 보존 요구와 데이터 관리 최적화 요구를 모두 충족하는 것을 기대한다.

### Soft Delete
 is_delete 필드를 사용하여 논리적으로 데이터가 삭제된 것처럼 표시하며, 데이터는 여전히 데이터베이스에 존재한다. 데이터 복구 및 추적을 위해 사용한다.

- Soft Delete 로직
    1. menu_id로 데이터베이스에서 메뉴를 조회한다.
    2. 해당 메뉴가 없으면 404 Not Found 에러를 반환한다.
    3. 메뉴의 is_delete 필드를 1로 설정하고, commit하여 데이터베이스에 반영한다.

### Hard Delete
데이터베이스에서 레코드를 완전히 제거하여, 더 이상 데이터가 남지 않게 한다.

- hard delete 로직
    1. menu_id로 데이터베이스에서 메뉴를 조회한다.
    2. 해당 메뉴가 없으면 404 Not Found 에러를 반환한다.
    3. 조회된 메뉴를 session.delete()로 삭제하고, commit하여 데이터베이스에서 영구적으로 제거한다.


### Menu class를 calum 베이스로 변경하고 요청받을 데이터만 Field로 정의
2024-11-15

- Menu class
    - 데이터베이스에 저장되는 실제 테이블 정의.
    - sa_column=Column(...)을 사용해 SQLAlchemy 스타일로 정의.

- MenuCreate api
    - API에서 클라이언트가 요청(Request)할 때 사용할 모델.
    - 필요한 필드만 포함.

- MenuResponse api
    - API에서 클라이언트에게 반환(Response)할 때 사용할 모델.
    - 데이터베이스의 모든 필드를 포함.

- menuname 필드 수정
    - sa_column=Column(String(255), nullable=False)로 수정.
    - VARCHAR 타입에 255 길이를 지정.
    - 나머지 필드는 기존 구조를 유지하면서 SQLAlchemy Column으로 정의.