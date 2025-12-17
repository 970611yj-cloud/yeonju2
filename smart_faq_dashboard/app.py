import streamlit as st
import pandas as pd
import time
from dotenv import load_dotenv
import os

# Load modules
from src.data_loader import load_data
from src.search_engine import smart_search, get_suggestion
from src.llm_engine import generate_ai_summary
from src.sms_sender import send_sms

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Smart FAQ Dashboard",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for "Google Style" simple search
st.markdown("""
<style>
    .stTextInput > div > div > input {
        border-radius: 24px;
        padding: 10px 20px;
        border: 1px solid #dfe1e5;
        box-shadow: 0 1px 6px rgba(32,33,36,0.28);
    }
    .stTextInput > div > div > input:focus {
        border: 1px solid #dfe1e5;
        outline: none;
        box-shadow: 0 1px 6px rgba(32,33,36,0.28);
    }
    .search-container {
        display: flex;
        justify_content: center;
        padding-top: 50px;
        padding-bottom: 30px;
    }
    .result-card {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        border: 1px solid #e0e0e0;
        cursor: pointer;
    }
    .result-card:hover {
        background-color: #f1f3f4;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align: center; color: #444;'>스마트 FAQ 및 AI 상담 도우미</h1>", unsafe_allow_html=True)

# 1. Sidebar & Data Loading
with st.sidebar:
    st.header("⚙️ 설정")
    
    # API Key Input
    api_key_input = st.text_input("OpenAI API Key 입력", type="password", placeholder="sk-...")
    if api_key_input:
        os.environ["OPENAI_API_KEY"] = api_key_input # Set for this session
    
    uploaded_file = st.file_uploader("CSV 파일 업로드 (데이터 덮어쓰기)", type=["csv"])
    if uploaded_file:
        st.info("✅ CSV 파일 사용 중")
    else:
        st.info("ℹ️ 기본/구글 시트 사용 중")
        
    st.divider()
    
    # Deployment/Sharing Info
    with st.expander("🌐 공유하는 법 (배포)"):
        st.markdown("""
        이 링크는 **로컬(내 컴퓨터)**에서만 작동합니다.
        다른 사람에게 공유하려면 **배포**가 필요합니다.
        
        [배포 가이드 보기](https://share.streamlit.io/)
        """)
        
    st.markdown("Developed by Antigravity")

# Placeholder URL - Replace with actual Google Sheet URL from env or input
GOOGLE_SHEET_URL = os.environ.get("GOOGLE_SHEET_URL", "dummy_url")
df = load_data(GOOGLE_SHEET_URL, uploaded_file)

# 2. Search Bar
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    query = st.text_input("", placeholder="상품 이슈, 매뉴얼, 키워드 등을 검색하세요...", label_visibility="collapsed")

# 3. Search Logic & Display
if query:
    results_df = smart_search(df, query)
    
    if not results_df.empty:
        st.write(f"🔍 '**{query}**'에 대한 검색 결과 {len(results_df)}건")
        
        # Group by Product to show product-level cards initially? 
        # Or just show specific FAQ matches. Request asks for "Search Result Click -> Modal".
        # Let's list unique Products found or individual FAQ items.
        # Given the "Product -> N FAQs" structure, maybe we show the relevant FAQ item directly.
        
        for index, row in results_df.iterrows():
            with st.container():
                # Streamlit doesn't support native modals perfectly locally without extra libs, 
                # but 'st.expander' or 'st.popover' (newer versions) work well.
                # Let's use st.expander for details.
                label = f"**[{row['Product']}]** {row['Question']} ({row['score']}%)"
                with st.expander(label):
                    st.markdown("### 🤖 AI 요약 답변")
                    
                    # Call LLM on demand to save tokens, or have a button? 
                    # Request says "AI Summary Section... real-time summary".
                    # Let's create a placeholder for the summary to load it async-ish or just run it.
                    context = f"Product: {row['Product']}\nFAQ Answer: {row['Answer']}"
                    if row['Manual']:
                         context += f"\nManual: {row['Manual']}"
                    
                    if st.button("AI 답변 생성", key=f"btn_ai_{index}"):
                        with st.spinner("AI가 답변을 요약 중입니다..."):
                            # Use input key or env key
                            current_api_key = api_key_input if api_key_input else os.environ.get("OPENAI_API_KEY")
                            ai_answer = generate_ai_summary(context, query, current_api_key)
                            st.info(ai_answer)
                            st.code(ai_answer, language="text") # Easy copy
                    
                    st.divider()
                    
                    st.markdown("### 📄 기존 매뉴얼/FAQ 답변")
                    st.write(row['Answer'])
                    st.code(row['Answer'], language="text") # Easy copy
                    
                    st.divider()
                    
                    st.markdown("### 💬 문자(SMS) 전송")
                    c_sms1, c_sms2 = st.columns([3, 1])
                    with c_sms1:
                        phone = st.text_input("고객 전화번호", key=f"phone_{index}", placeholder="01012345678")
                    with c_sms2:
                        # We need to decide WHAT to send. Let's send the FAQ answer by default.
                        msg_to_send = row['Answer'] 
                        if st.button("전송", key=f"btn_sms_{index}"):
                            success, resp = send_sms(phone, msg_to_send)
                            if success:
                                st.toast(f"✅ 발송 성공: {resp}")
                            else:
                                st.error(f"❌ 발송 실패: {resp}")

    else:
        # No results, try suggestion
        suggestion = get_suggestion(df, query)
        if suggestion:
            st.warning(f"검색 결과가 없습니다. 혹시 '**{suggestion}**'을(를) 찾으시나요?")
            if st.button(f"'{suggestion}'(으)로 검색하기"):
                # Rerun search with suggestion
                results_df = smart_search(df, suggestion)
                st.write(f"🔍 '**{suggestion}**'에 대한 검색 결과 {len(results_df)}건")
                for index, row in results_df.iterrows():
                     with st.container():
                        label = f"**[{row['Product']}]** {row['Question']} ({row['score']}%)"
                        with st.expander(label):
                            st.markdown("### 🤖 AI 요약 답변")
                            context = f"Product: {row['Product']}\nFAQ Answer: {row['Answer']}"
                            if 'Manual' in row and row['Manual']:
                                 context += f"\nManual: {row['Manual']}"
                            
                            if st.button("AI 답변 생성", key=f"btn_ai_s_{index}"):
                                with st.spinner("AI가 답변을 요약 중입니다..."):
                                    current_api_key = api_key_input if api_key_input else os.environ.get("OPENAI_API_KEY")
                                    ai_answer = generate_ai_summary(context, suggestion, current_api_key)
                                    st.info(ai_answer)
                            
                            st.divider()
                            st.markdown("### 📄 기존 매뉴얼/FAQ 답변")
                            st.write(row['Answer'])
                            st.divider()
                            st.markdown("### 💬 문자(SMS) 전송")
                            c_sms1, c_sms2 = st.columns([3, 1])
                            with c_sms1:
                                phone = st.text_input("고객 전화번호", key=f"phone_s_{index}", placeholder="01012345678")
                            with c_sms2:
                                msg_to_send = row['Answer'] 
                                if st.button("전송", key=f"btn_sms_s_{index}"):
                                    success, resp = send_sms(phone, msg_to_send)
                                    if success:
                                        st.toast(f"✅ 발송 성공: {resp}")
        else:
            st.warning("검색 결과가 없습니다. 다른 키워드로 검색해보세요.")
else:
    # Landing State
    st.markdown("<div style='text-align: center; color: #888; margin-top: 50px;'>위 검색창에 키워드를 입력하세요.</div>", unsafe_allow_html=True)
