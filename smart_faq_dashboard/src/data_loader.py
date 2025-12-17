import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import os
import json

# Define the scope
SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

def read_csv_robust(file_path_or_buffer):
    """
    Reads CSV with robust encoding handling (utf-8-sig > cp949).
    """
    encodings = ['utf-8-sig', 'cp949', 'euc-kr']
    for enc in encodings:
        try:
            if hasattr(file_path_or_buffer, 'seek'):
                file_path_or_buffer.seek(0)
            df = pd.read_csv(file_path_or_buffer, encoding=enc)
            return df
        except UnicodeDecodeError:
            continue
        except Exception:
            continue
    raise ValueError("Failed to read CSV with supported encodings.")

@st.cache_data(ttl=600)  # Cache for 10 minutes to avoid hitting API limits
def load_data(sheet_url, csv_file=None):
    """
    Loads data from CSV if provided, else Google Sheets, else Mock data.
    """
    df = None
    source_name = ""

    # Priority 1: Uploaded CSV via Streamlit Uploader
    if csv_file is not None:
        try:
            df = read_csv_robust(csv_file)
            source_name = "Uploaded CSV"
        except Exception as e:
            st.error(f"업로드된 CSV 파일 로드 오류: {e}")

    # Priority 2: Local Default CSV (faq.csv)
    if df is None:
        base_path = os.path.dirname(os.path.dirname(__file__)) # Go up from src/ to root
        default_csv_path = os.path.join(base_path, 'faq.csv')
        
        if os.path.exists(default_csv_path):
            try:
                df = read_csv_robust(default_csv_path)
                source_name = "faq.csv (Local)"
            except Exception as e:
                print(f"Default CSV load error: {e}")
    
    # Common Processing for CSVs
    if df is not None:
        try:
            # Clean column names (strip whitespace)
            df.columns = df.columns.str.strip()
            
            # Handle hidden/empty columns (Unnamed: X)
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
            
            # Ensure compatibility: Add missing columns if they don't exist
            expected_cols = ['Tags', 'Manual'] 
            for col in expected_cols:
                if col not in df.columns:
                    df[col] = "" 
            
            return df
        except Exception as e:
             st.error(f"데이터 처리 중 오류 ({source_name}): {e}")

    # Priority 3: Google Sheets
    if "GOOGLE_KEY_FILE" in os.environ:
         creds_file = os.environ["GOOGLE_KEY_FILE"] # Path to json file
         creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, SCOPE)
    elif "GOOGLE_CREDENTIALS_JSON" in getattr(st, "secrets", {}):
         # Support Streamlit secrets for deployment
         creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS_JSON"])
         creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, SCOPE)
    else:
        creds = None
        # Fallback for local dev without env var set (Mock Mode if needed, or error)
        # For now, let's return a mock dataframe if no creds are found to allow UI dev
        print("Warning: No Google Credentials found. Using mock data.")
        return _get_mock_data()

    try:
        client = gspread.authorize(creds)
        sheet = client.open_by_url(sheet_url).sheet1
        data = sheet.get_all_records()
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        st.error(f"Error loading Google Sheet: {e}")
        return _get_mock_data()

def _get_mock_data():
    """Returns mock data for testing/demo purposes."""
    data = {
        'Product': ['스마트 공기청정기 X1', '로봇청소기 R5', '스마트 공기청정기 X1'],
        'Model': ['SAP-X1', 'RV-R5', 'SAP-X1'],
        'Tags': ['필터, 소음, 전원', '배터리, 지도, 센서', '와이파이, 앱, 연결'],
        'Manual': [
            'SAP-X1 모델은 헤파 13등급 필터를 사용합니다. 교체 주기는 6개월입니다. 수면 모드 시 소음은 30dB입니다.',
            '첫 사용 전 4시간 충전이 필요합니다. LiDAR 센서를 사용하여 지도를 생성합니다.',
            '2.4GHz 와이파이만 지원합니다. SmartHome 앱을 통해 제어할 수 있습니다.'
        ],
        'Question': [
            '필터 교체는 어떻게 하나요?',
            '로봇청소기가 지도를 그리지 않아요.',
            '와이파이 연결이 안 돼요.'
        ],
        'Answer': [
            '후면 커버를 열고 기존 필터의 탭을 당겨 제거한 후, 새 필터를 "딸각" 소리가 날 때까지 밀어 넣어주세요.',
            '상단 LiDAR 센서가 가려져 있지 않은지 확인해주세요. 설정에서 지도를 초기화한 후 다시 시도해주세요.',
            '5GHz 와이파이가 아닌 2.4GHz 와이파이에 연결되어 있는지 확인해주세요. 기기의 전원 버튼을 5초간 눌러 와이파이를 초기화하세요.'
        ]
    }
    return pd.DataFrame(data)
