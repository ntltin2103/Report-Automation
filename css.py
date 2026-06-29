import streamlit as st

def layout_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        /* Font dùng chung cho toàn bộ giao diện */
        html, body, [data-testid="stAppViewContainer"], p, h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif !important;
        }

        /* Font cho nội dung văn bản */
        .stMarkdown div p, .stMarkdown span:not([class*="material"]) {
            font-family: 'Inter', sans-serif !important;
        }

        /* Font cho nút bấm */
        div.stButton > button div p, div.stButton > button {
            font-family: 'Inter', sans-serif !important;
        }

        /* Màu nền chung của app */
        [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background-color: #0B0F17 !important; 
            color: #E2E8F0 !important;
        }
        
        /* Tối ưu không gian thở vùng nội dung chính */
        [data-testid="stMainBlockContainer"] {
            padding: 2rem 4rem !important;
        }

        /* ĐỒNG BỘ MÀU CHỮ TIÊU ĐỀ TRÊN TOPBAR (SỬA LỖI CHỮ ĐEN) */
        h3, [data-testid="stMarkdown"] h3 {
            color: #F8FAFC !important;
            font-weight: 600 !important;
        }

        /* Thanh menu bên trái */
        [data-testid="stSidebar"] {
            background-color: #070A10 !important; 
            border-right: 1px solid #1E293B !important;
            width: 280px !important;
        }

        /* Bảng dữ liệu */
        [data-testid="stDataFrame"] {
            background-color: #111827 !important;
            border: 1px solid #1F2937 !important;
            border-radius: 12px !important;
            padding: 6px !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }

        /* Tối ưu header của bảng dữ liệu Streamlit */
        [data-testid="stDataFrame"] data-styled-table-container {
            border-radius: 8px !important;
        }
        
        /* Ô tìm kiếm */
        .stTextInput input {
            background-color: #111827 !important;
            color: #F3F4F6 !important;
            border-radius: 10px !important;
            border: 1px solid #1F2937 !important;
            padding: 10px 16px !important;
            transition: all 0.2s ease !important;
        }
        .stTextInput input:focus {
            border-color: #38BDF8 !important; 
            box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.1) !important;
        }

        /* Nút bấm */
        div.stButton > button {
            background-color: #111827 !important; 
            color: #9CA3AF !important; 
            border: 1px solid #1F2937 !important; 
            border-radius: 10px !important;
            width: 100% !important;
            font-weight: 500 !important;
            padding: 10px 16px !important;
            transition: all 0.2s ease !important;
        }
        
        /* Hover mượt mà phản hồi cao cấp */
        div.stButton > button:hover {
            color: #38BDF8 !important; 
            border-color: #38BDF8 !important;
            background-color: #1F2937 !important;
            box-shadow: 0 4px 12px rgba(56, 189, 248, 0.1) !important;
        }

        /* Màu chữ cho nút trên thanh đầu trang */
        [data-testid="stMainBlockContainer"] div.stButton > button {
            color: #E2E8F0 !important;
            font-size: 13px !important;
        }
        [data-testid="stMainBlockContainer"] div.stButton > button:hover {
            color: #38BDF8 !important;
        }

        /* Tiêu đề nhóm menu */
        .stMarkdown h3 {
            font-size: 11px !important;
            text-transform: uppercase !important;
            letter-spacing: 0.08em !important;
            color: #4B5563 !important;
            margin-top: 1.8rem !important;
            margin-bottom: 0.6rem !important;
        }
        
        hr {
            border-color: #1F2937 !important;
            margin: 1.5rem 0 !important;
        }

        /* Cách hiển thị thông báo */
        [data-testid="stNotification"] {
            background-color: rgba(16, 185, 129, 0.08) !important;
            border: 1px solid rgba(16, 185, 129, 0.2) !important;
            color: #10B981 !important;
            border-radius: 10px !important;
        }
        [data-testid="stNotification"] p {
            color: #10B981 !important;
            font-weight: 500 !important;
            font-size: 13px !important;
        }

        /* Căn chỉnh phần đầu trang */
        .topbar-wrapper [data-testid="stHorizontalBlock"] {
            align-items: center !important;
        }

        /* Giảm khoảng cách trên ô nhập */
        .fixed-search-input [data-testid="stWidgetLabel"] {
            display: none !important;
        }
        .fixed-search-input div[data-testid="stTextInput"] {
            margin-top: 0 !important;
            margin-bottom: 0 !important;
            padding-top: 0 !important;
            padding-bottom: 0 !important;
        }
    </style>
    """, unsafe_allow_html=True)