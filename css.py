import streamlit as st

def layout_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        /* ĐỒNG BỘ FONT CHỮ TOÀN APP */
        html, body, [data-testid="stAppViewContainer"], .stMarkdown, p, button, span, label {
            font-family: 'Inter', sans-serif !important;
        }

        /* 1. THAY ĐỔI TOÀN BỘ NỀN (TÔNG XÁM ĐEN TRẦM - DỊU MẮT) */
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

        /* 2. SIDEBAR SANG TRỌNG */
        [data-testid="stSidebar"] {
            background-color: #070A10 !important; 
            border-right: 1px solid #1E293B !important;
            width: 280px !important;
        }

        /* 3. TỐI ƯU BẢNG DỮ LIỆU GOOGLE SHEET (DỄ NHÌN, SẠCH SẼ) */
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
        
        /* 4. THANH TÌM KIẾM TOÀN CỤC MỀM MẠI */
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

        /* 5. NÚT BẤM (SIDEBAR & TOPBAR) ĐỒNG BỘ SẮC NÉT */
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

        /* Sửa lỗi chữ đen ẩn của nút "Cấu hình bộ lọc" trên Topbar */
        [data-testid="stMainBlockContainer"] div.stButton > button {
            color: #E2E8F0 !important;
            font-size: 13px !important;
        }
        [data-testid="stMainBlockContainer"] div.stButton > button:hover {
            color: #38BDF8 !important;
        }

        /* Tiêu đề nhóm menu (Services, Tools) */
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

        /* TỐI ƯU CƠ CHẾ HIỂN THỊ ALERT/SUCCESS MẶC ĐỊNH CỦA STREAMLIT */
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

        /* =========================================================================
           ⚡ KHỐI CẬP NHẬT MỚI: GIẢI QUYẾT LỆCH HÀNG CHÊN VÊNH CỦA TOPBAR
           ========================================================================= */
        /* Ép toàn bộ các phần tử trong hàng ngang của Topbar phải thẳng tâm trục dọc */
        .topbar-wrapper [data-testid="stHorizontalBlock"] {
            align-items: center !important;
        }

        /* Triệt tiêu khoảng trống thừa vô hình bên trên ô Text Input */
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