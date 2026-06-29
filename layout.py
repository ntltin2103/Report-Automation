import streamlit as st
import pandas as pd
from validation_report import *
from css import layout_css
import datetime

# 1. Cài đặt ban đầu
st.set_page_config(
    layout="wide", 
    page_title="Automation Report Team", 
    page_icon="📊",
    initial_sidebar_state="expanded"
)

# Áp dụng giao diện cho báo cáo
layout_css()

# Khởi tạo menu mặc định lần đầu chạy
if "current_menu" not in st.session_state:
    st.session_state.current_menu = "✨ Summary"


# 2. Tải dữ liệu chung một lần
SPREADSHEET_NAME = "GS connector"

# Hiển thị trạng thái đang đồng bộ dữ liệu
with st.spinner("Đang đồng bộ dữ liệu từ Google Sheets..."):
    # Dữ liệu này dùng chung cho toàn bộ ứng dụng
    df_data = get_google_sheet_data(SPREADSHEET_NAME)


# 3. Menu bên trái
with st.sidebar:
    st.markdown("<h2 style='color: #F8FAFC; font-size: 22px; font-weight:700; padding-left:8px; margin-bottom: 2rem;'>Menu</h2>", unsafe_allow_html=True)
    
    st.markdown("### Services")
    if st.button("✨ Summary", use_container_width=True):
        st.session_state.current_menu = "✨ Summary"
    if st.button("📁 Chart", use_container_width=True):
        st.session_state.current_menu = "📁 Report"
    if st.button("🌐 Download PPT", use_container_width=True):
        st.session_state.current_menu = "🌐 Download PPT"
    # if st.button("🚀 SaaS", use_container_width=True):
    #     st.session_state.current_menu = "🚀 SaaS"
    
    # st.markdown("### Tools")
    # if st.button("🎨 Design Tools", use_container_width=True):
    #     st.session_state.current_menu = "🎨 Design Tools"
    # if st.button("🛠️ Dev Tools", use_container_width=True):
    #     st.session_state.current_menu = "🛠️ Dev Tools"
    
    # st.markdown("### E-Commerce")
    # if st.button("🛒 Storefronts", use_container_width=True):
    #     st.session_state.current_menu = "🛒 Storefronts"
    # if st.button("💳 Finance", use_container_width=True):
    #     st.session_state.current_menu = "💳 Finance"


# 4. Thanh đầu trang
st.markdown('<div class="topbar-wrapper">', unsafe_allow_html=True)

h_logo, h_search, h_btn, h_space, h_profile = st.columns([1.2, 3.8, 1.5, 1.3, 0.4])

with h_logo:
    st.markdown("<p style='margin:0; color:#F8FAFC; font-weight:700; font-size:15px; letter-spacing: 0.05em; white-space:nowrap;'>REPORT TEAM</p>", unsafe_allow_html=True)

if "search_input_value" not in st.session_state:
    st.session_state["search_input_value"] = ""

# Xóa nội dung tìm kiếm khi bấm nút Clear
def clear_search_callback():
    st.session_state["search_input_key"] = ""
    st.toast("Đã xóa từ khóa tìm kiếm!", icon="")

# Khung tìm kiếm
with h_search:
    # Chia khung thành vùng nhập và nút xóa
    st.markdown('<div class="fixed-search-input">', unsafe_allow_html=True)
    col_input, col_clear = st.columns([0.85, 0.15])
    
    with col_input:
        search_val = st.text_input(
            "Global Search", 
            placeholder="Tìm số request, tên yêu cầu...", 
            label_visibility="collapsed",
            key="search_input_key"  # Gắn key để có thể clear bằng callback
        )
    
    with col_clear:
        # Nút Clear Search nhỏ gọn bằng icon hoặc chữ ngắn
        if st.button("✖️", help="Xóa tìm kiếm", on_click=clear_search_callback, use_container_width=True):
            pass
            
    st.markdown('</div>', unsafe_allow_html=True)

# Hiển thị kết quả tìm kiếm
if search_val:
    query = search_val.strip().lower()
    
    if not df_data.empty:
        col_req = "REQUEST" if "REQUEST" in df_data.columns else ("Request" if "Request" in df_data.columns else None)
        col_name = "Yêu cầu" if "Yêu cầu" in df_data.columns else None
        
        mask = pd.Series(False, index=df_data.index)
        if col_req:
            mask |= df_data[col_req].astype(str).str.lower().str.contains(query, na=False)
        if col_name:
            mask |= df_data[col_name].astype(str).str.lower().str.contains(query, na=False)
        
        df_search_result = df_data[mask]
        
        if not df_search_result.empty:
            st.toast(f"Tìm thấy {len(df_search_result)} kết quả!", icon="")
            st.markdown("---")
            st.markdown(f"### 🔍 Kết quả tìm kiếm toàn cầu cho từ khóa: `{search_val}`")
            
            # Hiển thị bảng lớn full size giống hệt dashboard chính
            st.dataframe(df_search_result, use_container_width=True, height=350)
            st.markdown("---")
        else:
            st.toast("Không tìm thấy, vui lòng nhập lại!", icon="")
            st.warning(f"Không tìm thấy kết quả nào khớp với: '{search_val}'. Vui lòng kiểm tra lại số request hoặc tên yêu cầu.")
    else:
        st.toast("Dữ liệu hệ thống đang trống!", icon="")
with h_btn:
    st.button("Tìm kiếm", use_container_width=True)

with h_space:
        st.markdown("<p style='margin:0; color:#10B981; font-weight:600; text-align:right; margin:0; font-size:13px; white-space:nowrap;'>Kết nối ổn định</p>", unsafe_allow_html=True)

with h_profile:
    st.markdown("<div style='text-align:right; font-size:18px; color:#9CA3AF; cursor:pointer; line-height:1;'>👤</div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True) # Đóng div topbar-wrapper

st.markdown("<hr style='margin-top: 1rem; margin-bottom: 2rem; border-color: #1F2937;'>", unsafe_allow_html=True)

# 5. Chuyển màn hình theo menu
menu = st.session_state.current_menu

if menu == "✨ Summary":
    # Bố cục nút làm mới dữ liệu
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

    # Khối thống kê
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

    # Hiển thị các chỉ số trên giao diện
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

    # Hiển thị bảng dữ liệu
    if not df_data.empty:
        st.dataframe(df_data, use_container_width=True, height=400)
    else:
        st.info("Chưa có dữ liệu hoặc bảng tính đang trống.")
    
elif menu == "📁 Report":
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
        st.warning("Không thể vẽ biểu đồ do dữ liệu trống.")
        
    st.markdown("<br><br><hr style='border-color: #1F2937; margin: 2rem 0;'>", unsafe_allow_html=True)

        # --- BƯỚC 4: CHIA LÀM 2 COLUMNS DÙNG WITH COL1, COL2 ---
    col1, col2 = st.columns(2)
    
    with col1:
        # Biểu đồ cột đôi nằm gọn gàng bên cột số 1, chữ nghĩa giãn đều tuyệt đẹp
        chart_testing_round_8_week(df_data)
        
    with col2:
        # Cột số 2 này em có thể để trống hoặc gọi thêm 1 biểu đồ khác vào sau này nhé
        chart_summary_request_completed(df_data)

elif menu == "🌐 Download PPT":
    st.markdown(f"<h1 style='font-size:28px;'>{menu} Dashboard</h1>", unsafe_allow_html=True)
    st.info("Down Report tại đây.")
    
    if not df_data.empty:
        # Hiển thị bảng dữ liệu Download PPT
        # st.dataframe(df_data, use_container_width=True, height=400)
        
        # Thêm một khoảng hở nhỏ cho thoáng giao diện
        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        
        # --- NÚT BẤM DOWNLOAD FILE POWERPOINT CHO MENU Download PPT ---
        # pptx_data = export_charts_to_pptx(df_data)
        st.download_button(
            label="Tải Slide Báo Cáo (PowerPoint)",
            data=export_charts_to_pptx(df_data),
            file_name=f"Executive_Report_{datetime.date.today().strftime('%Y%m%d')}.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            use_container_width=True
        )
    else:
        st.info("Hệ thống kết nối thành công nhưng chưa tìm thấy dữ liệu phù hợp trong bảng tính.")

else:
    st.markdown(f"<h1 style='font-size:28px;'>{menu} Management</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748B;'>Module báo cáo đang trong lộ trình phát triển và hoàn thiện dữ liệu.</p>", unsafe_allow_html=True)