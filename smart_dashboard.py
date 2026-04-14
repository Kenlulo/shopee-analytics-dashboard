"""
📊 Shopee Revenue Analytics Suite v4.0
Chuyên phân tích doanh thu Shopee Seller Center
Auto-mapping cột, tính toán phí sàn, doanh thu thực nhận
Author: Hồ Anh Khoa | 2026
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re
from datetime import datetime


# ═══════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Shopee Revenue Analytics",
    page_icon="🛒",
    layout="wide"
)

# ═══════════════════════════════════════════════════════════════
# CSS — Premium Dark Teal Theme
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #F0F2F6 0%, #E8ECF1 100%);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0A4F4A 0%, #0B5C57 40%, #0D6B65 100%) !important;
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] {
        color: #E8F6F3 !important;
    }

    [data-testid="stHeader"] { background-color: transparent; }
    .block-container { padding-top: 1rem !important; max-width: 98% !important; }

    /* Title */
    .suite-title {
        font-size: 28px; font-weight: 800;
        background: linear-gradient(135deg, #EE4D2D, #FF6633);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px; margin-bottom: 0;
    }
    .suite-subtitle { font-size: 14px; color: #7FB3D5; font-weight: 500; margin-bottom: 16px; }

    /* KPI Cards */
    .kpi-card {
        background: #FFFFFF; border-radius: 14px; padding: 18px 20px;
        text-align: center; border: 1px solid #E5E8EB;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
        transition: all 0.25s ease;
    }
    .kpi-card:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(238,77,45,0.12); border-color: #EE4D2D; }
    .kpi-icon { font-size: 22px; margin-bottom: 4px; }
    .kpi-label { color: #7F8C8D; font-size: 10px; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 700; margin-bottom: 4px; }
    .kpi-value { color: #2C3E50; font-size: 24px; font-weight: 800; margin: 2px 0; }
    .kpi-value.orange { color: #EE4D2D; }
    .kpi-value.green { color: #27AE60; }
    .kpi-value.red { color: #E74C3C; }
    .kpi-value.blue { color: #2980B9; }
    .kpi-sub { color: #95A5A6; font-size: 11px; font-weight: 500; }

    /* Empty state */
    .empty-state {
        text-align: center; padding: 80px 40px;
        background: #FFFFFF; border-radius: 16px; border: 2px dashed #BDC3C7;
        margin: 40px auto; max-width: 620px;
    }
    .empty-state .icon { font-size: 64px; margin-bottom: 16px; }
    .empty-state h3 { color: #2C3E50; font-weight: 700; }
    .empty-state p { color: #7F8C8D; font-size: 15px; }

    hr { border-color: #D5DBDB !important; margin: 16px 0 !important; }
    /* Fix file uploader text contrast */
    [data-testid="stSidebar"] [data-testid="stFileUploader"] p,
    [data-testid="stSidebar"] [data-testid="stFileUploader"] span,
    [data-testid="stSidebar"] [data-testid="stFileUploader"] small,
    [data-testid="stSidebar"] [data-testid="stFileUploader"] div {
        color: #2C3E50 !important;
    }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# LANGUAGE SYSTEM
# ═══════════════════════════════════════════════════════════════
TRANSLATIONS = {
    'Chào mừng đến với Shopee Revenue Analytics': 'Welcome to Shopee Revenue Analytics',
    'Tải lên file xuất từ Shopee Seller Center để bắt đầu phân tích.': 'Upload your Shopee Seller Center export to start analyzing.',
    'Bộ Lọc': 'Filters',
    'Trạng thái đơn hàng': 'Order Status',
    'Tất cả': 'All',
    'Tải lên file dữ liệu': 'Upload data file',
    'Chỉ Số Tổng Quan': 'Key Metrics',
    'Tổng Doanh Thu (GMV)': 'Gross Merchandise Value',
    'Doanh Thu Thực Nhận': 'Net Revenue',
    'Tổng Phí Sàn': 'Total Platform Fees',
    'Tỷ Lệ Đơn Hủy/Hoàn': 'Cancellation Rate',
    'Xu Hướng & So Sánh': 'Trends & Comparison',
    'Xu Hướng Doanh Thu Thực Nhận': 'Net Revenue Trend',
    'Doanh Thu vs Phí Sàn theo Ngày': 'Revenue vs Fees by Day',
    'Phân Tích Chi Tiết': 'Detailed Analysis',
    'Tỷ Trọng Các Loại Phí': 'Fee Breakdown',
    'Top 10 Sản Phẩm Doanh Thu Cao Nhất': 'Top 10 Products by Revenue',
    'Phân Tích Hành Vi': 'Behavioral Analysis',
    'Đơn Hàng Theo Khung Giờ': 'Orders by Hour',
    'Trạng Thái Đơn Hàng': 'Order Status Distribution',
    'Dữ Liệu Gốc': 'Raw Data',
    'Xem dữ liệu chi tiết': 'View detailed data',
    'dòng': 'rows',
    'cột': 'columns',
    'Tải xuống CSV': 'Download CSV',
    'Doanh thu': 'Revenue',
    'Phí sàn': 'Fees',
    'theo ngày': 'by day',
    'Giờ vàng': 'Golden Hours',
    'Phí cố định': 'Fixed Fee',
    'Phí dịch vụ': 'Service Fee',
    'Phí thanh toán': 'Payment Fee',
    'Phí Freeship': 'Freeship Fee',
    'DỰ ÁN CÁ NHÂN: Công cụ phân tích doanh thu Shopee mã nguồn mở. Các phân tích chỉ mang tính chất tham khảo.': 'PERSONAL PROJECT: Open-source Shopee revenue analysis tool. Analytics are for reference only.',
    'Nếu bạn muốn xem thêm dự án khác hãy': 'If you want to view more projects, please',
    'nhấp vào đây': 'click here',
    'Phân tích doanh thu, phí sàn, và hành vi đơn hàng từ Shopee Seller Center': 'Analyze revenue, platform fees, and order behavior from Shopee Seller Center',
    'Tự động nhận diện cột Shopee (Tiếng Việt & Tiếng Anh)': 'Auto-detect Shopee columns (Vietnamese & English)',
    'Tính toán Doanh thu thực nhận, Phí sàn, Tỷ lệ hủy': 'Calculate Net Revenue, Platform Fees, Cancel Rate',
    '6+ biểu đồ chuyên sâu (Xu hướng, Phí, Top SP, Giờ vàng)': '6+ advanced charts (Trends, Fees, Top Products, Golden Hour)',
    'Lọc theo Trạng thái đơn hàng': 'Filter by Order Status',
    'Regex xử lý ₫, dấu chấm/phẩy lộn xộn': 'Robust Regex handling for ₫, mixed dot/comma formats',
    'Tải File Dữ Liệu Shopee Mẫu (Excel)': 'Download Shopee Sample Data (Excel)',
    'Phát triển bởi Hồ Anh Khoa': 'Developed by Ho Anh Khoa',
    'Nhấp vào đây để xem thêm các dự án Portfolio khác': 'Click here to view my other Portfolio projects',
    'Hoàn thành': 'Completed',
    'Đã hủy': 'Cancelled',
    'Trả hàng/Hoàn tiền': 'Returned/Refunded',
    'Đang xử lý': 'Processing',
    'Đang hủy': 'Cancelled',
    'Trả hàng/Hoàn tiền': 'Returned/Refunded',
    'Đang xử lý': 'Processing',
    'Đang giao hàng': 'Shipping',
    '📅 Khoảng ngày': '📅 Date Range',
    'Hiển thị:': 'Showing:',
    'Xuất Báo Cáo (Excel)': 'Export Report (Excel)',
    'Chỉ Số': 'Metric',
    'Giá Trị': 'Value',
    'Tổng Quan': 'Summary',
}
lang = "VN"

def t(text):
    if lang == "EN" and text in TRANSLATIONS:
        return TRANSLATIONS[text]
    return text

def fmt(n):
    if pd.isna(n): return "—"
    n = float(n)
    if abs(n) >= 1e9: return f"{n/1e9:,.1f}B"
    if abs(n) >= 1e6: return f"{n/1e6:,.1f}M"
    if abs(n) >= 1e3: return f"{n:,.0f}"
    if isinstance(n, float) and n != int(n): return f"{n:,.2f}"
    return f"{n:,.0f}"


# ═══════════════════════════════════════════════════════════════
# DATA ENGINE — Bulletproof Cleaning
# ═══════════════════════════════════════════════════════════════
def force_numeric(series):
    """
    Xử lý mọi định dạng số Shopee:
    ₫25.000.000, 25,000,000, 25 000, -500.000, v.v.
    """
    s = series.astype(str)

    def parse_value(x):
        if pd.isna(x): return pd.NA
        x = str(x).strip()
        if x == '' or x.lower() in ('nan', 'none', 'nat', '...', '-'): return pd.NA

        dots = x.count('.')
        commas = x.count(',')

        # US: 1,000.50 → xóa phẩy
        if commas > 0 and dots == 1:
            x = x.replace(',', '')
        # VN: 1.000.000,50 → xóa chấm, đổi phẩy → chấm
        elif dots > 0 and commas == 1:
            x = x.replace('.', '').replace(',', '.')
        # Nhiều phẩy: 1,000,000 → xóa phẩy
        elif commas > 1:
            x = x.replace(',', '')
        # Nhiều chấm: 1.000.000 → xóa chấm
        elif dots > 1:
            x = x.replace('.', '')

        # Xóa mọi ký tự không phải số / chấm / dấu trừ (₫, VND, $, %, v.v.)
        return re.sub(r'[^\d.\-]', '', x)

    return pd.to_numeric(s.apply(parse_value), errors='coerce')


def clean_data(df):
    """Pipeline dọn dẹp 3 bước."""
    df = df.dropna(how='all').reset_index(drop=True)

    # Strip whitespace & normalize NaN
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace(
            ['nan', 'None', 'NaN', '', 'NaT', 'null', 'NULL', 'N/A', 'n/a', '#N/A', '-'],
            pd.NA
        )

    # Ép kiểu số
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]) or pd.api.types.is_numeric_dtype(df[col]):
            continue
        converted = force_numeric(df[col])
        valid_orig = df[col].notna().sum()
        valid_conv = converted.notna().sum()
        if valid_orig > 0 and (valid_conv / valid_orig) > 0.3:
            df[col] = converted

    # Tự động nhận diện cột ngày tháng
    datetime_keywords = ['ngày', 'ngay', 'date', 'thời gian', 'thoi gian', 'time',
                         'order_date', 'created', 'đặt hàng', 'dat hang']
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]) or pd.api.types.is_datetime64_any_dtype(df[col]):
            continue
        col_lower = col.lower()
        if any(kw in col_lower for kw in datetime_keywords):
            parsed = pd.to_datetime(df[col], errors='coerce', dayfirst=True)
            if parsed.notna().sum() > 0:
                df[col] = parsed

    return df


# ═══════════════════════════════════════════════════════════════
# SHOPEE COLUMN MAPPING — Fuzzy tìm cột
# ═══════════════════════════════════════════════════════════════
def find_col(df, keywords, prefer_numeric=True):
    """Tìm cột trong DataFrame có tên chứa bất kỳ keyword nào."""
    for kw in keywords:
        for col in df.columns:
            if kw.lower() in col.lower():
                if prefer_numeric and not pd.api.types.is_numeric_dtype(df[col]):
                    continue
                return col
    # Retry không kiểm tra numeric
    if prefer_numeric:
        return find_col(df, keywords, prefer_numeric=False)
    return None


def map_shopee_columns(df):
    """
    Mapping thông minh: Tự tìm các cột Shopee dù tên có bị khác nhau.
    Trả về dict roles.
    """
    roles = {}

    # ── Doanh thu (GMV) ──
    roles['revenue'] = find_col(df, [
        'số tiền người mua thanh toán', 'người mua thanh toán',
        'grand total', 'doanh thu', 'tổng tiền', 'thành tiền',
        'total payment', 'order amount', 'amount'
    ])

    # ── Các loại phí sàn ──
    roles['fee_fixed'] = find_col(df, [
        'phí cố định', 'phi co dinh', 'fixed fee', 'commission'
    ])
    roles['fee_service'] = find_col(df, [
        'phí dịch vụ', 'phi dich vu', 'service fee'
    ])
    roles['fee_payment'] = find_col(df, [
        'phí thanh toán', 'phi thanh toan', 'payment fee', 'transaction fee'
    ])
    roles['fee_freeship'] = find_col(df, [
        'phí freeship extra', 'freeship', 'phí vận chuyển', 'shipping fee'
    ])

    # ── Trạng thái ──
    roles['status'] = find_col(df, [
        'trạng thái đơn hàng', 'trang thai don hang', 'trạng thái',
        'trang thai', 'order status', 'status'
    ], prefer_numeric=False)

    # ── Thời gian ──
    roles['date'] = find_col(df, [
        'thời gian đặt hàng', 'thoi gian dat hang',
        'ngày đặt hàng', 'ngay dat hang',
        'order date', 'created date', 'ngày tạo', 'ngay tao',
        'thời gian tạo đơn', 'thoi gian tao don'
    ], prefer_numeric=False)

    # ── Sản phẩm ──
    roles['product'] = find_col(df, [
        'tên sản phẩm', 'ten san pham', 'sku phân loại', 'sku phan loai',
        'product name', 'item name', 'sản phẩm', 'san pham', 'product'
    ], prefer_numeric=False)

    # ── Mã đơn hàng ──
    roles['order_id'] = find_col(df, [
        'mã đơn hàng', 'ma don hang', 'order id', 'order no',
        'mã đơn', 'ma don'
    ], prefer_numeric=False)

    # Loại bỏ None
    roles = {k: v for k, v in roles.items() if v is not None}

    return roles


# ═══════════════════════════════════════════════════════════════
# CHART PALETTE
# ═══════════════════════════════════════════════════════════════
COLORS = ['#EE4D2D', '#2980B9', '#27AE60', '#F39C12', '#8E44AD',
          '#1ABC9C', '#E74C3C', '#3498DB', '#E67E22', '#16A085']
PX_TEMPLATE = 'plotly_white'


# ═══════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🛒 Shopee Analytics")
    st.markdown("---")

    lang_choice = st.radio("🌐", ["🇻🇳 Tiếng Việt", "🇬🇧 English"], horizontal=True, label_visibility="collapsed")
    lang = "EN" if "English" in lang_choice else "VN"

    st.markdown("---")
    st.markdown(f"### 📁 {t('Tải lên file dữ liệu')}")
    uploaded_file = st.file_uploader(
        t("Tải lên file dữ liệu"),
        type=['xlsx', 'xls', 'csv'],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown("**👤 Hồ Anh Khoa**")
    st.caption("v4.0 — Shopee Revenue Analytics")

# Disclaimer
st.warning(f"⚖️ {t('DỰ ÁN CÁ NHÂN: Công cụ phân tích doanh thu Shopee mã nguồn mở. Các phân tích chỉ mang tính chất tham khảo.')}")
st.markdown(f"<p style='font-size: 15px; margin-top: -5px; padding-left: 15px;'>👉 {t('Nếu bạn muốn xem thêm dự án khác hãy')} <a href='https://portfolio-394g.vercel.app' target='_blank' style='text-decoration: underline; color: #1f77b4;'>{t('nhấp vào đây')}</a></p>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# EMPTY STATE
# ═══════════════════════════════════════════════════════════════
if uploaded_file is None:
    st.markdown('<p class="suite-title">🛒 SHOPEE REVENUE ANALYTICS</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="suite-subtitle">{t("Phân tích doanh thu, phí sàn, và hành vi đơn hàng từ Shopee Seller Center")}</p>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="empty-state">
        <div class="icon">📂</div>
        <h3>{t('Chào mừng đến với Shopee Revenue Analytics')}</h3>
        <p>{t('Tải lên file xuất từ Shopee Seller Center để bắt đầu phân tích.')}</p>
        <br/>
    </div>
    """, unsafe_allow_html=True)
    
    # ── Tải File Mẫu & Portfolio ──
    try:
        with open('shopee_sample_data.xlsx', 'rb') as f:
            sample_data = f.read()
        col1, col2, col3 = st.columns([1, 1.5, 1])
        with col2:
            st.download_button(
                label=f"📥 {t('Tải File Dữ Liệu Shopee Mẫu (Excel)')}",
                data=sample_data,
                file_name="shopee_sample_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
            st.markdown(
                f"<p style='text-align:center; font-size:14px; margin-top: 8px;'>"
                f"👨‍💻 <b>{t('Phát triển bởi Hồ Anh Khoa')}</b> <br> <a href='https://portfolio-394g.vercel.app' target='_blank' style='color:#16A085; text-decoration:none; font-weight:700;'>👉 {t('Nhấp vào đây để xem thêm các dự án Portfolio khác')}</a>"
                f"</p>", 
                unsafe_allow_html=True
            )
    except FileNotFoundError:
        pass

    st.stop()


# ═══════════════════════════════════════════════════════════════
# DATA LOADING
# ═══════════════════════════════════════════════════════════════
@st.cache_data
def load_file(file):
    name = file.name.lower()
    try:
        if name.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        df = df.dropna(how='all')
        return clean_data(df), None
    except Exception as e:
        return None, str(e)

df_raw, load_error = load_file(uploaded_file)

if load_error:
    st.error(f"❌ Lỗi đọc file: {load_error}")
    st.stop()
if df_raw is None or df_raw.empty:
    st.warning("⚠️ File không chứa dữ liệu!")
    st.stop()

# Auto-capture sample structure for AI
try:
    df_raw.head(20).to_csv('captured_shopee_sample.csv', index=False)
except:
    pass


# ═══════════════════════════════════════════════════════════════
# COLUMN MAPPING
# ═══════════════════════════════════════════════════════════════
roles = map_shopee_columns(df_raw)
num_cols = df_raw.select_dtypes(include=['number']).columns.tolist()
cat_cols = df_raw.select_dtypes(include=['object', 'category']).columns.tolist()

# Nếu không có cột ngày → chưa parse, thử heuristic
if 'date' not in roles:
    for col in df_raw.columns:
        if pd.api.types.is_datetime64_any_dtype(df_raw[col]):
            roles['date'] = col
            break

# Nếu vẫn không có revenue → fallback: cột số có tổng lớn nhất
if 'revenue' not in roles and num_cols:
    sums = {c: df_raw[c].sum() for c in num_cols}
    roles['revenue'] = max(sums, key=sums.get)


# ═══════════════════════════════════════════════════════════════
# SIDEBAR — DYNAMIC FILTERS
# ═══════════════════════════════════════════════════════════════
df = df_raw.copy()

with st.sidebar:
    st.markdown(f"### 🎛️ {t('Bộ Lọc')}")

    # Filter: Trạng thái đơn hàng
    if 'status' in roles:
        sc = roles['status']
        statuses = [t('Tất cả')] + sorted(df[sc].dropna().unique().tolist())
        sel_status = st.selectbox(t("Trạng thái đơn hàng"), statuses, format_func=t)
        if sel_status != t('Tất cả'):
            df = df[df[sc] == sel_status]

    # Filter: Khoảng ngày
    if 'date' in roles:
        dc = roles['date']
        valid_dates = df[dc].dropna()
        if not valid_dates.empty and pd.api.types.is_datetime64_any_dtype(valid_dates):
            min_d = valid_dates.min().date()
            max_d = valid_dates.max().date()
            date_range = st.date_input(t("📅 Khoảng ngày"), value=(min_d, max_d), min_value=min_d, max_value=max_d)
            if len(date_range) == 2:
                df = df[df[dc].dt.date.between(date_range[0], date_range[1])]

    st.caption(f"📋 {t('Hiển thị:')} **{len(df):,}** / {len(df_raw):,} {t('dòng')}")


# ═══════════════════════════════════════════════════════════════
# SAFETY CHECK
# ═══════════════════════════════════════════════════════════════
num_cols_filtered = df.select_dtypes(include=['number']).columns.tolist()

if not num_cols_filtered:
    st.error("⚠️ Không tìm thấy cột số trong file. Kiểm tra lại định dạng.")
    st.dataframe(df.dtypes.rename("Type").reset_index().rename(columns={"index": "Column"}))
    st.stop()


# ═══════════════════════════════════════════════════════════════
# CALCULATED METRICS
# ═══════════════════════════════════════════════════════════════
rev_col = roles.get('revenue', num_cols_filtered[0])
total_gmv = df[rev_col].sum() if rev_col in df.columns else 0

# Tổng phí sàn = sum tất cả cột phí tìm được
fee_cols = [roles.get(k) for k in ['fee_fixed', 'fee_service', 'fee_payment', 'fee_freeship'] if roles.get(k) and roles.get(k) in df.columns]
total_fees = sum(df[c].fillna(0).abs().sum() for c in fee_cols) if fee_cols else 0

# Doanh thu thực nhận
net_revenue = total_gmv - total_fees

# Tỷ lệ phí sàn
fee_ratio = (total_fees / total_gmv * 100) if total_gmv > 0 else 0

# Tỷ lệ đơn hủy/hoàn
cancel_rate = 0
if 'status' in roles:
    sc = roles['status']
    total_orders = df[sc].notna().sum()
    cancel_keywords = ['hủy', 'huy', 'cancel', 'hoàn', 'hoan', 'trả hàng', 'tra hang', 'return', 'refund']
    cancelled = df[sc].astype(str).str.lower().apply(
        lambda x: any(kw in x for kw in cancel_keywords)
    ).sum()
    cancel_rate = (cancelled / total_orders * 100) if total_orders > 0 else 0


# ═══════════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════
# TITLE
# ═══════════════════════════════════════════════════════════════
st.markdown('<p class="suite-title">🛒 SHOPEE REVENUE ANALYTICS</p>', unsafe_allow_html=True)
st.markdown(f'<p class="suite-subtitle">📁 {uploaded_file.name} — {len(df):,} {t("dòng")} × {len(df.columns)} {t("cột")}</p>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# HÀNG 1: 4 KPI CARDS
# ═══════════════════════════════════════════════════════════════
st.markdown(f"### {t('Chỉ Số Tổng Quan')}")
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">💰</div>
        <p class="kpi-label">{t('Tổng Doanh Thu (GMV)')}</p>
        <p class="kpi-value orange">{fmt(total_gmv)}</p>
        <p class="kpi-sub">{rev_col}</p>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">✅</div>
        <p class="kpi-label">{t('Doanh Thu Thực Nhận')}</p>
        <p class="kpi-value green">{fmt(net_revenue)}</p>
        <p class="kpi-sub">{fee_ratio:.1f}% phí sàn</p>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">🏷️</div>
        <p class="kpi-label">{t('Tổng Phí Sàn')}</p>
        <p class="kpi-value red">{fmt(total_fees)}</p>
        <p class="kpi-sub">{len(fee_cols)} loại phí</p>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">📦</div>
        <p class="kpi-label">{t('Tỷ Lệ Đơn Hủy/Hoàn')}</p>
        <p class="kpi-value blue">{cancel_rate:.1f}%</p>
        <p class="kpi-sub">{cancelled if 'status' in roles else 0}/{total_orders if 'status' in roles else len(df)} đơn</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()


# ═══════════════════════════════════════════════════════════════
# CHART ENGINE — Chỉ vẽ khi dữ liệu đủ điều kiện
# ═══════════════════════════════════════════════════════════════
charts_rendered = 0


# ── HÀNG 2: Area Chart + Stacked Bar (2 cột) ──
if 'date' in roles and roles['date'] in df.columns:
    if not pd.api.types.is_datetime64_any_dtype(df[roles['date']]):
        df[roles['date']] = pd.to_datetime(df[roles['date']], errors='coerce', dayfirst=True)

is_valid_date = ('date' in roles and roles['date'] in df.columns and pd.api.types.is_datetime64_any_dtype(df[roles['date']]))
has_area = (is_valid_date and rev_col in df.columns)
has_stacked = (is_valid_date and fee_cols)

if has_area or has_stacked:
    st.markdown(f"### 📈 {t('Xu Hướng & So Sánh')}")
    h2c1, h2c2 = st.columns(2)

    if has_area:
        with h2c1:
            dc = roles['date']
            # Tính net revenue theo ngày
            daily = df.groupby(df[dc].dt.date).agg({rev_col: 'sum'}).reset_index()
            daily.columns = ['Ngày', rev_col]

            if fee_cols:
                fee_daily = df.groupby(df[dc].dt.date)[fee_cols].sum().abs().sum(axis=1).reset_index()
                fee_daily.columns = ['Ngày', 'Phí sàn']
                daily = daily.merge(fee_daily, on='Ngày', how='left')
                daily['Net Revenue'] = daily[rev_col] - daily['Phí sàn'].fillna(0)
                y_col = 'Net Revenue'
            else:
                y_col = rev_col

            daily = daily.sort_values('Ngày')
            fig = px.area(daily, x='Ngày', y=y_col, template=PX_TEMPLATE, color_discrete_sequence=['#27AE60'])
            fig.update_traces(line=dict(width=2, color='#27AE60'), fillcolor='rgba(39,174,96,0.15)')
            fig.update_layout(
                title=dict(text=f"📈 {t('Xu Hướng Doanh Thu Thực Nhận')} {t('theo ngày')}", font=dict(size=14, color='#1A5276')),
                height=420, hovermode='x unified', margin=dict(l=20, r=20, t=50, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)
            charts_rendered += 1

    if has_stacked:
        col_target = h2c2 if has_area else h2c1
        with col_target:
            dc = roles['date']
            daily_rev = df.groupby(df[dc].dt.date).agg({rev_col: 'sum'}).reset_index()
            daily_rev.columns = ['Ngày', 'Doanh thu']
            daily_fee = df.groupby(df[dc].dt.date)[fee_cols].sum().abs().sum(axis=1).reset_index()
            daily_fee.columns = ['Ngày', 'Phí sàn']
            combined = daily_rev.merge(daily_fee, on='Ngày', how='left').sort_values('Ngày')

            fig = go.Figure()
            fig.add_trace(go.Bar(name=t('Doanh thu'), x=combined['Ngày'], y=combined['Doanh thu'],
                                 marker_color='#EE4D2D'))
            fig.add_trace(go.Bar(name=t('Phí sàn'), x=combined['Ngày'], y=combined['Phí sàn'],
                                 marker_color='#E74C3C'))
            fig.update_layout(
                barmode='stack', template=PX_TEMPLATE,
                title=dict(text=f"📊 {t('Doanh Thu vs Phí Sàn theo Ngày')}", font=dict(size=14, color='#1A5276')),
                height=420,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                margin=dict(l=20, r=20, t=60, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)
            charts_rendered += 1

    st.divider()


# ── HÀNG 3: Pie Chart (Phí) + Top 10 Sản phẩm ──
has_pie = len(fee_cols) >= 2
has_top10 = ('product' in roles and roles['product'] in df.columns and rev_col in df.columns)

if has_pie or has_top10:
    st.markdown(f"### 🔍 {t('Phân Tích Chi Tiết')}")
    h3c1, h3c2 = st.columns(2)

    if has_pie:
        with h3c1:
            fee_labels = []
            fee_values = []
            fee_name_map = {
                'fee_fixed': t('Phí cố định'),
                'fee_service': t('Phí dịch vụ'),
                'fee_payment': t('Phí thanh toán'),
                'fee_freeship': t('Phí Freeship'),
            }
            for key in ['fee_fixed', 'fee_service', 'fee_payment', 'fee_freeship']:
                if roles.get(key) and roles[key] in df.columns:
                    val = df[roles[key]].fillna(0).abs().sum()
                    if val > 0:
                        fee_labels.append(fee_name_map.get(key, roles[key]))
                        fee_values.append(val)

            if fee_labels:
                fee_df = pd.DataFrame({'Loại phí': fee_labels, 'Số tiền': fee_values})
                fig = px.pie(fee_df, names='Loại phí', values='Số tiền', hole=0.5,
                             template=PX_TEMPLATE, color_discrete_sequence=COLORS)
                fig.update_traces(textinfo='label+percent', textfont=dict(size=12),
                                  hovertemplate='%{label}<br>%{value:,.0f}<br>%{percent}')
                fig.update_layout(
                    title=dict(text=f"🥧 {t('Tỷ Trọng Các Loại Phí')}", font=dict(size=14, color='#1A5276')),
                    height=420, showlegend=False, margin=dict(l=10, r=10, t=50, b=10)
                )
                st.plotly_chart(fig, use_container_width=True)
                charts_rendered += 1

    if has_top10:
        col_target = h3c2 if has_pie else h3c1
        with col_target:
            pc = roles['product']
            top10 = df.groupby(pc)[rev_col].sum().nlargest(10).reset_index()
            top10 = top10.sort_values(rev_col, ascending=True)
            fig = px.bar(top10, x=rev_col, y=pc, orientation='h',
                         template=PX_TEMPLATE, color_discrete_sequence=['#2980B9'],
                         text=top10[rev_col].apply(fmt))
            fig.update_traces(textposition='outside', textfont=dict(size=10, color='#566573'))
            fig.update_layout(
                title=dict(text=f"🏆 {t('Top 10 Sản Phẩm Doanh Thu Cao Nhất')}", font=dict(size=14, color='#1A5276')),
                height=420, yaxis_title="", xaxis_title="", margin=dict(l=10, r=40, t=50, b=10)
            )
            st.plotly_chart(fig, use_container_width=True)
            charts_rendered += 1

    st.divider()


# ── HÀNG 4: Đơn theo khung giờ + Trạng thái ──
has_hourly = ('date' in roles and roles['date'] in df.columns and pd.api.types.is_datetime64_any_dtype(df[roles['date']]))
has_status_chart = ('status' in roles and roles['status'] in df.columns and df[roles['status']].nunique() >= 2)

if has_hourly or has_status_chart:
    st.markdown(f"### 🕐 {t('Phân Tích Hành Vi')}")
    h4c1, h4c2 = st.columns(2)

    if has_hourly:
        with h4c1:
            dc = roles['date']
            hours = df[dc].dropna().dt.hour
            if not hours.empty:
                hour_counts = hours.value_counts().reindex(range(24), fill_value=0).reset_index()
                hour_counts.columns = ['Giờ', 'Số đơn']
                # Highlight giờ vàng
                peak_hour = hour_counts.loc[hour_counts['Số đơn'].idxmax(), 'Giờ']
                colors_h = ['#EE4D2D' if h == peak_hour else '#BDC3C7' for h in hour_counts['Giờ']]

                fig = go.Figure(go.Bar(
                    x=hour_counts['Giờ'], y=hour_counts['Số đơn'],
                    marker_color=colors_h,
                    text=hour_counts['Số đơn'], textposition='outside',
                    textfont=dict(size=9)
                ))
                fig.update_layout(
                    template=PX_TEMPLATE,
                    title=dict(text=f"🕐 {t('Đơn Hàng Theo Khung Giờ')} — {t('Giờ vàng')}: {int(peak_hour)}h",
                               font=dict(size=14, color='#1A5276')),
                    height=420, xaxis_title="Giờ (0h-23h)", yaxis_title="Số đơn",
                    xaxis=dict(tickmode='linear', tick0=0, dtick=1),
                    margin=dict(l=20, r=20, t=50, b=20)
                )
                st.plotly_chart(fig, use_container_width=True)
                charts_rendered += 1

    if has_status_chart:
        col_target = h4c2 if has_hourly else h4c1
        with col_target:
            sc = roles['status']
            status_counts = df[sc].value_counts().reset_index()
            status_counts.columns = ['Trạng thái', 'Số đơn']
            fig = px.pie(status_counts, names='Trạng thái', values='Số đơn', hole=0.5,
                         template=PX_TEMPLATE, color_discrete_sequence=COLORS)
            fig.update_traces(textinfo='label+percent', textfont=dict(size=11))
            fig.update_layout(
                title=dict(text=f"📦 {t('Trạng Thái Đơn Hàng')}", font=dict(size=14, color='#1A5276')),
                height=420, showlegend=False, margin=dict(l=10, r=10, t=50, b=10)
            )
            st.plotly_chart(fig, use_container_width=True)
            charts_rendered += 1

    st.divider()


# ═══════════════════════════════════════════════════════════════
# FALLBACK: Nếu chưa có biểu đồ nào → generic charts
# ═══════════════════════════════════════════════════════════════
if charts_rendered == 0:
    st.markdown("### 📊 Phân Tích Tổng Quan")
    fc1, fc2 = st.columns(2)

    with fc1:
        # Bar chart: tổng từng cột số
        bar_data = pd.DataFrame({
            'Cột': num_cols_filtered[:6],
            'Tổng': [df[c].sum() for c in num_cols_filtered[:6]]
        })
        fig = px.bar(bar_data, x='Cột', y='Tổng', template=PX_TEMPLATE,
                     color='Cột', color_discrete_sequence=COLORS, text_auto='.2s')
        fig.update_layout(title="📊 Tổng giá trị từng cột số", height=420, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    if len(num_cols_filtered) >= 2:
        with fc2:
            # Scatter
            scatter_df = df[[num_cols_filtered[0], num_cols_filtered[1]]].dropna()
            fig = px.scatter(scatter_df, x=num_cols_filtered[0], y=num_cols_filtered[1],
                             template=PX_TEMPLATE, color_discrete_sequence=COLORS, opacity=0.7)
            fig.update_layout(title=f"🔗 {num_cols_filtered[0]} vs {num_cols_filtered[1]}", height=420)
            st.plotly_chart(fig, use_container_width=True)

    st.divider()


# ═══════════════════════════════════════════════════════════════
# RAW DATA + DOWNLOAD
# ═══════════════════════════════════════════════════════════════
with st.expander(f"📋 {t('Dữ Liệu Gốc')} — {t('Xem dữ liệu chi tiết')} ({len(df):,} {t('dòng')})"):
    st.dataframe(df, use_container_width=True, height=350)
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label=f"⬇️ {t('Tải xuống CSV')}",
        data=csv,
        file_name=f"shopee_analytics_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime='text/csv'
    )

# Debug
with st.expander("🔧 Debug: Column Mapping"):
    st.json(roles)
    st.caption("Kiểu dữ liệu:")
    st.dataframe(df.dtypes.rename("Type").reset_index().rename(columns={"index": "Column"}))
