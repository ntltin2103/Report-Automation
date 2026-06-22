import streamlit as st

def layout_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
        
        /* ĐỒNG BỘ FONT CHỮ TOÀN APP */
        html, body, [data-testid="stAppViewContainer"], .stMarkdown, p, button {
            font-family: 'Inter', sans-serif !important;
        }

        /* 1. THAY ĐỔI TOÀN BỘ NỀN (TÔNG XÁM ĐEN TRẦM - DỊU MẮT) */
        [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background-color: #0B0F17 !important; /* Màu xanh đen trầm, giảm mỏi mắt tuyệt đối */
            color: #E2E8F0 !important;
        }
        
        /* Vùng chứa nội dung chính cần có thêm không gian thở */
        [data-testid="stMainBlockContainer"] {
            padding: 3rem 5rem !important;
        }

        /* 2. SIDEBAR SANG TRỌNG */
        [data-testid="stSidebar"] {
            background-color: #070A10 !important; /* Tối hơn nền chính một tone để tạo chiều sâu */
            border-right: 1px solid #1E293B !important;
            width: 280px !important;
        }

        /* 3. ĐẶC BIỆT: TỐI ƯU BẢNG DỮ LIỆU (st.dataframe) ĐỂ DỄ NHÌN */
        /* Ép bảng dữ liệu Google Sheet mượt mà vào tone nền darkmode */
        [data-testid="stDataFrame"] {
            background-color: #111827 !important;
            border: 1px solid #1E293B !important;
            border-radius: 12px !important;
            padding: 8px !important;
        }
        
        /* 4. THANH TÌM KIẾM MỀM MẠI */
        .stTextInput input {
            background-color: #111827 !important;
            color: #F3F4F6 !important;
            border-radius: 12px !important;
            border: 1px solid #374151 !important;
            padding: 12px 16px !important;
            transition: all 0.2s ease !important;
        }
        .stTextInput input:focus {
            border-color: #6EE7B7 !important; /* Xanh Mint nhẹ nhàng, không bị chói như lá neon */
            box-shadow: 0 0 0 3px rgba(110, 231, 183, 0.1) !important;
        }

        /* 5. NÚT BẤM MENU SIDEBAR (SỬA ĐỂ HIỆN THỊ RÕ RÀNG HƠN) */
        div.stButton > button {
            background-color: #111827 !important; /* Thêm màu nền nhẹ thay vì trong suốt hoàn toàn */
            color: #9CA3AF !important; 
            border: 1px solid #1F2937 !important; 
            border-radius: 10px !important;
            width: 100% !important;
            font-weight: 500 !important;
            padding: 12px 16px !important;
            transition: all 0.2s ease !important;
            margin-bottom: 8px !important;
        }
        
        /* Hover mượt, phản hồi thân thiện */
        div.stButton > button:hover {
            color: #10B981 !important; /* Chuyển text sang màu xanh ngọc dịu mắt */
            border-color: #10B981 !important;
            background-color: #1F2937 !important;
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.1) !important;
        }

        /* Tiêu đề nhóm menu (SERVICES, TOOLS) */
        .stMarkdown h3 {
            font-size: 12px !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
            color: #4B5563 !important;
            margin-top: 1.5rem !important;
            margin-bottom: 0.75rem !important;
        }
        
        hr {
            border-color: #1F2937 !important;
        }

        /* 6. LAYOUT CARDS HÌNH ẢNH */
        .design-card {
            background-color: #111827;
            border-radius: 16px;
            border: 1px solid #1F2937;
            margin-bottom: 24px;
            overflow: hidden;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
        }
        .design-card:hover {
            transform: translateY(-2px);
            border-color: #374151;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
        }
        .design-card img {
            width: 100%;
            height: auto;
            display: block;
        }
    </style>
    """, unsafe_allow_html=True)