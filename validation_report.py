import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd  
import streamlit as st

# Định nghĩa quyền truy cập
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

creds_file = "credentials.json"

@st.cache_data(ttl=300)
def get_google_sheet_data(spreadsheet_name):
    """
    Hàm kết nối Google Sheet và trả về một Pandas DataFrame.
    """
    try:
        # Xác thực tài khoản
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
        client = gspread.authorize(creds)
        
        # Mở bảng tính và lấy sheet đầu tiên (sheet1)
        sheet = client.open(spreadsheet_name).sheet1
        
        # Đọc dữ liệu thành danh sách dictionary
        data = sheet.get_all_records()
        
        # Chuyển thành DataFrame của Pandas
        df = pd.DataFrame(data)
        return df
        
    except gspread.exceptions.SpreadsheetNotFound:
        st.error(f"❌ Không tìm thấy file Google Sheet có tên: '{spreadsheet_name}'")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Đã xảy ra lỗi khi kết nối: {e}")
        return pd.DataFrame()
    
