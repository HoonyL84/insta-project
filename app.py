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
        --primary-color: #FFB7C5;
        --accent-color: #77DD77;
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

    .cute-card {
        background: var(--card-bg);
        border: 4px solid #FEE;
        border-radius: 30px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 20px rgba(255, 183, 197, 0.1);
    }

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

    .count-container {
        display: flex;
        gap: 15px;
        margin-bottom: 20px;
    }

    .count-box {
        flex: 1;
        text-align: center;
        background: #FFF;
        border: 2px solid #FEE;
        border-radius: 15px;
        padding: 15px;
    }

    .count-val {
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--primary-color);
    }

    .count-label {
        font-size: 0.8rem;
        color: #888;
    }

    .preview-item {
        background: #FFF9FA;
        border-radius: 12px;
        padding: 10px 15px;
        margin-bottom: 8px;
        border-left: 5px solid var(--primary-color);
    }

    .preview-user {
        font-weight: 700;
        color: var(--primary-color);
        font-size: 0.9rem;
    }

    .preview-text {
        font-size: 0.85rem;
        color: #666;
    }

    .post-item {
        border-radius: 20px;
        overflow: hidden;
        border: 4px solid #FEE;
        transition: border-color 0.3s;
    }
    .post-item:hover {
        border-color: var(--primary-color);
    }

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

MOCK_COMMENTS_POOL = [
    {"username": "strawberry_milk", "text": "참여합니다! #이벤트"},
    {"username": "blue_ocean", "text": "저요저요!!"},
    {"username": "lucky_cat", "text": "#이벤트 완료 ✨"},
    {"username": "happy_hoony", "text": "당첨 기원 🌸"},
    {"username": "sunny_day", "text": "참여 완료! #이벤트"},
    {"username": "mountain_lover", "text": "응모합니다 하하"},
]

# --- Functions ---
def get_instagram_accounts(token, mock=False):
    if mock: return MOCK_ACCOUNTS
    if not token: return []
    try:
        url = f"https://graph.facebook.com/v19.0/me/accounts?access_token={token}"
        res = requests.get(url).json()
        pages = res.get('data', [])
        accounts = [] # Fixed indentation
        for page in pages:
            url_ig = f"https://graph.facebook.com/v19.0/{page['id']}?fields=instagram_business_account&access_token={token}"
            res_ig = requests.get(url_ig).json()
            ig_acc = res_ig.get('instagram_business_account')
            if ig_acc:
                url_detail = f"https://graph.facebook.com/v19.0/{ig_acc['id']}?fields=username,name&access_token={token}"
                res_detail = requests.get(url_detail).json()
                accounts.append({
                    "name": res_detail.get('name', page['name']),
                    "username": res_detail.get('username'),
                    "id": ig_acc['id']
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

def fetch_all_comments(post_ids, token, mock=False):
    comments = []
    if mock:
        time.sleep(1)
        for _ in post_ids:
            comments.extend(random.sample(MOCK_COMMENTS_POOL, random.randint(3, 5)))
        return comments
    
    for pid in post_ids:
        url = f"https://graph.facebook.com/v19.0/{pid}/comments?fields=id,username,text&access_token={token}"
        try:
            res = requests.get(url).json()
            comments.extend(res.get('data', []))
        except: pass
    return comments

# --- Session State Initialization ---
def init_state():
    if 'step' not in st.session_state: st.session_state.step = 1
    if 'selected_account' not in st.session_state: st.session_state.selected_account = None
    if 'selected_posts' not in st.session_state: st.session_state.selected_posts = []
    if 'all_comments' not in st.session_state: st.session_state.all_comments = []
    if 'winners' not in st.session_state: st.session_state.winners = []

# --- Main Logic ---
def main():
    init_state()
    mock_mode = not ENV_TOKEN
    
    _, col, _ = st.columns([1, 2.5, 1])
    
    with col:
        # Step 1: Account Selection
        if st.session_state.step == 1:
            st.markdown('<div class="cute-card"><h3>1. 계정을 선택해 주세요 🌸</h3></div>', unsafe_allow_html=True)
            accounts = get_instagram_accounts(ENV_TOKEN, mock=mock_mode)
            if not accounts:
                st.warning("연결된 계정이 없어요!")
                if not ENV_TOKEN: st.info("토큰이 없어 데모 모드로 동작 중입니다.")
            else:
                account_options = {f"{acc['name']} (@{acc['username']})": acc for acc in accounts}
                selected_name = st.selectbox("추첨할 계정", options=list(account_options.keys()))
                st.session_state.selected_account = account_options[selected_name]
                if st.button("게시물 불러오기 ✨"):
                    st.session_state.step = 2
                    st.rerun()

        # Step 2: Post Selection
        elif st.session_state.step == 2:
            # SAFETY GUARD
            if not st.session_state.selected_account:
                st.session_state.step = 1
                st.rerun()
                
            st.markdown(f'<div class="cute-card"><h3>2. 게시물을 골라주세요 ✨</h3><p>@{st.session_state.selected_account["username"]} 계정</p></div>', unsafe_allow_html=True)
            posts = get_posts(st.session_state.selected_account['id'], ENV_TOKEN, mock=mock_mode)
            
            if not posts:
                st.info("게시물이 없습니다.")
                if st.button("← 뒤로 가기"): st.session_state.step = 1; st.rerun()
            else:
                selected_ids = []
                p_cols = st.columns(2)
                for i, post in enumerate(posts):
                    with p_cols[i % 2]:
                        st.markdown('<div class="post-item">', unsafe_allow_html=True)
                        st.image(post['media_url'], use_column_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                        if st.checkbox(f"선택 ({post['id'][-4:]})", key=post['id']):
                            selected_ids.append(post['id'])
                
                if st.button(f"댓글 불러오기 ({len(selected_ids)}개 선택됨) 🌸"):
                    if not selected_ids: st.error("게시물을 선택해 주세요!")
                    else:
                        with st.spinner("댓글 수집 중..."):
                            st.session_state.selected_posts = selected_ids
                            st.session_state.all_comments = fetch_all_comments(selected_ids, ENV_TOKEN, mock=mock_mode)
                            st.session_state.step = 3
                            st.rerun()
                if st.button("이전으로", type="secondary"): st.session_state.step = 1; st.rerun()

        # Step 3: Draw Settings & Preview
        elif st.session_state.step == 3:
            # SAFETY GUARD
            if not st.session_state.all_comments and not mock_mode:
                st.session_state.step = 2
                st.rerun()
                
            all_comments = st.session_state.all_comments
            st.markdown('<div class="cute-card"><h3>3. 추첨 대상을 확인해요 🍭</h3></div>', unsafe_allow_html=True)
            
            keyword = st.text_input("포함할 단어 (비워두면 전체)", placeholder="예: #이벤트")
            remove_duplicates = st.toggle("중복 참여 제외 (1인 1응모)", value=True)
            winners_count = st.number_input("추첨 인원", min_value=1, value=1)
            
            df_temp = pd.DataFrame(all_comments)
            if not df_temp.empty:
                if keyword:
                    df_temp = df_temp[df_temp['text'].str.contains(keyword, case=False, na=False)]
                if remove_duplicates:
                    df_temp = df_temp.drop_duplicates(subset=['username'])
                target_count = len(df_temp)
            else:
                target_count = 0
            
            st.markdown(f"""
            <div class="count-container">
                <div class="count-box">
                    <div class="count-label">전체 댓글</div>
                    <div class="count-val">{len(all_comments)}</div>
                </div>
                <div class="count-box" style="border-color: var(--primary-color);">
                    <div class="count-label">추첨 대상</div>
                    <div class="count-val">{target_count}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if target_count > 0:
                with st.expander(f"📖 추첨 대상 명단 보기 ({target_count}명)", expanded=False):
                    for idx, row in df_temp.iterrows():
                        st.markdown(f"""
                        <div class="preview-item">
                            <div class="preview-user">@{row['username']}</div>
                            <div class="preview-text">"{row['text']}"</div>
                        </div>
                        """, unsafe_allow_html=True)
            
            st.write("")
            if st.button("🎉 추첨 시작! 🎉"):
                if target_count == 0:
                    st.error("추첨 대상이 없습니다.")
                else:
                    winners = df_temp.sample(n=min(target_count, int(winners_count))).to_dict('records')
                    st.session_state.winners = winners
                    st.session_state.step = 4
                    st.rerun()
            
            if st.button("게시물 다시 고르기"): st.session_state.step = 2; st.rerun()

        # Step 4: Display Winners
        elif st.session_state.step == 4:
            # SAFETY GUARD
            if not st.session_state.winners:
                st.session_state.step = 3
                st.rerun()
                
            st.balloons()
            st.markdown('<div class="cute-card"><h2 style="text-align:center;">🎉 축하드려요! 🎉</h2></div>', unsafe_allow_html=True)
            for w in st.session_state.winners:
                st.markdown(f'''
                <div class="winner-box">
                    <div class="winner-name">@{w['username']}</div>
                    <div style="color: #555; font-style: italic;">"{w['text']}"</div>
                </div>
                ''', unsafe_allow_html=True)
            if st.button("처음으로 ✨"):
                st.session_state.step = 1
                st.rerun()

    st.markdown('<div style="text-align:center; padding: 2rem; color: #DDD;">🌸 InstaDraw by Hoony 🌸</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
