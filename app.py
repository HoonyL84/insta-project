import streamlit as st
import requests
import random
import pandas as pd
import time
import os
from dotenv import load_dotenv

# --- Load Environment Variables ---
load_dotenv()
ENV_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")

# --- Page Config ---
st.set_page_config(
    page_title="InstaDraw - Cute Comment Picker",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Cute & Simple Custom CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@300;400;500;600;700&display=swap');

    :root {
        --primary-color: #FFB7C5; /* Cherry Blossom Pink */
        --accent-color: #77DD77;  /* Pastel Green */
        --bg-color: #FFF9F9;
        --card-bg: #FFFFFF;
        --text-color: #5D5D5D;
    }

    .stApp {
        background-color: var(--bg-color);
        color: var(--text-color);
        font-family: 'Fredoka', sans-serif;
    }

    .header {
        text-align: center;
        padding: 2rem 0;
    }

    .header-title {
        font-size: 3rem;
        color: var(--primary-color);
        font-weight: 700;
        margin-bottom: 0px;
    }

    .header-subtitle {
        color: #A0A0A0;
        font-size: 1.1rem;
    }

    /* Bubbly Cards */
    .cute-card {
        background: var(--card-bg);
        border: 4px solid #FEE;
        border-radius: 30px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 20px rgba(255, 183, 197, 0.1);
    }

    /* Cute Buttons */
    .stButton>button {
        background-color: var(--primary-color);
        color: white !important;
        border: none !important;
        border-radius: 50px;
        padding: 0.8rem 2rem;
        font-weight: 600 !important;
        font-size: 1.2rem !important;
        transition: transform 0.2s;
        box-shadow: 0 5px 15px rgba(255, 183, 197, 0.4);
        width: 100%;
    }

    .stButton>button:hover {
        transform: scale(1.05);
        background-color: #FFA7B5;
    }

    /* Simple Inputs */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        border-radius: 20px !important;
        border: 2px solid #FEE !important;
        padding: 10px 20px !important;
    }

    /* Post Selection */
    .post-item {
        border-radius: 20px;
        overflow: hidden;
        border: 4px solid #FEE;
        transition: border-color 0.3s;
    }
    .post-item:hover {
        border-color: var(--primary-color);
    }

    /* Winner Display */
    .winner-box {
        background: #FFF0F3;
        border: 3px dashed var(--primary-color);
        border-radius: 25px;
        padding: 30px;
        text-align: center;
        margin-top: 20px;
    }
    
    .winner-name {
        font-size: 2.5rem;
        color: var(--primary-color);
        font-weight: 700;
        margin: 10px 0;
    }

    /* Divider */
    hr {
        border-top: 2px dashed #FEE;
    }
</style>
""", unsafe_allow_html=True)

# --- App Header ---
st.markdown("""
<div class="header">
    <div class="header-title">🌸 InstaDraw</div>
    <div class="header-subtitle">Simple & Sweet Comment Picker</div>
</div>
""", unsafe_allow_html=True)

# --- Mock Data ---
MOCK_ACCOUNTS = [
    {"name": "Lifestyle Blog", "id": "ig1", "username": "lifestyle_hoony"},
    {"name": "Tech Reviews", "id": "ig2", "username": "tech_hoony"},
]

MOCK_POSTS = {
    "ig1": [
        {"id": "p1", "media_url": "https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=500", "caption": "Cute Event Post! ✨", "timestamp": "2024-01-20"},
        {"id": "p2", "media_url": "https://images.unsplash.com/photo-1611162616305-c69b3fa7fbe0?w=500", "caption": "Sunday Vibes 🌸", "timestamp": "2024-01-21"},
    ],
    "ig2": [
        {"id": "p3", "media_url": "https://images.unsplash.com/photo-1611162618071-b39a2ad055fb?w=500", "caption": "Gadget Giveaway! 📱", "timestamp": "2024-01-22"},
    ]
}

# --- Functions ---
def get_instagram_accounts(token, mock=False):
    if mock: return MOCK_ACCOUNTS
    if not token: return []
    try:
        # 1. Get Facebook Pages
        url = f"https://graph.facebook.com/v19.0/me/accounts?access_token={token}"
        res = requests.get(url).json()
        pages = res.get('data', [])
        
        accounts = []
        for page in pages:
            page_id = page['id']
            # 2. Get linked IG account for each page
            url_ig = f"https://graph.facebook.com/v19.0/{page_id}?fields=instagram_business_account&access_token={token}"
            res_ig = requests.get(url_ig).json()
            ig_acc = res_ig.get('instagram_business_account')
            if ig_acc:
                # 3. Get IG details
                ig_id = ig_acc['id']
                url_detail = f"https://graph.facebook.com/v19.0/{ig_id}?fields=username,name&access_token={token}"
                res_detail = requests.get(url_detail).json()
                accounts.append({
                    "name": res_detail.get('name', page['name']),
                    "username": res_detail.get('username'),
                    "id": ig_id
                })
        return accounts
    except: return []

def get_posts(account_id, token, mock=False):
    if mock: return MOCK_POSTS.get(account_id, [])
    url = f"https://graph.facebook.com/v19.0/{account_id}/media?fields=id,caption,media_url,timestamp&access_token={token}"
    try:
        res = requests.get(url).json()
        return res.get('data', [])
    except: return []

# --- Main Logic ---
def main():
    if 'step' not in st.session_state: st.session_state.step = 1
    if 'selected_account' not in st.session_state: st.session_state.selected_account = None

    mock_mode = not ENV_TOKEN
    
    _, col, _ = st.columns([1, 3, 1])
    
    with col:
        # Step 1: Account Selection
        if st.session_state.step == 1:
            st.markdown('<div class="cute-card"><h3>1. 계정을 선택해 주세요 🌸</h3><p>여러 개의 인스타 계정이 연결되어 있을 수 있어요.</p></div>', unsafe_allow_html=True)
            
            accounts = get_instagram_accounts(ENV_TOKEN, mock=mock_mode)
            
            if not accounts:
                st.warning("연결된 인스타 계정을 찾을 수 없습니다.")
                if not ENV_TOKEN: st.info("토큰이 설정되지 않아 데모 모드로 동작 중입니다.")
            else:
                account_options = {f"{acc['name']} (@{acc['username']})": acc for acc in accounts}
                selected_name = st.selectbox("추첨할 계정", options=list(account_options.keys()))
                st.session_state.selected_account = account_options[selected_name]
                
                st.write("")
                if st.button("내 게시물 불러오기 ✨"):
                    st.session_state.step = 2
                    st.rerun()

        # Step 2: Post Selection
        elif st.session_state.step == 2:
            st.markdown(f'<div class="cute-card"><h3>2. 게시물을 골라주세요 ✨</h3><p>@{st.session_state.selected_account["username"]} 계정의 게시물들입니다.</p></div>', unsafe_allow_html=True)
            
            posts = get_posts(st.session_state.selected_account['id'], ENV_TOKEN, mock=mock_mode)
            
            if not posts:
                st.info("게시물이 없어요!")
                if st.button("뒤로 가기"): st.session_state.step = 1; st.rerun()
            else:
                selected_ids = []
                p_cols = st.columns(2)
                for i, post in enumerate(posts):
                    with p_cols[i % 2]:
                        st.markdown('<div class="post-item">', unsafe_allow_html=True)
                        st.image(post['media_url'], use_column_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                        if st.checkbox(f"선택하기 ({post['id'][-4:]})", key=post['id']):
                            selected_ids.append(post['id'])
                
                st.write("")
                if st.button(f"다음으로 ({len(selected_ids)}개 선택됨) ✨"):
                    if not selected_ids: st.error("하나 이상 선택해 주세요!")
                    else:
                        st.session_state.selected_posts = selected_ids
                        st.session_state.step = 3
                        st.rerun()
                if st.button("처음으로", type="secondary"): st.session_state.step = 1; st.rerun()

        # Step 3: Draw Settings
        elif st.session_state.step == 3:
            st.markdown('<div class="cute-card"><h3>3. 추첨 옵션을 정해요 🍭</h3></div>', unsafe_allow_html=True)
            
            with st.form("cute_draw"):
                keyword = st.text_input("포함할 단어 (선택)", placeholder="예: #이벤트")
                winners = st.number_input("당첨 인원", min_value=1, value=1)
                st.write("")
                submit = st.form_submit_button("두근두근 추첨 시작! 💖")
            
            if submit:
                # Mock Drawing for demo
                mock_entries = [
                    {"username": "strawberry_milk", "text": "참여합니다! #이벤트"},
                    {"username": "blue_ocean", "text": "저요저요!!"},
                    {"username": "lucky_cat", "text": "#이벤트 완료 ✨"},
                    {"username": "happy_hoony", "text": "당첨 기원 🌸"},
                ]
                
                # Simple logic for result (demo)
                res = [e for e in mock_entries if not keyword or keyword in e['text']]
                if not res: st.error("조건에 맞는 댓글이 없어요 ㅠ.ㅠ")
                else:
                    final_winners = random.sample(res, min(len(res), int(winners)))
                    st.session_state.winners = final_winners
                    st.session_state.step = 4
                    st.rerun()
            
            if st.button("게시물 다시 고르기"): st.session_state.step = 2; st.rerun()

        # Step 4: Display Winners
        elif st.session_state.step == 4:
            st.balloons()
            st.markdown('<div class="cute-card"><h2 style="text-align:center;">🎉 축하드려요! 🎉</h2></div>', unsafe_allow_html=True)
            
            for w in st.session_state.winners:
                st.markdown(f'''
                <div class="winner-box">
                    <div style="font-size: 0.9rem; color: #888;">CONGRATS!</div>
                    <div class="winner-name">@{w['username']}</div>
                    <div style="color: #555; font-style: italic;">"{w['text']}"</div>
                </div>
                ''', unsafe_allow_html=True)
            
            st.write("")
            if st.button("다시 하기 ✨"):
                st.session_state.step = 1
                st.rerun()

    st.markdown('<div style="text-align:center; padding: 2rem; color: #DDD;">🌸 InstaDraw by Hoony 🌸</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
