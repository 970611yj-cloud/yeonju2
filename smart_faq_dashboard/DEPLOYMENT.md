# 🌐 대시보드 공유 및 배포 가이드

현재 보고 계신 주소(`localhost:8501`)는 고객님의 **내 컴퓨터(로컬)**에서만 접속할 수 있는 주소입니다.
다른 사람이 이 대시보드를 보려면 인터넷에 **배포(Deploy)**를 해야 합니다.

## 가장 추천하는 방법: Streamlit Community Cloud (무료)
Streamlit에서 공식적으로 제공하는 무료 호스팅 서비스입니다. 가장 간편합니다.

### 1단계: GitHub에 코드 올리기
1. [GitHub](https://github.com/)에 회원가입 후 로그인합니다.
2. 새 리포지토리(Repository)를 생성합니다. (예: `smart-faq-dashboard`)
3. 작업하신 `smart_faq_dashboard` 폴더 안의 파일들을 해당 리포지토리에 업로드합니다.
   - `app.py`, `requirements.txt`, `src/` 폴더가 필수입니다.
   - **주의**: `.env` 파일이나 API Key는 절대 올리지 마세요!

### 2단계: Streamlit Cloud 연결
1. [Streamlit Community Cloud](https://share.streamlit.io/)에 접속하여 GitHub 계정으로 로그인합니다.
2. **"New app"** 버튼을 클릭합니다.
3. 방금 만든 GitHub 리포지토리를 선택합니다.
4. **"Main file path"**에 `smart_faq_dashboard/app.py`를 입력합니다.
5. **"Deploy!"** 버튼을 누릅니다.

### 3단계: API 키 설정 (Secrets)
배포된 앱에서 AI 기능이 작동하려면 API 키를 클라우드에 알려줘야 합니다.
1. 배포된 앱 우측 하단의 **Manage app** (또는 Settings) > **Settings** > **Secrets** 메뉴로 이동합니다.
2. 아래와 같이 입력하고 저장합니다.
   ```toml
   OPENAI_API_KEY = "sk-..."
   GOOGLE_CREDENTIALS_JSON = "..."
   ```
3. 이제 생성된 링크를 다른 사람에게 공유하면 누구나 접속 가능합니다! 🎉

---

## 대안: ngrok 사용 (임시 공유)
잠깐만 보여주고 싶다면 `ngrok` 프로그램을 사용할 수 있습니다.
1. [ngrok](https://ngrok.com/) 설치 및 로그인.
2. 터미널에서 `ngrok http 8501` 입력.
3. 생성된 `https://...` 주소를 공유. (터미널 끄면 접속 불가)
