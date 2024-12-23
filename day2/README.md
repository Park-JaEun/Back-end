
---
---
## 유저 DB table
2024-11-22

- User 모델
    - 데이터베이스에서 사용할 유저 정보를 담은 테이블 정의.
    - created_at 및 updated_at으로 생성/수정 시간을 기록.
---
---
## 회원 가입
2024-11-22
1. 회원가입 요청 처리
- /user/add 경로에서 회원가입 요청 처리.
- 요청 본문은 UserCreate 기반으로 데이터가 전달.
2. 중복 유저 검사
- DB에서 동일한 user_id 중복 체크.
- 중복이면 HTTPException을 발생시켜 409 Conflict 에러 코드.

3. 비밀번호 해싱
사용자의 비밀번호를 해싱해 데이터베이스에 저장.
- pwd_context.hash 메서드를 사용해 안전한 암호화된 비밀번호를 생성. (평문으로 저장하지 않기 위해)

4. 유저 데이터 생성
- UserDB 모델 객체를 생성해 사용자의 데이터 캡슐화.
- is_admin는 일반 사용자(False:0)로 설정.

5. 데이터베이스 저장
- SQLAlchemy 세션으로 새 유저 데이터를 데이터베이스에 추가.

6. 응답 반환
- 회원가입 성공 시, 새 유저 데이터를 반환.
- 반환 모델은 필수 정보만 있는 UserResponse.
---
---
## JWT 인증
2024-11-22

create_access_token 함수로 JWT 생성.
토큰 만료 시간을 명시적으로 관리.

- JWT 검증을 위한 의존성 함수 추가 
    - 토큰을 검증하고 유저 정보를 가져오는 의존성을 만듬.

- 메뉴 API에 로그인 확인 의존성 적용
    - 모든 메뉴 API 엔드포인트에 의존성을 추가해 로그인 상태를 확인함.
---
---
## create_access_token 함수
2024-11-22

1. 데이터 준비
입력 데이터를 복사.

2. 만료 시간 설정
유효기간(expires_delta)이 주어지면 이를 기반으로 만료 시간을 계산.
유효기간이 없으면 15분 후(디폴트 값)를 만료 시간으로 설정.

3. 만료 시간 포함
exp 키를 통해 만료 시간을 데이터에 추가.

4. JWT 생성
준비된 데이터와 SECRET_KEY, 알고리즘을 사용하여 JWT를 생성.

5. 토큰 반환
생성된 JWT 문자열을 반환.


---
---
## admin(관리자)만 menu를 수정, 삭제할 수 있도록
2024-11-22

1. get_current_user 함수

    - JWT를 검증하고 사용자 정보 추출.
    - 토큰이 없거나 잘못된 경우이면 401 에러 반환.

2. create_menu, hard_delete_menu, soft_delete_menu 권한 체크

    - 사용자 정보(current_user)에서 is_admin 확인.
    - 관리자 권한(is_admin == 1)이 없으면 403 에러를 반환.
---
---
## 코드 보완
2024-11-25
### 1. import 구문 작성 순서
표준 라이브러리 → 외부 라이브러리 → 직접 작성한 모듈

### 2. 보안 관련 코드 env 파일로 이동
보안 관련 키나 정보는 env 파일로 관리한다. 이는 민감한 정보를 코드 안에 노출하지 않고 외부 파일에서 안전하게 로드하기 위함이다.

###  3. 토큰 유효성 검사 코드 추가
토큰 검증 전, 토큰이 정상적으로 전달되었는지 확인하는 코드를 추가

### 4. 불필요한 에러 반환 코드 제거
user_id를 토큰에서 추출할 때 이미 토큰이 유효하지 않으면 예외가 발생하므로 중복되는 불필요한 예외 처리를 제거.

### 5. 불필요한 DB 접근 코드 제거
get_active_menus에서 current_user는 필요하지 않은 정보이기 때문에 제거.

---
2024-12-03
### 6. Passlib.context.CryptContext를 Argon2로 교체

passlib.context.CryptContext 대신 argon2 라이브러리로 비밀번호 해싱과 검증 처리한다.
bcrypt를 사용한 부분은 argon2로 변경해 비밀번호를 해싱하고 검증한다.
PasswordHasher 객체를 생성하고 hash 메서드로 비밀번호를 해싱해 verify 메서드로 비밀번호를 검증한다.

### 7. JWT 생성 및 검증

jose 라이브러리 대신 PyJWT를 사용하여 JWT를 생성하고 검증한다.
jwt.encode로 JWT를 인코딩하고, jwt.decode로 디코딩한다.
jose.JWTError는 PyJWT에서는 jwt.JWTError로 변경한다.
jose.JWTError 예외 처리를 jwt.ExpiredSignatureError, jwt.JWTError로 처리한다.