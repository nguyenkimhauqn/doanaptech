"""
🏥 STREAMLIT APP - ĐỒ ÁN CUỐI KỲ
Main entry point cho Streamlit Cloud deployment
"""

import streamlit as st
import sys
from pathlib import Path

# Thêm thư mục App vào Python path
app_dir = Path(__file__).parent / "App"
sys.path.insert(0, str(app_dir))

# Thiết lập trang
st.set_page_config(
    page_title="Đồ án Cuối Kỳ - Phân Tích Dữ Liệu Y Tế",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 2rem 0;
    }
    .dashboard-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 5px solid #667eea;
        transition: transform 0.3s ease;
    }
    .dashboard-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 12px rgba(0,0,0,0.15);
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        font-weight: bold;
        font-size: 1.1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🏥 ĐỒ ÁN CUỐI KỲ<br>Phân Tích Dữ Liệu Y Tế</h1>', unsafe_allow_html=True)

st.markdown("---")

# Giới thiệu
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📊 Tổng hồ sơ", "400,000")
with col2:
    st.metric("📈 Số Dashboard", "2")
with col3:
    st.metric("🎯 Phương pháp", "EDA + ML")

st.markdown("---")

# Giới thiệu dự án
st.markdown("""
### 📝 Giới thiệu Dự án

Đồ án này thực hiện **phân tích và khai phá dữ liệu y tế** từ hệ thống quản lý bệnh viện, 
bao gồm 400,000 hồ sơ bệnh nhân với nhiều phương pháp phân tích khác nhau.

**Công nghệ sử dụng:**
- 📊 **EDA (Exploratory Data Analysis)** - 7 bước cơ bản
- 🎯 **KMeans Clustering** - Phân cụm bệnh nhân
- 📉 **PCA (Principal Component Analysis)** - Giảm chiều dữ liệu
- 📈 **Streamlit** - Dashboard tương tác

---
""")

# Chọn dashboard
st.subheader("🎯 Chọn Dashboard để Khám phá")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="dashboard-card">
        <h3>📊 Dashboard 1: Phân Tích Toàn Diện</h3>
        <p><strong>File:</strong> analysis_dashboard.py</p>
        <p><strong>Nội dung:</strong></p>
        <ul>
            <li>✅ EDA - 7 Bước Cơ Bản</li>
            <li>✅ KMeans Clustering</li>
            <li>✅ PCA Analysis</li>
            <li>✅ PCA + KMeans</li>
            <li>✅ So sánh Raw vs PCA</li>
            <li>✅ Insights & Kết luận</li>
        </ul>
        <p><strong>Phù hợp cho:</strong> Phân tích chuyên sâu, Machine Learning</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Mở Dashboard Phân Tích Toàn Diện", key="btn1"):
        st.info("💡 **Hướng dẫn:** Chọn dashboard này bằng cách deploy với Main file path: `App/analysis_dashboard.py`")

with col2:
    st.markdown("""
    <div class="dashboard-card">
        <h3>👥 Dashboard 2: Phân Tích Nhân Khẩu Học</h3>
        <p><strong>File:</strong> eda_dashboard.py</p>
        <p><strong>Nội dung:</strong></p>
        <ul>
            <li>✅ Tổng quan dữ liệu</li>
            <li>✅ Phân bố Nhân khẩu học</li>
            <li>✅ Top Bệnh lý</li>
            <li>✅ Bệnh lý theo Giới tính</li>
            <li>✅ Bệnh lý theo Nhóm tuổi</li>
            <li>✅ Phân tích Kết hợp</li>
        </ul>
        <p><strong>Phù hợp cho:</strong> Phân tích dịch tễ học, Báo cáo nhanh</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Mở Dashboard Nhân Khẩu Học", key="btn2"):
        st.info("💡 **Hướng dẫn:** Chọn dashboard này bằng cách deploy với Main file path: `App/eda_dashboard.py`")

st.markdown("---")

# Hướng dẫn deployment
st.subheader("📚 Hướng dẫn Deployment trên Streamlit Cloud")

st.markdown("""
### 🔧 Cấu hình trên Streamlit Cloud:

1. **Repository:** `nguyenkimhauqn/doanaptech`
2. **Branch:** `main`
3. **Main file path:** Chọn một trong hai:
   - `App/analysis_dashboard.py` ← **Khuyến nghị** (Dashboard đầy đủ)
   - `App/eda_dashboard.py` (Dashboard nhân khẩu học)
   - `streamlit_app.py` (Trang chủ này)

### ✅ Lưu ý quan trọng:

- ✓ File `result.csv` phải nằm trong thư mục `App/` hoặc root
- ✓ File `requirements.txt` phải có đầy đủ thư viện
- ✓ Đảm bảo repository là **Public** hoặc đã kết nối quyền truy cập

### 📦 Các file cần thiết:
- `App/analysis_dashboard.py` ✅
- `App/eda_dashboard.py` ✅
- `App/result.csv` ✅
- `requirements.txt` ✅
""")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray; padding: 1rem;'>
        <p>🏥 <strong>Đồ án Cuối Kỳ - APTECH</strong></p>
        <p>📊 Phân Tích và Khai Phá Dữ Liệu Y Tế | 400,000 hồ sơ</p>
        <p style='font-size: 0.8rem;'>Powered by Streamlit | © 2025</p>
    </div>
""", unsafe_allow_html=True)

