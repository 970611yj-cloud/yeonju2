from openai import OpenAI
import streamlit as st
import os

def generate_ai_summary(context_text, query, api_key=None):
    """
    Generates an AI summary based on the provided context (Manual + FAQ) and the user query.
    """
    if not api_key:
        # Fallback to env or secrets if not provided explicitly
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            api_key = st.secrets.get("OPENAI_API_KEY")

    if not api_key:
        return "⚠️ OpenAI API Key가 없습니다. 설정 메뉴에서 키를 입력해주세요."

    client = OpenAI(api_key=api_key)

    system_prompt = """
    당신은 친절하고 전문적인 제품 상담 도우미입니다.
    제공된 [Context]를 바탕으로 사용자의 [Query]에 답변하세요.
    - 답변이 문맥(Context)에 있다면, 명확하고 정중하게 요약하여 답변하세요(최대 3문장).
    - 답변을 찾을 수 없다면 "제공된 정보에는 해당 내용이 없습니다."라고 말하세요.
    - 없는 사실을 지어내지 마세요(Hallucination 방지).
    - 어조: 전문적임, 친절함, 간결함.
    """
    
    user_message = f"""
    [Context]:
    {context_text}
    
    [Query]:
    {query}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # Or gpt-3.5-turbo if cost is a concern
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.3, # Low temperature for factual consistency
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error generating AI summary: {str(e)}"
