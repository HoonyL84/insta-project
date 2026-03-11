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
# Branding name from .env, fallback to "유앤쥬"
BRANDING_NAME = os.getenv("APP_BRANDING_NAME", "유앤쥬")

# Theme colors from .env, fallback to the original cute pink theme
PRIMARY_COLOR = os.getenv("APP_PRIMARY_COLOR", "#FFB7C5")
HOVER_COLOR = os.getenv("APP_HOVER_COLOR", "#FFA7B5")
BG_COLOR = os.getenv("APP_BG_COLOR", "#FFF9F9")

# Emoji branding from .env
APP_EMOJI = os.getenv("APP_EMOJI", "🌸")

# --- Page Config ---
st.set_page_config(
    page_title=f"{BRANDING_NAME} - 인스타 추첨기",
    page_icon=APP_EMOJI,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Cute & Simple Custom CSS ---
# Use format() or f-string carefully. We use single braces f-string for python vars and double {{}} for CSS blocks.
css_code = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght=300;400;500;600;700&display=swap');

    :root {{
        --primary-color: {PRIMARY_COLOR};
        --accent-hover: {HOVER_COLOR};
        --bg-color: {BG_COLOR};
        --card-bg: #FFFFFF;
        --text-color: #5D5D5D;
    }}

    .stApp {{
        background-color: var(--bg-color);
        color: var(--text-color);
        font-family: 'Fredoka', sans-serif;
    }}

    .header {{
        text-align: center;
        padding: 1.5rem 0;
    }}

    .header-title {{
        font-size: 2.5rem;
        color: var(--primary-color);
        font-weight: 700;
        margin-bottom: 0px;
    }}

    .header-subtitle {{
        color: #A0A0A0;
        font-size: 1rem;
    }}

    .cute-card {{
        background: var(--card-bg);
        border: 4px solid #FEE;
        border-radius: 30px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 20px rgba(255, 183, 197, 0.1);
    }}

    .stButton>button {{
        background-color: var(--primary-color);
        color: white !important;
        border: none !important;
        border-radius: 50px;
        padding: 0.6rem 1.5rem;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        transition: transform 0.2s;
        box-shadow: 0 5px 15px rgba(255, 183, 197, 0.4);
        width: 100%;
    }}

    .stButton>button:hover {{
        transform: scale(1.05);
        background-color: var(--accent-hover);
    }}

    /* --- GHOST INTERACTION LAYER --- */
    .post-wrapper .element-container:has(div[data-testid="stCheckbox"]) {{
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 100% !important;
        z-index: 10 !important;
        padding: 0 !important;
        margin: 0 !important;
    }}

    .post-wrapper div[data-testid="stCheckbox"] {{
        width: 100% !important;
        height: 100% !important;
        padding: 0 !important;
        margin: 0 !important;
    }}

    .post-wrapper div[data-testid="stCheckbox"] * {{
        opacity: 0 !important;
        visibility: hidden !important;
        pointer-events: none !important;
        height: 0 !important;
        width: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }}

    .post-wrapper div[data-testid="stCheckbox"] label {{
        display: block !important;
        opacity: 0 !important;
        visibility: visible !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 100% !important;
        padding: 0 !important;
        margin: 0 !important;
        pointer-events: auto !important;
        cursor: pointer !important;
        z-index: 100 !important;
    }}

    /* Post Card Styling */
    .post-wrapper {{
        position: relative;
        margin-bottom: 25px;
        transition: transform 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }}
    .post-wrapper:hover {{
        transform: translateY(-5px);
    }}

    .insta-post {{
        background: white;
        border: 2px solid #EFEFEF;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        position: relative;
        z-index: 1;
    }}
    
    .selected .insta-post {{
        border-color: var(--primary-color);
        box-shadow: 0 0 0 4px rgba(255, 183, 197, 0.3);
    }}

    .insta-header {{
        display: flex;
        align-items: center;
        padding: 8px 10px;
        border-bottom: 1px solid #FAFAFA;
    }}
    .insta-avatar {{
        width: 24px;
        height: 24px;
        border-radius: 50%;
        background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%);
        margin-right: 8px;
        padding: 1.5px;
    }}
    .insta-avatar-inner {{
        width: 100%;
        height: 100%;
        background: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 10px;
        font-weight: bold;
        color: #FFB7C5;
    }}
    .insta-username {{
        font-weight: 600;
        font-size: 12px;
        color: #262626;
    }}

    .insta-img-wrapper {{
        aspect-ratio: 1/1;
        overflow: hidden;
        background: #FAFAFA;
        position: relative;
    }}
    .insta-img-wrapper img {{
        width: 100% !important;
        height: 100% !important;
        object-fit: cover !important;
    }}

    .selection-overlay {{
        position: absolute;
        top: 10px;
        right: 10px;
        background: var(--primary-color);
        color: white;
        width: 26px;
        height: 26px;
        border-radius: 50%;
        display: none;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2);
        z-index: 5;
        border: 2px solid white;
    }}
    .selected .selection-overlay {{
        display: flex;
    }}

    /* Other UI Elements */
    .count-container {{
        display: flex;
        gap: 15px;
        margin-bottom: 20px;
    }}
    .count-box {{
        flex: 1;
        text-align: center;
        background: #FFF;
        border: 2px solid #FEE;
        border-radius: 15px;
        padding: 15px;
    }}
    .count-val {{
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--primary-color);
    }}

    .preview-item {{
        background: #FFF9FA;
        border-radius: 12px;
        padding: 10px 15px;
        margin-bottom: 8px;
        border-left: 5px solid var(--primary-color);
        text-align: left;
    }}
    .preview-user {{ font-weight: 600; color: var(--primary-color); font-size: 0.9rem; }}
    .preview-text {{ color: #555; font-size: 0.85rem; margin-top: 2px; }}

    .winner-box {{
        background: white;
        border: 3px dashed var(--primary-color);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 15px;
        text-align: center;
    }}
    .winner-name {{
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--primary-color);
        margin-bottom: 5px;
    }}
</style>
"""
st.markdown(css_code, unsafe_allow_html=True)

# --- App Header ---
st.markdown(f"""
<div class="header">
    <div class="header-title">{APP_EMOJI} {BRANDING_NAME}</div>
    <div class="header-subtitle">인스타 추첨 이벤트</div>
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
        {"id": "p4", "media_url": "https://images.unsplash.com/photo-1611162616475-46b635cb6868?w=500", "caption": "Coffee Time ☕", "timestamp": "2024-01-22"},
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
        accounts = []
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
    if 'checkbox_values' not in st.session_state: st.session_state.checkbox_values = {}

# --- Main Logic ---
def main():
    init_state()
    mock_mode = not ENV_TOKEN
    
    _, col, _ = st.columns([1, 2.5, 1])
    
    with col:
        # Step 1: Account Selection
        if st.session_state.step == 1:
            st.markdown(f'<div class="cute-card"><h3>1. 계정을 선택해 주세요 {APP_EMOJI}</h3></div>', unsafe_allow_html=True)
            accounts = get_instagram_accounts(ENV_TOKEN, mock=mock_mode)
            if not accounts:
                st.warning("연결된 계정이 없어요!")
            else:
                account_options = {f"{acc['name']} (@{acc['username']})": acc for acc in accounts}
                selected_name = st.selectbox("추첨할 계정", options=list(account_options.keys()))
                st.session_state.selected_account = account_options[selected_name]
                if st.button("내 게시물 불러오기 ✨"):
                    st.session_state.step = 2
                    st.rerun()

        # Step 2: Post Selection
        elif st.session_state.step == 2:
            if not st.session_state.selected_account:
                st.session_state.step = 1
                st.rerun()
                
            st.markdown(f'<div class="cute-card"><h3 style="margin-bottom:5px;">2. 게시물을 터치해서 선택하세요 ✨</h3><p style="font-size:0.9rem; text-align:center; color:#888;">@{st.session_state.selected_account["username"]} 계정</p></div>', unsafe_allow_html=True)
            posts = get_posts(st.session_state.selected_account['id'], ENV_TOKEN, mock=mock_mode)
            
            if not posts:
                st.info("게시물이 없습니다.")
                if st.button("← 뒤로 가기"): st.session_state.step = 1; st.rerun()
            else:
                p_cols = st.columns(3)
                selected_ids = []
                
                for i, post in enumerate(posts):
                    with p_cols[i % 3]:
                        is_checked = st.session_state.checkbox_values.get(post['id'], False)
                        selected_class = "selected" if is_checked else ""
                        avatar_init = BRANDING_NAME[0].upper() if BRANDING_NAME else 'U'
                        
                        st.markdown(f"""
                        <div class="post-wrapper {selected_class}">
                            <div class="insta-post">
                                <div class="insta-header">
                                    <div class="insta-avatar"><div class="insta-avatar-inner">{avatar_init}</div></div>
                                    <div class="insta-username">{st.session_state.selected_account['username']}</div>
                                </div>
                                <div class="insta-img-wrapper">
                                    <img src="{post['media_url']}">
                                    <div class="selection-overlay">✔</div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # The Ghost Checkbox
                        val = st.checkbox(" ", value=is_checked, key=f"sel_{post['id']}")
                        if val != is_checked:
                            st.session_state.checkbox_values[post['id']] = val
                            st.rerun()
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                        if val:
                            selected_ids.append(post['id'])
                
                st.write("")
                count = len(selected_ids)
                if st.button(f"다음 단계로 ({count}개 선택됨) {APP_EMOJI}"):
                    if count == 0: st.error("게시물을 최소 하나는 선택해 주세요!")
                    else:
                        with st.spinner("댓글 수집 중..."):
                            st.session_state.selected_posts = selected_ids
                            st.session_state.all_comments = fetch_all_comments(selected_ids, ENV_TOKEN, mock=mock_mode)
                            st.session_state.step = 3
                            st.rerun()
                if st.button("계정 다시 선택", type="secondary"): 
                    st.session_state.checkbox_values = {}
                    st.session_state.step = 1
                    st.rerun()

        # Step 3: Draw Settings & Preview
        elif st.session_state.step == 3:
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
                st.session_state.checkbox_values = {}
                st.session_state.step = 1
                st.rerun()

    st.markdown(f'<div style="text-align:center; padding: 2rem; color: #DDD;">{APP_EMOJI} {BRANDING_NAME} with Hoony {APP_EMOJI}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
