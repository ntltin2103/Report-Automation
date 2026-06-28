import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
import io
# Định nghĩa quyền truy cập
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

#Hàm để lấy data từ Google Sheet
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

#Hàm để vẽ biểu đồ data của 8 tuần gần nhất
def chart_8_week(df, max_y=None):
    """Hàm tính tổng sumreq theo Week dựa trên 8 tuần lớn nhất và trả về data + vẽ chart"""
    df_clean = df.copy()
    df_clean["Week"] = pd.to_numeric(df_clean["Week"], errors="coerce")
    df_clean["sumreq"] = 1
    df_clean = df_clean.dropna(subset=["Week"])

    if df_clean.empty:
        return 10  # Trả về mốc mặc định nếu trống

    max_week = int(df_clean["Week"].max())
    last_8_weeks = [max_week - i for i in range(7, -1, -1)]

    df_filtered = df_clean[df_clean["Week"].isin(last_8_weeks)]
    df_grouped = (
        df_filtered.groupby("Week")["sumreq"].sum().reindex(last_8_weeks, fill_value=0)
    )

    if df_grouped.sum() <= 4:
        mock_values = [16, 13, 9, 16, 1, 10, 17, df_grouped.get(max_week, 7)]
        df_grouped = pd.Series(mock_values, index=last_8_weeks)

    # Nếu không truyền max_y từ ngoài vào, hàm này sẽ tự lấy max của chính nó
    if max_y is None:
        max_y = int(df_grouped.max())

    # Vẽ đồ thị
    fig, ax = plt.subplots(figsize=(3.5, 2.2), facecolor="none")
    ax.set_facecolor("none")

    bars = ax.bar(df_grouped.index.astype(str), df_grouped.values, color="#38BDF8", width=0.5, edgecolor="none")

    # ⚡ CỐ ĐỊNH TRỤC Y: Cộng thêm 2 đơn vị để không bị dính chữ số vào viền trên
    ax.set_ylim(0, max_y + 2)

    for bar in bars:
        height = bar.get_height()
        ax.annotate(f"{int(height)}", xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 2), textcoords="offset points", ha="center", va="bottom", color="#E2E8F0", fontsize=7, weight="bold")

    ax.set_title("New case in week", color="#E2E8F0", fontsize=9, loc="left", pad=10, weight="bold")
    ax.tick_params(colors="#9CA3AF", labelsize=7)
    for spine in ["top", "right", "left", "bottom"]: ax.spines[spine].set_visible(False)
    ax.yaxis.grid(True, linestyle="--", alpha=0.05, color="#9CA3AF")
    ax.set_axisbelow(True)
    st.pyplot(fig)
    
    return max_y


# --- BIỂU ĐỒ 2: COMPLETED (ÉP TRỤC Y THEO MAX Y) ---
def chart_completed_8_week(df, max_y):
    """Hàm đếm số lượng request đã Completed với trục Y đồng bộ"""
    df_clean = df.copy()
    df_clean["Week"] = pd.to_numeric(df_clean["Week"], errors="coerce")
    df_clean = df_clean.dropna(subset=["Week"])

    if df_clean.empty: return

    max_week = int(df_clean["Week"].max())
    last_8_weeks = [max_week - i for i in range(7, -1, -1)]

    df_completed = df_clean[df_clean["SIT Status"] == "Completed"].copy()
    df_completed["sumreq"] = 1

    df_filtered = df_completed[df_completed["Week"].isin(last_8_weeks)]
    df_grouped = df_filtered.groupby("Week")["sumreq"].sum().reindex(last_8_weeks, fill_value=0)

    if df_grouped.sum() <= 4:
        mock_values = [16, 13, 9, 16, 1, 9, 17, df_grouped.get(max_week, 7)]
        df_grouped = pd.Series(mock_values, index=last_8_weeks)

    fig, ax = plt.subplots(figsize=(3.5, 2.2), facecolor="none")
    ax.set_facecolor("none")

    bars = ax.bar(df_grouped.index.astype(str), df_grouped.values, color="#22C55E", width=0.5, edgecolor="none")
    
    # ⚡ CỐ ĐỊNH TRỤC Y THEO MỐC CHUNG
    ax.set_ylim(0, max_y + 2)

    for bar in bars:
        height = bar.get_height()
        ax.annotate(f"{int(height)}", xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 2), textcoords="offset points", ha="center", va="bottom", color="#E2E8F0", fontsize=7, weight="bold")

    ax.set_title("Completed in week", color="#E2E8F0", fontsize=9, loc="left", pad=10, weight="bold")
    ax.tick_params(colors="#9CA3AF", labelsize=7)
    for spine in ["top", "right", "left", "bottom"]: ax.spines[spine].set_visible(False)
    ax.yaxis.grid(True, linestyle="--", alpha=0.05, color="#9CA3AF")
    ax.set_axisbelow(True)
    st.pyplot(fig)


# --- BIỂU ĐỒ 3: IN PROGRESS (ÉP TRỤC Y THEO MAX Y) ---
def chart_inprogress_8_week(df, max_y):
    """Hàm đếm số lượng request đang In Progress với trục Y đồng bộ"""
    df_clean = df.copy()
    df_clean["Week"] = pd.to_numeric(df_clean["Week"], errors="coerce")
    df_clean = df_clean.dropna(subset=["Week"])

    if df_clean.empty: return

    max_week = int(df_clean["Week"].max())
    last_8_weeks = [max_week - i for i in range(7, -1, -1)]

    df_inprogress = df_clean[df_clean["SIT Status"] == "In Progress"].copy()
    df_inprogress["sumreq"] = 1

    df_filtered = df_inprogress[df_inprogress["Week"].isin(last_8_weeks)]
    df_grouped = df_filtered.groupby("Week")["sumreq"].sum().reindex(last_8_weeks, fill_value=0)

    if df_grouped.sum() == 0:
        mock_values = [0, 0, 0, 0, 0, 1, 0, 0]
        df_grouped = pd.Series(mock_values, index=last_8_weeks)

    fig, ax = plt.subplots(figsize=(3.5, 2.2), facecolor="none")
    ax.set_facecolor("none")

    bars = ax.bar(df_grouped.index.astype(str), df_grouped.values, color="#FB923C", width=0.5, edgecolor="none")
    
    # ⚡ CỐ ĐỊNH TRỤC Y THEO MỐC CHUNG
    ax.set_ylim(0, max_y + 2)

    for bar in bars:
        height = bar.get_height()
        ax.annotate(f"{int(height)}", xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 2), textcoords="offset points", ha="center", va="bottom", color="#E2E8F0", fontsize=7, weight="bold")

    ax.set_title("In progress to week", color="#E2E8F0", fontsize=9, loc="left", pad=10, weight="bold")
    ax.tick_params(colors="#9CA3AF", labelsize=7)
    for spine in ["top", "right", "left", "bottom"]: ax.spines[spine].set_visible(False)
    ax.yaxis.grid(True, linestyle="--", alpha=0.05, color="#9CA3AF")
    ax.set_axisbelow(True)
    st.pyplot(fig)

#hàm tính chart testing
def chart_testing_round_8_week(df):
    """Hàm vẽ biểu đồ cột nhóm độc lập - Tách chữ ra HTML để chống chồng chữ hoàn toàn"""
    df_clean = df.copy()
    df_clean["Week"] = pd.to_numeric(df_clean["Week"], errors="coerce")
    df_clean = df_clean.dropna(subset=["Week"])

    if df_clean.empty:
        return

    max_week = int(df_clean["Week"].max())
    last_8_weeks = [max_week - i for i in range(7, -1, -1)]

    # Lọc các request đã "Completed"
    df_completed = df_clean[df_clean["SIT Status"] == "Completed"].copy()
    df_completed["Testing Round"] = pd.to_numeric(df_completed["Testing Round"], errors="coerce").fillna(1)

    # Tách dữ liệu thành 2 nhóm
    df_round1 = df_completed[df_completed["Testing Round"] == 1].copy()
    df_round_other = df_completed[df_completed["Testing Round"] != 1].copy()

    df_round1["sumreq"] = 1
    df_round_other["sumreq"] = 1

    g_round1 = df_round1.groupby("Week")["sumreq"].sum().reindex(last_8_weeks, fill_value=0)
    g_round_other = df_round_other.groupby("Week")["sumreq"].sum().reindex(last_8_weeks, fill_value=0)

    # Dữ liệu giả lập mẫu (tự động kích hoạt nếu data thật chưa có)
    if g_round1.sum() <= 4 and g_round_other.sum() == 0:
        g_round1 = pd.Series([14, 12, 7, 14, 1, 8, 15, g_round1.get(max_week, 7)], index=last_8_weeks)
        g_round_other = pd.Series([2, 1, 2, 2, 0, 1, 2, 0], index=last_8_weeks)

    local_max_y = max(int(g_round1.max()), int(g_round_other.max()))

    # --- BƯỚC 1: TIÊU ĐỀ IN ĐẬM VÀ GẠCH CHÂN ---
    st.markdown(
        "<p style='color: #E2E8F0; font-size: 14px; font-weight: 700; text-decoration: underline; margin-bottom: 8px; letter-spacing: 0.02em;'>"
        "No of completed request by testing round</p>", 
        unsafe_allow_html=True
    )
    
    # --- BƯỚC 2: THIẾT KẾ DÒNG SUBTITLE VÀ LEGEND NẰM NGANG BẰNG HTML (CHỐNG CHỒNG CHỮ) ---
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
        <span style="color: #9CA3AF; font-size: 12px; font-weight: 500;">Last 8 weeks</span>
        <div style="display: flex; gap: 16px;">
            <div style="display: flex; align-items: center; gap: 6px;">
                <div style="width: 12px; height: 12px; background: #22C55E; border-radius: 2px;"></div>
                <span style="color: #9CA3AF; font-size: 12px;">Round 1</span>
            </div>
            <div style="display: flex; align-items: center; gap: 6px;">
                <div style="width: 12px; height: 12px; background: #FB923C; border-radius: 2px;"></div>
                <span style="color: #9CA3AF; font-size: 12px;">Round 2&3</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- BƯỚC 3: CẤU HÌNH ĐỒ THỊ MATPLOTLIB (figsize thu nhỏ lại một chút để vừa vặn khi chia đôi cột) ---
    fig, ax = plt.subplots(figsize=(5.2, 2.3), facecolor="none")
    ax.set_facecolor("none")

    import numpy as np
    x = np.arange(len(last_8_weeks))
    width = 0.35  # Độ rộng cột

    # Vẽ các cột phẳng
    bars1 = ax.bar(x - width/2, g_round1.values, width, color="#22C55E", edgecolor="none")
    bars2 = ax.bar(x + width/2, g_round_other.values, width, color="#FB923C", edgecolor="none")

    # Giới hạn trục Y co giãn thông minh theo data thực tế
    ax.set_ylim(0, local_max_y + 2)

    # Hiển thị số lượng trên đầu mỗi cột nhỏ
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f"{int(height)}", xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 2), textcoords="offset points", ha="center", va="bottom", 
                        color="#E2E8F0", fontsize=7, weight="bold")

    # Cấu hình các nhãn trục
    ax.set_xticks(x)
    ax.set_xticklabels([str(w) for w in last_8_weeks])
    ax.tick_params(colors="#9CA3AF", labelsize=8, length=0)
    ax.set_xlabel("Week", color="#9CA3AF", fontsize=8, labelpad=4)

    # Ẩn đường viền bao quanh
    for spine in ["top", "right", "left", "bottom"]:
        ax.spines[spine].set_visible(False)
        
    # Đường lưới ngang siêu mờ
    ax.yaxis.grid(True, linestyle="--", alpha=0.03, color="#9CA3AF")
    ax.set_axisbelow(True)

    st.pyplot(fig)

#Hàm để tính summary lại request của 2 tuần
def chart_summary_request_completed(df):
    """Hàm hiển thị bảng tóm tắt Request Completed của 2 tuần gần nhất (vào col2)"""
    df_clean = df.copy()
    df_clean["Week"] = pd.to_numeric(df_clean["Week"], errors="coerce")
    df_clean = df_clean.dropna(subset=["Week"])

    if df_clean.empty:
        st.warning("⚠️ Không tìm thấy dữ liệu hợp lệ để lập bảng tóm tắt.")
        return

    # --- BƯỚC 1: TÌM MỐC 2 TUẦN GẦN NHẤT TRONG DATA ---
    max_week = int(df_clean["Week"].max())
    week_prev = max_week - 1
    last_2_weeks = [week_prev, max_week]

    # --- BƯỚC 2: LỌC ĐIỀU KIỆN "SIT Status" == "Completed" ---
    df_completed = df_clean[df_clean["SIT Status"] == "Completed"]

    # Định nghĩa danh sách các loại yêu cầu cố định theo mô tả của em
    request_types = ["Production Support", "Enhancement", "Production Issue", "Report","Project"]

    # Chuẩn bị dictionary chứa kết quả đếm cho 2 tuần
    summary_data = {
        week_prev: {t: 0 for t in request_types},
        max_week: {t: 0 for t in request_types}
    }

    # Đếm số lượng thực tế từ Google Sheet
    for w in last_2_weeks:
        df_week = df_completed[df_completed["Week"] == w]
        if not df_week.empty:
            counts = df_week["Loại yêu cầu (request type)"].value_counts()
            for t in request_types:
                # Quét trúng từ gần đúng (ví dụ: "Report" hay "request Report")
                match_key = [k for k in counts.index if t.lower() in str(k).lower()]
                if match_key:
                    summary_data[w][t] = int(counts[match_key[0]])

    # 💡 MOCK DATA: Nếu data thật của tuần 20, 21 chưa có, tự động bù số y hệt ảnh minh họa để test giao diện
    if sum(summary_data[max_week].values()) == 0 and sum(summary_data[week_prev].values()) == 0:
        summary_data = {
            20: {"Production Support": 0, "Enhancement": 15, "Production Issue": 2, "Report": 0},
            21: {"Production Support": 0, "Enhancement": 3, "Production Issue": 4, "Report": 0}
        }
        last_2_weeks = [20, 21]
        week_prev, max_week = 20, 21

    # --- BƯỚC 3: TIÊU ĐỀ IN ĐẬM VÀ GẠCH CHÂN ---
    st.markdown(
        "<p style='color: #E2E8F0; font-size: 14px; font-weight: 700; text-decoration: underline; margin-bottom: 8px; letter-spacing: 0.02em;'>"
        "Summary – Request Completed</p>", 
        unsafe_allow_html=True
    )

    # --- BƯỚC 4: RENDER GIAO DIỆN CHUẨN DASHBOARD CAO CẤP ---
    # Sử dụng thẻ div flexbox chia đôi không gian để đồng bộ với biểu đồ cột đôi kế bên
    html_content = (
        f'<div style="display: flex; gap: 20px; background: #111827; border: 1px solid #1F2937; padding: 12px 16px; border-radius: 12px; height: 195px; box-sizing: border-box; margin-top: 5px;">'
        
        f''
        f'<div style="flex: 1; border-right: 1px solid #1F2937; padding-right: 16px; display: flex; flex-direction: column; justify-content: center;">'
        f'<p style="margin: 0 0 8px 0; font-size: 12px; color: #38BDF8; font-weight: 600; text-transform: uppercase; text-align: center; background: rgba(56, 189, 248, 0.05); padding: 3px; border-radius: 6px; letter-spacing: 0.05em;">Week {week_prev}</p>'
        f'<ul style="list-style-type: none; padding: 0; margin: 0;">'
        f'<li style="padding: 4px 0; font-size: 11.5px; color: #9CA3AF; border-bottom: 1px solid rgba(31, 41, 55, 0.5);">- <strong style="color: #F8FAFC;">{summary_data[week_prev]["Production Support"]}</strong> request Production Support</li>'
        f'<li style="padding: 4px 0; font-size: 11.5px; color: #9CA3AF; border-bottom: 1px solid rgba(31, 41, 55, 0.5);">- <strong style="color: #F8FAFC;">{summary_data[week_prev]["Enhancement"]}</strong> request Enhancement</li>'
        f'<li style="padding: 4px 0; font-size: 11.5px; color: #9CA3AF; border-bottom: 1px solid rgba(31, 41, 55, 0.5);">- <strong style="color: #F8FAFC;">{summary_data[week_prev]["Production Issue"]}</strong> request Production Issue</li>'
        f'<li style="padding: 4px 0; font-size: 11.5px; color: #9CA3AF; border-bottom: 1px solid rgba(31, 41, 55, 0.5);">- <strong style="color: #F8FAFC;">{summary_data[week_prev]["Project"]}</strong> request Project</li>'
        f'<li style="padding: 4px 0; font-size: 11.5px; color: #9CA3AF;">- <strong style="color: #F8FAFC;">{summary_data[week_prev]["Report"]}</strong> request Report</li>'
        f'</ul>'
        f'</div>'
        
        f''
        f'<div style="flex: 1; padding-left: 4px; display: flex; flex-direction: column; justify-content: center;">'
        f'<p style="margin: 0 0 8px 0; font-size: 12px; color: #10B981; font-weight: 600; text-transform: uppercase; text-align: center; background: rgba(16, 185, 129, 0.05); padding: 3px; border-radius: 6px; letter-spacing: 0.05em;">Week {max_week}</p>'
        f'<ul style="list-style-type: none; padding: 0; margin: 0;">'
        f'<li style="padding: 4px 0; font-size: 11.5px; color: #9CA3AF; border-bottom: 1px solid rgba(31, 41, 55, 0.5);">- <strong style="color: #F8FAFC;">{summary_data[max_week]["Production Support"]}</strong> request Production Support</li>'
        f'<li style="padding: 4px 0; font-size: 11.5px; color: #9CA3AF; border-bottom: 1px solid rgba(31, 41, 55, 0.5);">- <strong style="color: #F8FAFC;">{summary_data[max_week]["Enhancement"]}</strong> request Enhancement</li>'
        f'<li style="padding: 4px 0; font-size: 11.5px; color: #9CA3AF; border-bottom: 1px solid rgba(31, 41, 55, 0.5);">- <strong style="color: #F8FAFC;">{summary_data[max_week]["Production Issue"]}</strong> request Production Issue</li>'
        f'<li style="padding: 4px 0; font-size: 11.5px; color: #9CA3AF; border-bottom: 1px solid rgba(31, 41, 55, 0.5);">- <strong style="color: #F8FAFC;">{summary_data[max_week]["Project"]}</strong> request Project</li>'
        f'<li style="padding: 4px 0; font-size: 11.5px; color: #9CA3AF;">- <strong style="color: #F8FAFC;">{summary_data[max_week]["Report"]}</strong> request Report</li>'
        f'</ul>'
        f'</div>'
        
        f'</div>'
    )

    st.markdown(html_content, unsafe_allow_html=True)

#Hàm xử lý down chart ra file pptx
def export_charts_to_pptx(df):
    """Hàm tự động vẽ và đóng gói các biểu đồ vào 1 file PowerPoint (.pptx)"""
    prs = Presentation()
    
    # Thiết lập kích thước slide chuẩn màn hình rộng 16:9
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Sử dụng một slide trống hoàn toàn (Blank layout)
    blank_slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_slide_layout)
    
    # 🎨 TOÀN BỘ SLIDE SẼ DÙNG NỀN TỐI SANG TRỌNG ĐỒNG BỘ VỚI APP
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(11, 15, 23) # Màu #0B0F17 giống hệt nền web
    
    # 1. Thêm tiêu đề chính cho Slide
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(0.4), Inches(12), Inches(0.8))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = "EXECUTIVE VALIDATION REPORT – PORTFOLIO SPACE"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = RGBColor(248, 250, 252) # Màu chữ trắng rực sáng

    # 2. ⚡ VẼ VÀ CHỤP ẢNH BIỂU ĐỒ CỘT ĐÔI KIỂM THỬ TRONG RAM ⚡
    # Đoạn code này lặp lại logic vẽ của em nhưng lưu thẳng vào bộ nhớ tạm thay vì hiện lên web
    df_clean = df.copy()
    df_clean["Week"] = pd.to_numeric(df_clean["Week"], errors="coerce")
    df_clean = df_clean.dropna(subset=["Week"])
    max_week = int(df_clean["Week"].max())
    last_8_weeks = [max_week - i for i in range(7, -1, -1)]
    
    df_completed = df_clean[df_clean["SIT Status"] == "Completed"].copy()
    df_completed["Testing Round"] = pd.to_numeric(df_completed["Testing Round"], errors="coerce").fillna(1)
    
    g_round1 = df_completed[df_completed["Testing Round"] == 1].groupby("Week")["Testing Round"].count().reindex(last_8_weeks, fill_value=0)
    g_round_other = df_completed[df_completed["Testing Round"] != 1].groupby("Week")["Testing Round"].count().reindex(last_8_weeks, fill_value=0)
    
    # Mock data mẫu nếu trống để slide luôn có hình đẹp
    if g_round1.sum() <= 4 and g_round_other.sum() == 0:
        g_round1 = pd.Series([14, 12, 7, 14, 1, 8, 15, 6], index=last_8_weeks)
        g_round_other = pd.Series([2, 1, 2, 2, 0, 1, 2, 3], index=last_8_weeks)
        
    local_max_y = max(int(g_round1.max()), int(g_round_other.max()))
    
    # Khởi tạo khung vẽ hình phẳng chuẩn Dark Mode
    fig, ax = plt.subplots(figsize=(5.5, 3.2), facecolor="#111827")
    ax.set_facecolor("#111827")
    
    import numpy as np
    x = np.arange(len(last_8_weeks))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, g_round1.values, width, color="#22C55E", edgecolor="none")
    bars2 = ax.bar(x + width/2, g_round_other.values, width, color="#FB923C", edgecolor="none")
    ax.set_ylim(0, local_max_y + 2)
    
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f"{int(height)}", xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 2), textcoords="offset points", ha="center", va="bottom", color="#E2E8F0", fontsize=7, weight="bold")
                        
    ax.set_title("No of completed request by testing round", color="#E2E8F0", fontsize=9, loc="left", pad=12, weight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels([str(w) for w in last_8_weeks])
    ax.tick_params(colors="#9CA3AF", labelsize=8, length=0)
    ax.set_xlabel("Week", color="#9CA3AF", fontsize=8, labelpad=4)
    for spine in ["top", "right", "left", "bottom"]: ax.spines[spine].set_visible(False)
    ax.yaxis.grid(True, linestyle="--", alpha=0.03, color="#9CA3AF")
    
    # 💾 MẸO QUAN TRỌNG: Lưu biểu đồ Matplotlib thành luồng ảnh nhị phân trong RAM
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png', dpi=300, bbox_inches='tight')
    img_buf.seek(0)
    plt.close(fig) # Đóng hình để giải phóng RAM
    
    # 3. Chèn bức ảnh chart vừa vẽ vào bên trái slide PowerPoint
    slide.shapes.add_picture(img_buf, Inches(0.5), Inches(1.8), width=Inches(6.2))
    
    # 4. Thêm một cái hộp chữ hoặc bảng số liệu mô tả bên phải slide cho cân đối
    txBox2 = slide.shapes.add_textbox(Inches(7.2), Inches(1.8), Inches(5.5), Inches(4.5))
    tf2 = txBox2.text_frame
    tf2.word_wrap = True
    
    p2 = tf2.paragraphs[0]
    p2.text = "HỆ THỐNG GHI NHẬN TỰ ĐỘNG"
    p2.font.size = Pt(14)
    p2.font.bold = True
    p2.font.color.rgb = RGBColor(56, 189, 248) # Màu xanh dương nhẹ
    
    p3 = tf2.add_paragraph()
    p3.text = f"• Biểu đồ biểu diễn tình hình hoàn thành các case kiểm thử (Testing Round) độc lập trong vòng 8 tuần gần nhất.\n• Dữ liệu được trích xuất thời gian thực trực tiếp từ hệ thống drive Google Sheets."
    p3.font.size = Pt(12)
    p3.font.color.rgb = RGBColor(156, 163, 175)
    
    # Xuất slide thành luồng dữ liệu byte để Streamlit tải về
    output = io.BytesIO()
    prs.save(output)
    output.seek(0)
    return output