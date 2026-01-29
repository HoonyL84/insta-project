# 🌸 유앤쥬 인스타 추첨기 가이드

유앤쥬 전용 인스타 추첨 이벤트 도구입니다. 이 가이드는 프로그램 설치부터 실행까지의 과정을 담고 있습니다.

---

## 🚀 1. 준비 사항 (Python 설치)

이 프로그램을 실행하려면 컴퓨터에 **Python(파이썬)**이 설치되어 있어야 합니다.

### 🪟 Windows 사용자
1. [Python 공식 홈페이지](https://www.python.org/downloads/windows/)에 접속합니다.
2. **Download Windows installer (64-bit)**를 클릭하여 설치 파일을 다운로드합니다.
3. **중요!** 설치 시작 화면 하단의 **[Add Python to PATH]** 체크박스를 반드시 선택하고 [Install Now]를 누르세요.

### 🍎 Mac 사용자
1. 터미널(Terminal) 앱을 엽니다.
2. 아래 명령어를 입력하여 파이썬 설치 여부를 확인합니다:
   ```bash
   python3 --version
   ```
3. 설치되어 있지 않다면, [Python 공식 홈페이지](https://www.python.org/downloads/macos/)에서 최신 버전을 다운로드하여 설치하세요. (혹은 터미널에서 `brew install python`으로 설치 가능)

---

## ⚙️ 2. 설정 (환경 변수)

프로젝트 폴더에 있는 `.env` 파일을 메모장이나 텍스트 편집기로 열어 아래 내용을 수정해 주세요.

```env
# 인스타그램 API 토큰 (필수)
INSTAGRAM_ACCESS_TOKEN=본인의_토큰_입력

# 앱 브랜딩 이름 (선택 - 기본값: 유앤쥬)
APP_BRANDING_NAME=유앤쥬
```

---

## 🏃‍♂️ 3. 실행 방법 (One-Click)

### 🪟 Windows 사용자
- 폴더 안에 있는 **`run_instadraw.bat`** 파일을 마우스로 더블 클릭합니다.
- 최초 실행 시 필요한 라이브러리를 자동으로 설치한 후 웹 브라우저가 열립니다.

### 🍎 Mac 사용자
1. 터미널을 열고 프로젝트 폴더로 이동합니다:
   ```bash
   cd "/Users/hoonyl/IdeaProjects/insta project"
   ```
2. 실행 권한을 부여합니다 (최초 1회):
   ```bash
   chmod +x run_instadraw.sh
   ```
3. 프로그램을 실행합니다:
   ```bash
   ./run_instadraw.sh
   ```

---

## ✨ 주요 기능
- **인스타 감성 UI**: 인스타그램 피드 스타일의 게시물 선택 화면
- **간편한 선택**: 게시물 이미지를 터치(클릭)하여 즉시 선택/해제
- **중복 제외 추첨**: 한 명의 사용자가 여러 번 댓글을 달아도 한 번만 응모되도록 설정 가능
- **실시간 명단 확인**: 추첨 전 응모자 명단을 미리 확인 가능

---
🌸 **유앤쥬** with Hoony
