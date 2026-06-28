import streamlit as st
import pandas as pd
from validation_report import *
from css import layout_css
import datetime

# =========================================================================
# 1. INITIAL SETUP & BRANDING
# =========================================================================
st.set_page_config(
    layout="wide", 
    page_title="Executive Validation Report", 
    page_icon="📊",
    initial_sidebar_state="expanded"
)

# Áp dụng bộ CSS siêu mịn đã tinh chỉnh riêng cho báo cáo cấp cao
layout_css()

# Khởi tạo trạng thái menu mặc định nếu hệ thống chạy lần đầu
if "current_menu" not in st.session_state:
    st.session_state.current_menu = "✨ AI Assets"


# =========================================================================
# 💡 ĐIỂM VÀNG TỐI ƯU: GỌI DATA CHUNG 1 LẦN DUY NHẤT CHO TOÀN BỘ APP
# =========================================================================
SPREADSHEET_NAME = "GS connector"

# Dùng st.spinner ở trên cùng, chỉ chạy đúng 1 lần khi load app hoặc đổi dữ liệu
with st.spinner("🔄 Hệ thống đang đồng bộ dữ liệu tổng thể từ Google Sheets..."):
    # Biến df_data này bây giờ là biến TOÀN CỤC (Global), menu nào cũng xài được
    df_data = get_google_sheet_data(SPREADSHEET_NAME)


# =========================================================================
# 2. SIDEBAR NAVIGATION SYSTEM (REDESIGNED)
# =========================================================================
with st.sidebar:
    st.markdown("<h2 style='color: #F8FAFC; font-size: 22px; font-weight:700; padding-left:8px; margin-bottom: 2rem;'>Studio.io</h2>", unsafe_allow_html=True)
    
    st.markdown("### Services")
    if st.button("✨ AI Assets", use_container_width=True):
        st.session_state.current_menu = "✨ AI Assets"
    if st.button("📁 Portfolio", use_container_width=True):
        st.session_state.current_menu = "📁 Portfolio"
    if st.button("🌐 Web3", use_container_width=True):
        st.session_state.current_menu = "🌐 Web3"
    if st.button("🚀 SaaS", use_container_width=True):
        st.session_state.current_menu = "🚀 SaaS"
    
    st.markdown("### Tools")
    if st.button("🎨 Design Tools", use_container_width=True):
        st.session_state.current_menu = "🎨 Design Tools"
    if st.button("🛠️ Dev Tools", use_container_width=True):
        st.session_state.current_menu = "🛠️ Dev Tools"
    
    st.markdown("### E-Commerce")
    if st.button("🛒 Storefronts", use_container_width=True):
        st.session_state.current_menu = "🛒 Storefronts"
    if st.button("💳 Finance", use_container_width=True):
        st.session_state.current_menu = "💳 Finance"


# =========================================================================
# 3. TOP EXECUTIVE HEADER BAR
# =========================================================================
st.markdown('<div class="topbar-wrapper">', unsafe_allow_html=True)

h_logo, h_search, h_btn, h_space, h_profile = st.columns([1.2, 3.8, 1.5, 1.3, 0.4])

with h_logo:
    st.markdown("<p style='margin:0; color:#F8FAFC; font-weight:700; font-size:15px; letter-spacing: 0.05em; white-space:nowrap;'>BẢNG ĐIỀU KHIỂN</p>", unsafe_allow_html=True)

with h_search:
    # Thêm một chút CSS riêng cho ô tìm kiếm để loại bỏ khoảng trống chênh vênh
    st.markdown('<div class="fixed-search-input">', unsafe_allow_html=True)
    st.text_input("Global Search", placeholder="Tìm kiếm hệ thống, mã yêu cầu, nhân sự...", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

with h_btn:
    st.button("⚙️ Cấu hình bộ lọc", use_container_width=True)

with h_space:
    st.markdown("<p style='color:#10B981; font-weight:600; text-align:right; margin:0; font-size:13px; white-space:nowrap;'>✓ Kết nối ổn định</p>", unsafe_allow_html=True)

with h_profile:
    st.markdown("<div style='text-align:right; font-size:18px; color:#9CA3AF; cursor:pointer; line-height:1;'>👤</div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True) # Đóng div topbar-wrapper

st.markdown("<hr style='margin-top: 1rem; margin-bottom: 2rem; border-color: #1F2937;'>", unsafe_allow_html=True)

# =========================================================================
# 4. DYNAMIC INTERFACE ROUTER (Dựa trên biến 'menu')
# =========================================================================
menu = st.session_state.current_menu

if menu == "✨ AI Assets":
    # Layout cho nút refresh data
    left, center, right = st.columns([6, 3, 1])
    with left:
        st.markdown("""
        <h2 style="margin:0; color:#E2E8F0; font-weight:700;">📊 Report Dashboard</h2>
        <p style="margin:0; color:#64748B; font-size:14px;">Google Sheets Data Monitoring</p>
        """, unsafe_allow_html=True)
    with center:
        st.success("🟢 Last synced successfully")
    with right:
        # TỐI ƯU NÚT REFRESH: Xóa cache chuẩn xác và ép render lại an toàn
        if st.button("↻", use_container_width=True):
            st.cache_data.clear()
            st.experimental_rerun() if hasattr(st, "experimental_rerun") else st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    
    f_title, f_tabs = st.columns([2, 3])
    with f_title:
        st.markdown(f"<h1 style='margin:0; font-size:28px;'>{menu}</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#64748B; font-size:14px; margin-top:4px;'>Hệ thống quản lý và phê duyệt danh sách vận hành tự động</p>", unsafe_allow_html=True)
    with f_tabs:
        st.markdown("<div style='text-align:right; color:#64748B; font-size:14px; padding-top:15px;'>Phân loại: <span style='color:#2563EB; font-weight:600; cursor:pointer;'>Tất cả ⌵</span> | <span style='cursor:pointer;'>Mới nhất ⌵</span> | <span style='cursor:pointer;'>Ưu tiên ⌵</span></div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    # --- KHỐI METRICS ---
    if not df_data.empty:
        # 1. Tổng số yêu cầu = Đếm tổng số dòng có trong cột "REQUEST" (loại bỏ các dòng trống nếu có)
        total_requests = int(df_data["REQUEST"].dropna().count())
        
        # 2. Đang xử lý = Đếm số dòng có trạng thái "In Progress" trong cột "SIT Status"
        in_progress_count = int((df_data["SIT Status"] == "In Progress").sum())
        
        # 3. Lỗi vận hành = Đếm số dòng có loại yêu cầu bằng "Production Issue" (hoặc "Production Support" tùy thuộc chính xác chữ trong sheet của em)
        # Thầy dùng toán tử toán hợp | (hoặc) để quét cả hai chữ cho chắc chắn nhé
        prod_issue_count = int(df_data["Loại yêu cầu (request type)"].isin(["Production Issue", "Production Support"]).sum())
        
        # 4. Tỷ lệ hoàn thành (SLA) = Tính tỷ lệ của số case "Completed" trên tổng số case có trạng thái
        completed_count = (df_data["SIT Status"] == "Completed").sum()
        total_status_count = df_data["SIT Status"].dropna().count()
        
        if total_status_count > 0:
            sla_percentage = (completed_count / total_status_count) * 100
            sla_value = f"{sla_percentage:.1f}%"
        else:
            sla_value = "0.0%"
    else:
        # Giá trị dự phòng nếu data load lên bị trống
        total_requests, in_progress_count, prod_issue_count, sla_value = 0, 0, 0, "0.0%"

    # --- BIỂU DIỄN GIAO DIỆN METRICS LÊN STREAMLIT ---
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div style="background: #111827; border: 1px solid #1F2937; padding: 1.2rem; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.2);">
            <p style="margin: 0; font-size: 13px; color: #9CA3AF; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em;">Tổng số yêu cầu</p>
            <p style="margin: 8px 0; font-size: 32px; color: #F8FAFC; font-weight: 700; line-height: 1;">{total_requests:,}</p>
            <span style="font-size: 12px; color: #10B981; background: rgba(16, 185, 129, 0.1); padding: 2px 8px; border-radius: 20px; font-weight: 500;">↑ Realtime Synced</span>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div style="background: #111827; border: 1px solid #1F2937; padding: 1.2rem; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.2);">
            <p style="margin: 0; font-size: 13px; color: #9CA3AF; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em;">Đang xử lý (SIT/UAT)</p>
            <p style="margin: 8px 0; font-size: 32px; color: #38BDF8; font-weight: 700; line-height: 1;">{in_progress_count}</p>
            <span style="font-size: 12px; color: #9CA3AF; background: rgba(156, 163, 175, 0.1); padding: 2px 8px; border-radius: 20px; font-weight: 500;">→ Running</span>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        # Nếu có lỗi vận hành (>0) thì hiện màu đỏ cảnh báo, ngược lại hiện màu xanh an toàn
        status_color = "#F87171" if prod_issue_count > 0 else "#9CA3AF"
        status_bg = "rgba(239, 68, 68, 0.1)" if prod_issue_count > 0 else "rgba(156, 163, 175, 0.1)"
        status_text = "↑ Critical Alert" if prod_issue_count > 0 else "✓ System Safe"
        
        st.markdown(f"""
        <div style="background: #111827; border: 1px solid #1F2937; padding: 1.2rem; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.2);">
            <p style="margin: 0; font-size: 13px; color: #9CA3AF; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em;">Lỗi vận hành (Prod)</p>
            <p style="margin: 8px 0; font-size: 32px; color: {status_color}; font-weight: 700; line-height: 1;">{prod_issue_count}</p>
            <span style="font-size: 12px; color: {status_color}; background: {status_bg}; padding: 2px 8px; border-radius: 20px; font-weight: 500;">{status_text}</span>
        </div>
        """, unsafe_allow_html=True)

    with m4:
        # SLA >= 95% màu xanh lá, ngược lại màu cam cần cải thiện
        is_sla_good = total_status_count > 0 and sla_percentage >= 95
        sla_color = "#22C55E" if is_sla_good else "#FB923C"
        sla_bg = "rgba(34, 197, 94, 0.1)" if is_sla_good else "rgba(251, 146, 60, 0.1)"
        sla_sub = "↑ On Target" if is_sla_good else "↓ Under Target"

        st.markdown(f"""
        <div style="background: #111827; border: 1px solid #1F2937; padding: 1.2rem; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.2);">
            <p style="margin: 0; font-size: 13px; color: #9CA3AF; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em;">Tỷ lệ hoàn thành (SLA)</p>
            <p style="margin: 8px 0; font-size: 32px; color: {sla_color}; font-weight: 700; line-height: 1;">{sla_value}</p>
            <span style="font-size: 12px; color: {sla_color}; background: {sla_bg}; padding: 2px 8px; border-radius: 20px; font-weight: 500;">{sla_sub}</span>
        </div>
        """, unsafe_allow_html=True)

    # HIỂN THỊ BẢNG DỮ LIỆU TẠI AI ASSETS
    if not df_data.empty:
        st.dataframe(df_data, use_container_width=True, height=400)
    else:
        st.info("Chưa có dữ liệu hoặc bảng tính đang trống.")
    
elif menu == "📁 Portfolio":
    # st.markdown(f"<h1 style='font-size:28px;'>{menu} Space</h1>", unsafe_allow_html=True)
    # st.markdown("<p style='color:#64748B;'>Danh mục hồ sơ và năng lực nhân sự phòng ban</p>", unsafe_allow_html=True)
    # st.markdown("<hr style='border-color: #1F2937;'>", unsafe_allow_html=True)
    
    left, center, right = st.columns([6, 3, 1])
    with left:
        st.markdown(f"<h1 style='font-size:28px;'>{menu} Space</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#64748B;'>Danh mục hồ sơ và năng lực nhân sự phòng ban</p>", unsafe_allow_html=True)
        st.markdown("<hr style='border-color: #1F2937;'>", unsafe_allow_html=True)
    with center:
        st.success("🟢 Last synced successfully")
    with right:
        # TỐI ƯU NÚT REFRESH: Xóa cache chuẩn xác và ép render lại an toàn
        if st.button("↻", use_container_width=True):
            st.cache_data.clear()
            st.experimental_rerun() if hasattr(st, "experimental_rerun") else st.rerun()

    # st.markdown("<br>", unsafe_allow_html=True)

    if not df_data.empty:
        # Cấu trúc 3 cột xếp hàng ngang hoàn hảo
        c1, c2, c3 = st.columns(3)
        
        with c1:
            shared_max_y = chart_8_week(df_data)
            
        with c2:
            chart_completed_8_week(df_data, max_y=shared_max_y)
            
        with c3:
            chart_inprogress_8_week(df_data,max_y=shared_max_y)
    else:
        st.warning("⚠️ Không thể vẽ biểu đồ do dữ liệu trống.")
        
    st.markdown("<br><br><hr style='border-color: #1F2937; margin: 2rem 0;'>", unsafe_allow_html=True)

        # --- BƯỚC 4: CHIA LÀM 2 COLUMNS DÙNG WITH COL1, COL2 ---
    col1, col2 = st.columns(2)
    
    with col1:
        # Biểu đồ cột đôi nằm gọn gàng bên cột số 1, chữ nghĩa giãn đều tuyệt đẹp
        chart_testing_round_8_week(df_data)
        
    with col2:
        # Cột số 2 này em có thể để trống hoặc gọi thêm 1 biểu đồ khác vào sau này nhé
        chart_summary_request_completed(df_data)
            # st.markdown("""
            # <div class='custom-card'>
            #     <h3 style='margin: 0 0 8px 0; color:#E2E8F0;'>Nhà thiết kế cấp cao</h3>
            #     <p style='color:#64748B; font-size:13px; margin-bottom:16px;'>Phụ trách UI/UX hệ thống Core Banking</p>
            #     <div style='display:flex; justify-content:space-between; align-items:center;'>
            #         <span style='background:#1E293B; color:#38BDF8; padding:4px 10px; border-radius:20px; font-size:12px; font-weight:600;'>Đang vận hành</span>
            #         <span style='color:#94A3B8; font-size:12px;'>12 Dự án</span>
            #     </div>
            # </div>
            # """, unsafe_allow_html=True)

elif menu == "🌐 Web3":
    st.markdown(f"<h1 style='font-size:28px;'>{menu} Dashboard</h1>", unsafe_allow_html=True)
    st.info("Giao diện đang được thiết kế cấu trúc riêng cho nền tảng phi tập trung.")
    
    if not df_data.empty:
        st.dataframe(df_data, use_container_width=True, height=450)
    else:
        st.info("Hệ thống kết nối thành công nhưng chưa tìm thấy dữ liệu phù hợp trong bảng tính.")

else:
    st.markdown(f"<h1 style='font-size:28px;'>{menu} Management</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748B;'>Module báo cáo đang trong lộ trình phát triển và hoàn thiện dữ liệu.</p>", unsafe_allow_html=True)