#!/bin/bash
echo "🌸 InstaDraw를 실행합니다..."

# 1. 가상환경 체크 및 생성
if [ ! -d "venv" ]; then
    echo "📦 가상환경을 생성하는 중 (최초 1회)..."
    python3 -m venv venv
fi

# 2. 패키지 설치
source venv/bin/activate
echo "🔧 필요한 라이브러리를 설치하는 중..."
pip install -r requirements.txt --quiet

# 3. 앱 실행
echo "🚀 앱을 시작합니다! 잠시만 기다려주세요..."
streamlit run app.py
