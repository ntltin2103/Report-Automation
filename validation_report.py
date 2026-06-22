import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import streamlit as st

# Định nghĩa quyền truy cập
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

@st.cache_data(ttl=600)
def get_google_sheet_data(spreadsheet_name):
    try:
        # THAY ĐỔI Ở ĐÂY: Dùng từ khóa từ hệ thống Secrets của Streamlit
        # giúp code chạy được cả trên mạng lẫn dưới máy (nếu cấu hình file .streamlit/secrets.toml)
        creds_dict = st.secrets["gcp_service_account"]
        
        # Sử dụng hàm from_json_keyfile_dict thay vì file name
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, SCOPE)
        client = gspread.authorize(creds)
        
        sheet = client.open(spreadsheet_name).sheet1
        data = sheet.get_all_records()
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Lỗi kết nối dữ liệu: {e}")
        return pd.DataFrame()

# --- Gọi hàm hiển thị bảng dữ liệu ---
df = get_google_sheet_data("GS connector")
if not df.empty:
    st.dataframe(df, use_container_width=True)