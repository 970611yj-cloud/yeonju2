# 스마트 FAQ & AI 요약 대시보드

상담원이 고객 문의를 빠르고 정확하게 처리할 수 있도록 돕는 AI 기반 대시보드입니다.

## 🚀 시작하기

### 1. 설치
터미널에서 다음 명령어를 실행하여 필요한 라이브러리를 설치합니다.
```bash
python -m pip install -r requirements.txt
```

### 2. 실행
```bash
streamlit run app.py
```
> **참고**: `smart_faq_dashboard` 폴더 내에서 실행하거나 `streamlit run smart_faq_dashboard/app.py`로 실행하세요.

### 3. 설정 (프로덕션 환경)
`.env.example` 파일을 복사하여 `.env`로 이름을 변경하고 API 키를 입력하세요.
- **GOOGLE_SHEET_URL**: 데이터를 불러올 구글 시트 주소
- **GOOGLE_KEY_FILE**: 구글 서비스 계정 JSON 키 파일 경로
- **OPENAI_API_KEY**: AI 답변 생성을 위한 OpenAI 키

## 📊 데이터 시트 구조 (Google Sheets)
구글 시트는 다음과 같은 컬럼 헤더를 가져야 합니다:
| Product | Model | Tags | Manual | Question | Answer |
|---------|-------|------|--------|----------|--------|
| 상품명   | 모델명 | 키워드| 매뉴얼 전문| 질문 | 답변 |

## 🛠 기능 설명
- **검색**: 상품명이나 증상을 입력하면 유사한 내용을 찾아줍니다. (예: '와이파이' -> 'WiFi' 검색 가능)
- **AI 답변**: [Generate AI Answer] 버튼을 누르면 매뉴얼을 분석해 답변을 요약해줍니다.
- **SMS 전송**: 답변 내용을 고객에게 문자로 보낼 수 있습니다. (현재는 시뮬레이션 모드)
