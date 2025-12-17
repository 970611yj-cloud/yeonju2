import pandas as pd
import os

try:
    file_path = 'faq.csv' 
    print(f"Testing file: {file_path}")
    if not os.path.exists(file_path):
        print("Error: File not found")
    if not os.path.exists(file_path):
        print("Error: File not found")
    else:
        # Try cp949 directly to see if it fixes the mojibake
        try:
             print("Attempting cp949...")
             df = pd.read_csv(file_path, encoding='cp949')
             print("Success reading with cp949")
             print(df.head())
             print(df.columns)
        except Exception as e:
             print(f"cp949 failed: {e}")
        except Exception as e:
             print(f"Other error: {e}")

except Exception as e:
    print(f"Top level error: {e}")
