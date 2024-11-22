### 유저 DB table
2024-11-22

- User 모델
데이터베이스에서 사용할 유저 정보를 담은 테이블 정의.
created_at 및 updated_at으로 생성/수정 시간을 기록.


회원가입
유저 ID가 중복되었는지 확인.
비밀번호를 해싱하여 데이터베이스에 저장.
관리자 여부(is_admin)를 포함.

로그인
JWT 토큰을 생성하여 클라이언트에 반환.
비밀번호 검증.

JWT 인증
create_access_token 함수로 JWT 생성.
토큰 만료 시간을 명시적으로 관리.