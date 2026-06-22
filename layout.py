import streamlit as st
from validation_report import get_google_sheet_data
from css import layout_css
# 1. Cấu hình trang Wide Mode và Dark Theme
st.set_page_config(layout="wide", page_title="Design Studio Layout", initial_sidebar_state="expanded")

# Khởi tạo trạng thái menu mặc định nếu chưa có
if "current_menu" not in st.session_state:
    st.session_state.current_menu = "✨ AI Assets"

# 2. Inject Custom CSS để biến đổi hoàn toàn UI
layout_css()

# 3. Sidebar Menu - Cập nhật st.session_state khi click
with st.sidebar:
    st.markdown("### MENU")
    st.markdown(" **SERVICES**")
    if st.button("✨ AI Assets"):
        st.session_state.current_menu = "✨ AI Assets"
    if st.button("📁 Portfolio"):
        st.session_state.current_menu = "📁 Portfolio"
    if st.button("🌐 Web3"):
        st.session_state.current_menu = "🌐 Web3"
    if st.button("🚀 SaaS"):
        st.session_state.current_menu = "🚀 SaaS"
    
    st.markdown("---")
    st.markdown("### TOOLS")
    if st.button("🎨 Design Tools"):
        st.session_state.current_menu = "🎨 Design Tools"
    if st.button("🛠️ Dev Tools"):
        st.session_state.current_menu = "🛠️ Dev Tools"
    
    st.markdown("---")
    st.markdown("### E-COMMERCE")
    if st.button("🛒 Storefronts"):
        st.session_state.current_menu = "🛒 Storefronts"
    if st.button("💳 Finance"):
        st.session_state.current_menu = "💳 Finance"


# 4. Top Navigation Bar (Dùng chung cho toàn bộ layout hệ thống)
t1, t2, t3, t4, t5 = st.columns([1, 4, 2, 1, 1])
with t1:
    st.markdown("### W.") 
with t2:
    st.text_input("", placeholder="Search for designs...", label_visibility="collapsed")
with t3:
    st.button("Submit a website")
with t4:
    st.markdown("<p style='color:#DAFFDE; font-weight:bold; padding-top:10px;'>Pro Access</p>", unsafe_allow_html=True)
with t5:
    st.markdown("👤") 

st.markdown("---")


# 5. ĐIỀU HƯỚNG GIAO DIỆN DỰA TRÊN MENU ĐANG CHỌN (Rất dễ để bạn Enhance)
# df_data = get_google_sheet_data("GS connector")
menu = st.session_state.current_menu
if menu == "✨ AI Assets":
    st.write("Style ⌵ | Illustration ⌵ | Attributes ⌵")
    
    SPREADSHEET_NAME = "GS connector" 
    
    with st.spinner("🔄 Đang đồng bộ dữ liệu từ Google Sheets..."):
        
        df_data = get_google_sheet_data(SPREADSHEET_NAME)
    
    if not df_data.empty:
        # Bạn có thể chọn cách hiển thị Dataframe thô hoặc map vào Grid UX/UI
        st.dataframe(df_data, use_container_width=True)
    else:
        st.info("Chưa có dữ liệu nào được tải lên hoặc bảng tính đang trống.")

elif menu == "📁 Portfolio":
    st.title("📁 Portfolio Space")
    # Viết tiếp Layout UI riêng cho mục Portfolio ở đây...
    st.write("Giao diện danh sách các nhà thiết kế nổi bật.")
    st.columns(3)

elif menu == "🌐 Web3":
    st.title("🌐 Web3 Directory")
    # Viết tiếp Layout UI riêng cho mục Web3 ở đây...
    st.info("Trang hiển thị các dự án Crypto/Web3 UX.")

elif menu == "🚀 SaaS":
    st.title("🚀 SaaS Platforms")
    # Viết tiếp Layout UI riêng cho mục SaaS ở đây...

elif menu == "🎨 Design Tools":
    st.title("🎨 Premium Design Tools")