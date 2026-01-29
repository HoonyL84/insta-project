# 🌸 InstaDraw 실행 가이드 (Mac 사용자용)

후니님, 맥에서 바로 테스트해보실 수 있는 명령어 모음입니다.

## 1. 프로젝트 폴더 이동
터미널을 열고 아래 명령어를 입력해 주세요.
```bash
cd "/Users/hoonyl/IdeaProjects/insta project"
```

## 2. 파일 실행 권한 부여
프로그램 실행 파일(`run_instadraw.sh`)에 실행 권한을 줍니다. (최초 1회만 수행하면 됩니다)
```bash
chmod +x run_instadraw.sh
```

## 3. 프로그램 실행
아래 명령어를 입력하면 자동으로 필요한 라이브러리를 설치하고 앱을 실행합니다.
```bash
./run_instadraw.sh
```

---

### 💡 참고 사항
*   **토큰 설정**: 시작 전 `.env` 파일을 열어 `INSTAGRAM_ACCESS_TOKEN=본인의토큰`을 입력했는지 확인해 주세요.
*   **로고 변경**: 나중에 로고 파일을 `assets/logo.png` 경로에 똑같은 이름으로 넣어주시면 화면에 바로 반영됩니다.
