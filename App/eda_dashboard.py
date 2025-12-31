"""
Streamlit Dashboard: Phân tích Nhóm Bệnh lý theo Đặc điểm Nhân khẩu học
File: eda_dashboard.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Thiết lập trang
st.set_page_config(
    page_title="Phân tích Nhóm Bệnh lý theo Đặc điểm Nhân khẩu học",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Thiết lập font cho matplotlib để hiển thị tiếng Việt
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# Hàm load dữ liệu với caching
@st.cache_data
def load_data():
    """Load dữ liệu từ file CSV"""
    try:
        df = pd.read_csv('result.csv', encoding='utf-8')
        # Làm sạch dữ liệu
        important_cols = ['gioi_tinh', 'nhom_tuoi', 'chuan_doan']
        df_clean = df.dropna(subset=important_cols).copy()
        return df_clean
    except FileNotFoundError:
        st.error("❌ Không tìm thấy file 'result.csv'. Vui lòng đảm bảo file nằm trong cùng thư mục với script này.")
        return None
    except Exception as e:
        st.error(f"❌ Lỗi khi đọc dữ liệu: {e}")
        return None

# Load dữ liệu
df = load_data()

if df is None:
    st.stop()

# Sidebar điều hướng
st.sidebar.title("🏥 Điều hướng")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Chọn phần phân tích:",
    [
        "📊 Tổng quan",
        "👥 Phân bố Nhân khẩu học",
        "🔝 Top Bệnh lý",
        "⚕️ Bệnh lý theo Giới tính",
        "📅 Bệnh lý theo Nhóm tuổi",
        "🔀 Phân tích Kết hợp",
        "📈 Tỷ lệ và Tỷ suất",
        "📋 Tổng kết"
    ]
)

# Header
st.markdown('<h1 class="main-header">🏥 Phân tích Nhóm Bệnh lý theo Đặc điểm Nhân khẩu học</h1>', unsafe_allow_html=True)
st.markdown("---")

# Biến dùng chung
age_order = ['Trẻ em', 'Thanh niên', 'Trung niên', 'Cao tuổi']
colors_gender = ['#3498db', '#e74c3c']  # Nam, Nữ
colors_age = ['#f39c12', '#2ecc71', '#3498db', '#9b59b6']  # 4 nhóm tuổi

# ============================================================================
# TRANG 1: TỔNG QUAN
# ============================================================================
if page == "📊 Tổng quan":
    st.header("📊 Tổng quan Dữ liệu")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Tổng số hồ sơ", f"{len(df):,}")
    
    with col2:
        st.metric("Số loại bệnh lý", f"{df['chuan_doan'].nunique()}")
    
    with col3:
        nam_count = len(df[df['gioi_tinh'] == 'Nam'])
        st.metric("Bệnh nhân Nam", f"{nam_count:,}")
    
    with col4:
        nu_count = len(df[df['gioi_tinh'] == 'Nữ'])
        st.metric("Bệnh nhân Nữ", f"{nu_count:,}")
    
    st.markdown("---")
    
    # Thông tin về dữ liệu
    st.subheader("📋 Thông tin cơ bản về dữ liệu")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Các cột trong dữ liệu:**")
        cols_df = pd.DataFrame({'Cột': df.columns.tolist()})
        st.dataframe(cols_df, use_container_width=True, hide_index=True)
        
        st.write("**Thống kê dữ liệu thiếu:**")
        missing_info = df[['gioi_tinh', 'nhom_tuoi', 'chuan_doan']].isnull().sum()
        missing_df = pd.DataFrame({
            'Cột': missing_info.index,
            'Số lượng thiếu': missing_info.values,
            'Tỷ lệ (%)': (missing_info.values / len(df) * 100).round(2)
        })
        st.dataframe(missing_df, use_container_width=True, hide_index=True)
    
    with col2:
        st.write("**5 dòng đầu tiên:**")
        st.dataframe(df.head(), use_container_width=True)
        
        st.write("**Giá trị duy nhất:**")
        st.write(f"- **Giới tính:** {', '.join(df['gioi_tinh'].unique().tolist())}")
        st.write(f"- **Nhóm tuổi:** {', '.join(df['nhom_tuoi'].unique().tolist())}")
        st.write(f"- **Số loại chẩn đoán:** {df['chuan_doan'].nunique()}")

# ============================================================================
# TRANG 2: PHÂN BỐ NHÂN KHẨU HỌC
# ============================================================================
elif page == "👥 Phân bố Nhân khẩu học":
    st.header("👥 Phân bố Nhân khẩu học")
    
    # Phân bố theo giới tính
    st.subheader("📊 Phân bố theo Giới tính")
    
    col1, col2 = st.columns(2)
    
    with col1:
        gender_counts = df['gioi_tinh'].value_counts()
        fig, ax = plt.subplots(figsize=(8, 6))
        bars = ax.bar(gender_counts.index, gender_counts.values, color=colors_gender)
        ax.set_title('Phân bố bệnh nhân theo Giới tính', fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('Giới tính', fontsize=12)
        ax.set_ylabel('Số lượng', fontsize=12)
        for i, v in enumerate(gender_counts.values):
            ax.text(i, v, f'{v:,}', ha='center', va='bottom', fontweight='bold', fontsize=11)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.pie(gender_counts.values, labels=gender_counts.index, autopct='%1.1f%%',
               colors=colors_gender, startangle=90, textprops={'fontsize': 12, 'fontweight': 'bold'})
        ax.set_title('Tỷ lệ bệnh nhân theo Giới tính', fontsize=14, fontweight='bold', pad=20)
        plt.tight_layout()
        st.pyplot(fig)
    
    # Hiển thị số liệu
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(gender_counts.to_frame('Số lượng'), use_container_width=True)
    
    st.markdown("---")
    
    # Phân bố theo nhóm tuổi
    st.subheader("📅 Phân bố theo Nhóm tuổi")
    
    col1, col2 = st.columns(2)
    
    with col1:
        age_counts = df['nhom_tuoi'].value_counts().reindex(age_order)
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(range(len(age_counts)), age_counts.values, color=colors_age)
        ax.set_xticks(range(len(age_counts)))
        ax.set_xticklabels(age_counts.index, rotation=45, ha='right', fontsize=11)
        ax.set_title('Phân bố bệnh nhân theo Nhóm tuổi', fontsize=14, fontweight='bold', pad=20)
        ax.set_ylabel('Số lượng', fontsize=12)
        for i, v in enumerate(age_counts.values):
            ax.text(i, v, f'{v:,}', ha='center', va='bottom', fontweight='bold', fontsize=11)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.pie(age_counts.values, labels=age_counts.index, autopct='%1.1f%%',
               colors=colors_age, startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'})
        ax.set_title('Tỷ lệ bệnh nhân theo Nhóm tuổi', fontsize=14, fontweight='bold', pad=20)
        plt.tight_layout()
        st.pyplot(fig)
    
    # Hiển thị số liệu
    col1, col2 = st.columns(2)
    with col1:
        age_counts_df = age_counts.to_frame('Số lượng')
        age_counts_df['Tỷ lệ (%)'] = (age_counts_df['Số lượng'] / len(df) * 100).round(2)
        st.dataframe(age_counts_df, use_container_width=True)
    
    st.markdown("---")
    
    # Ma trận phân bố kết hợp
    st.subheader("🔀 Ma trận Phân bố: Nhóm tuổi × Giới tính")
    
    pivot_data = pd.crosstab(df['nhom_tuoi'], df['gioi_tinh'])
    pivot_data = pivot_data.reindex(age_order)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(pivot_data, annot=True, fmt='d', cmap='YlOrRd', 
                cbar_kws={'label': 'Số lượng'}, ax=ax, linewidths=0.5, 
                annot_kws={'fontsize': 11, 'fontweight': 'bold'})
    ax.set_title('Ma trận Phân bố: Nhóm tuổi × Giới tính', fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Giới tính', fontsize=12)
    ax.set_ylabel('Nhóm tuổi', fontsize=12)
    plt.tight_layout()
    st.pyplot(fig)
    
    # Bảng chi tiết
    st.write("**Bảng chi tiết:**")
    pivot_data['Tổng'] = pivot_data.sum(axis=1)
    st.dataframe(pivot_data, use_container_width=True)

# ============================================================================
# TRANG 3: TOP BỆNH LÝ
# ============================================================================
elif page == "🔝 Top Bệnh lý":
    st.header("🔝 Top Bệnh lý Phổ biến")
    
    n_top = st.slider("Chọn số lượng bệnh lý hiển thị:", 10, 30, 20)
    
    top_diseases = df['chuan_doan'].value_counts().head(n_top)
    top_diseases_df = pd.DataFrame({
        'STT': range(1, len(top_diseases) + 1),
        'Bệnh lý': top_diseases.index,
        'Số lượng': top_diseases.values,
        'Tỷ lệ (%)': (top_diseases.values / len(df) * 100).round(2)
    })
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig, ax = plt.subplots(figsize=(12, max(8, n_top*0.4)))
        bars = ax.barh(range(len(top_diseases)), top_diseases.values, color='steelblue')
        ax.set_yticks(range(len(top_diseases)))
        ax.set_yticklabels(top_diseases.index, fontsize=10)
        ax.set_title(f'Top {n_top} Bệnh lý phổ biến nhất', fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('Số lượng', fontsize=12)
        ax.set_ylabel('Bệnh lý', fontsize=12)
        ax.invert_yaxis()
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        
        # Thêm số liệu trên thanh
        for i, v in enumerate(top_diseases.values):
            ax.text(v, i, f' {v:,}', va='center', fontsize=9, fontweight='bold')
        
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.write("**Bảng Top Bệnh lý:**")
        st.dataframe(top_diseases_df.set_index('STT'), use_container_width=True, height=600)

# ============================================================================
# TRANG 4: BỆNH LÝ THEO GIỚI TÍNH
# ============================================================================
elif page == "⚕️ Bệnh lý theo Giới tính":
    st.header("⚕️ Phân tích Bệnh lý theo Giới tính")
    
    n_top = st.slider("Chọn số lượng bệnh lý hiển thị:", 5, 20, 10)
    
    # Top bệnh lý theo giới tính
    st.subheader(f"🔝 Top {n_top} Bệnh lý theo Giới tính")
    
    col1, col2 = st.columns(2)
    
    for idx, gender in enumerate(['Nam', 'Nữ']):
        with [col1, col2][idx]:
            gender_diseases = df[df['gioi_tinh'] == gender]['chuan_doan'].value_counts().head(n_top)
            
            fig, ax = plt.subplots(figsize=(10, max(6, n_top*0.4)))
            bars = ax.barh(range(len(gender_diseases)), gender_diseases.values, color=colors_gender[idx])
            ax.set_yticks(range(len(gender_diseases)))
            ax.set_yticklabels(gender_diseases.index, fontsize=9)
            ax.set_title(f'Top {n_top} Bệnh lý - {gender}', fontsize=12, fontweight='bold', pad=15)
            ax.set_xlabel('Số lượng', fontsize=11)
            ax.set_ylabel('Bệnh lý', fontsize=11)
            ax.invert_yaxis()
            ax.grid(axis='x', alpha=0.3, linestyle='--')
            
            # Thêm số liệu
            for i, v in enumerate(gender_diseases.values):
                ax.text(v, i, f' {v:,}', va='center', fontsize=8, fontweight='bold')
            
            plt.tight_layout()
            st.pyplot(fig)
            
            # Bảng chi tiết
            gender_df = pd.DataFrame({
                'Bệnh lý': gender_diseases.index,
                'Số lượng': gender_diseases.values,
                'Tỷ lệ (%)': (gender_diseases.values / len(df[df['gioi_tinh'] == gender]) * 100).round(2)
            })
            st.dataframe(gender_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Heatmap
    st.subheader("🔥 Heatmap: Bệnh lý × Giới tính")
    
    top_15_diseases = df['chuan_doan'].value_counts().head(15).index
    disease_gender = pd.crosstab(
        df[df['chuan_doan'].isin(top_15_diseases)]['chuan_doan'],
        df[df['chuan_doan'].isin(top_15_diseases)]['gioi_tinh']
    )
    
    fig, ax = plt.subplots(figsize=(6, 10))
    sns.heatmap(disease_gender, annot=True, fmt='d', cmap='YlOrRd', 
                cbar_kws={'label': 'Số lượng'}, ax=ax, linewidths=0.5,
                annot_kws={'fontsize': 9})
    ax.set_title('Ma trận Bệnh lý × Giới tính (Top 15)', fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Giới tính', fontsize=12)
    ax.set_ylabel('Bệnh lý', fontsize=12)
    plt.tight_layout()
    st.pyplot(fig)
    
    # Bảng chi tiết heatmap
    st.dataframe(disease_gender, use_container_width=True)

# ============================================================================
# TRANG 5: BỆNH LÝ THEO NHÓM TUỔI
# ============================================================================
elif page == "📅 Bệnh lý theo Nhóm tuổi":
    st.header("📅 Phân tích Bệnh lý theo Nhóm tuổi")
    
    n_top = st.slider("Chọn số lượng bệnh lý hiển thị:", 5, 15, 10)
    
    # Top bệnh lý theo nhóm tuổi
    st.subheader(f"🔝 Top {n_top} Bệnh lý theo Nhóm tuổi")
    
    cols = st.columns(2)
    
    for idx, age_group in enumerate(age_order):
        with cols[idx % 2]:
            age_diseases = df[df['nhom_tuoi'] == age_group]['chuan_doan'].value_counts().head(n_top)
            color_idx = age_order.index(age_group)
            
            fig, ax = plt.subplots(figsize=(10, max(6, n_top*0.4)))
            bars = ax.barh(range(len(age_diseases)), age_diseases.values, color=colors_age[color_idx])
            ax.set_yticks(range(len(age_diseases)))
            ax.set_yticklabels(age_diseases.index, fontsize=8)
            ax.set_title(f'Top {n_top} Bệnh lý - {age_group}', fontsize=11, fontweight='bold', pad=15)
            ax.set_xlabel('Số lượng', fontsize=10)
            ax.set_ylabel('Bệnh lý', fontsize=10)
            ax.invert_yaxis()
            ax.grid(axis='x', alpha=0.3, linestyle='--')
            
            # Thêm số liệu
            for i, v in enumerate(age_diseases.values):
                ax.text(v, i, f' {v:,}', va='center', fontsize=8, fontweight='bold')
            
            plt.tight_layout()
            st.pyplot(fig)
            
            # Bảng chi tiết
            age_df = pd.DataFrame({
                'Bệnh lý': age_diseases.index,
                'Số lượng': age_diseases.values,
                'Tỷ lệ (%)': (age_diseases.values / len(df[df['nhom_tuoi'] == age_group]) * 100).round(2)
            })
            st.dataframe(age_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Stacked bar chart
    st.subheader("📊 Stacked Bar Chart: Top Bệnh lý theo Nhóm tuổi")
    
    top_10_diseases = df['chuan_doan'].value_counts().head(10).index
    disease_age = pd.crosstab(
        df[df['chuan_doan'].isin(top_10_diseases)]['chuan_doan'],
        df[df['chuan_doan'].isin(top_10_diseases)]['nhom_tuoi']
    )
    disease_age = disease_age.reindex(columns=age_order, fill_value=0)
    
    fig, ax = plt.subplots(figsize=(14, 8))
    disease_age.plot(kind='bar', stacked=True, ax=ax, color=colors_age, width=0.8)
    ax.set_title('Top 10 Bệnh lý phân bố theo Nhóm tuổi (Stacked)', fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Bệnh lý', fontsize=12)
    ax.set_ylabel('Số lượng', fontsize=12)
    ax.legend(title='Nhóm tuổi', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
    ax.tick_params(axis='x', rotation=45)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    st.pyplot(fig)
    
    # Bảng chi tiết
    st.write("**Bảng chi tiết:**")
    disease_age['Tổng'] = disease_age.sum(axis=1)
    st.dataframe(disease_age, use_container_width=True)

# ============================================================================
# TRANG 6: PHÂN TÍCH KẾT HỢP
# ============================================================================
elif page == "🔀 Phân tích Kết hợp":
    st.header("🔀 Phân tích Bệnh lý theo Giới tính và Nhóm tuổi (Kết hợp)")
    
    n_top = st.slider("Chọn số lượng bệnh lý hiển thị:", 5, 15, 10)
    
    top_diseases = df['chuan_doan'].value_counts().head(n_top).index
    
    # Heatmap 3 chiều
    st.subheader("🔥 Heatmap 3 chiều: Bệnh lý × (Giới tính-Nhóm tuổi)")
    
    heatmap_data = df[df['chuan_doan'].isin(top_diseases)].pivot_table(
        values='id',
        index='chuan_doan',
        columns=['gioi_tinh', 'nhom_tuoi'],
        aggfunc='count',
        fill_value=0
    )
    
    # Flatten column names
    heatmap_data.columns = [f'{gender}-{age}' for gender, age in heatmap_data.columns]
    
    fig, ax = plt.subplots(figsize=(12, max(8, n_top*0.5)))
    sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='YlOrRd',
                cbar_kws={'label': 'Số lượng'}, ax=ax, linewidths=0.5,
                annot_kws={'fontsize': 8})
    ax.set_title(f'Heatmap: Bệnh lý × (Giới tính-Nhóm tuổi) - Top {n_top}', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Giới tính - Nhóm tuổi', fontsize=12)
    ax.set_ylabel('Bệnh lý', fontsize=12)
    ax.tick_params(axis='x', rotation=45)
    plt.tight_layout()
    st.pyplot(fig)
    
    st.markdown("---")
    
    # Bảng pivot chi tiết
    st.subheader("📋 Bảng Pivot Chi tiết")
    
    pivot_detail = df[df['chuan_doan'].isin(top_diseases)].groupby(
        ['chuan_doan', 'gioi_tinh', 'nhom_tuoi']
    ).size().unstack(fill_value=0)
    
    # Sắp xếp lại columns theo thứ tự
    if not pivot_detail.empty:
        st.dataframe(pivot_detail, use_container_width=True)
    
    st.markdown("---")
    
    # Facet Grid (nếu số lượng không quá lớn)
    if n_top <= 10:
        st.subheader("📊 Facet Grid: Top Bệnh lý theo Giới tính và Nhóm tuổi")
        
        facet_data = df[df['chuan_doan'].isin(top_diseases)].copy()
        
        # Tạo subplot thủ công vì Streamlit không hỗ trợ FacetGrid trực tiếp
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        axes = axes.ravel()
        
        plot_idx = 0
        for gender in ['Nam', 'Nữ']:
            for age in age_order:
                subset = facet_data[(facet_data['gioi_tinh'] == gender) & 
                                   (facet_data['nhom_tuoi'] == age)]
                disease_counts = subset['chuan_doan'].value_counts().head(5)
                
                if len(disease_counts) > 0:
                    color_idx = age_order.index(age)
                    axes[plot_idx].barh(range(len(disease_counts)), disease_counts.values,
                                       color=colors_age[color_idx])
                    axes[plot_idx].set_yticks(range(len(disease_counts)))
                    axes[plot_idx].set_yticklabels(disease_counts.index, fontsize=7)
                    axes[plot_idx].set_title(f'{gender} - {age}', fontsize=10, fontweight='bold')
                    axes[plot_idx].set_xlabel('Số lượng', fontsize=9)
                    axes[plot_idx].invert_yaxis()
                    axes[plot_idx].grid(axis='x', alpha=0.3, linestyle='--')
                
                plot_idx += 1
        
        plt.suptitle(f'Top 5 Bệnh lý theo Giới tính và Nhóm tuổi', 
                     fontsize=14, fontweight='bold', y=0.995)
        plt.tight_layout()
        st.pyplot(fig)

# ============================================================================
# TRANG 7: TỶ LỆ VÀ TỶ SUẤT
# ============================================================================
elif page == "📈 Tỷ lệ và Tỷ suất":
    st.header("📈 Phân tích Tỷ lệ và Tỷ suất")
    
    st.subheader("📊 Tỷ lệ mắc bệnh theo Giới tính (Theo Nhóm tuổi)")
    
    n_top = st.slider("Chọn số lượng bệnh lý phân tích:", 5, 15, 10)
    top_diseases = df['chuan_doan'].value_counts().head(n_top).index
    
    # Tỷ lệ mắc bệnh
    for age_group in age_order:
        with st.expander(f"🔹 {age_group}", expanded=False):
            age_data = df[df['nhom_tuoi'] == age_group]
            age_top = [d for d in top_diseases if d in age_data['chuan_doan'].values]
            
            ratio_data = []
            for disease in age_top[:5]:
                disease_data = age_data[age_data['chuan_doan'] == disease]
                gender_dist = disease_data['gioi_tinh'].value_counts(normalize=True) * 100
                
                for gender, pct in gender_dist.items():
                    count = disease_data[disease_data['gioi_tinh'] == gender].shape[0]
                    ratio_data.append({
                        'Bệnh lý': disease,
                        'Giới tính': gender,
                        'Số lượng': count,
                        'Tỷ lệ (%)': round(pct, 2)
                    })
            
            if ratio_data:
                ratio_df = pd.DataFrame(ratio_data)
                st.dataframe(ratio_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Normalized stacked bar chart
    st.subheader("📊 Biểu đồ Stacked (Normalized) theo Giới tính")
    
    normalized_data = []
    for disease in top_diseases:
        for gender in ['Nam', 'Nữ']:
            for age in age_order:
                count = len(df[(df['chuan_doan'] == disease) &
                               (df['gioi_tinh'] == gender) &
                               (df['nhom_tuoi'] == age)])
                total = len(df[(df['chuan_doan'] == disease)])
                normalized_data.append({
                    'Bệnh lý': disease,
                    'Giới tính': gender,
                    'Nhóm tuổi': age,
                    'Tỷ lệ': (count/total*100) if total > 0 else 0
                })
    
    norm_df = pd.DataFrame(normalized_data)
    pivot_norm = norm_df.pivot_table(values='Tỷ lệ', index='Bệnh lý',
                                     columns=['Giới tính', 'Nhóm tuổi'], fill_value=0)
    
    col1, col2 = st.columns(2)
    
    for idx, gender in enumerate(['Nam', 'Nữ']):
        with [col1, col2][idx]:
            gender_cols = [col for col in pivot_norm.columns if col[0] == gender]
            if gender_cols:
                gender_data = pivot_norm[gender_cols]
                gender_data.columns = [col[1] for col in gender_cols]
                gender_data = gender_data.reindex(columns=age_order, fill_value=0)
                
                fig, ax = plt.subplots(figsize=(10, 8))
                gender_data.plot(kind='bar', stacked=True, ax=ax,
                                color=colors_age, width=0.8)
                ax.set_title(f'Tỷ lệ mắc bệnh - {gender} (Normalized)', 
                            fontsize=12, fontweight='bold', pad=20)
                ax.set_xlabel('Bệnh lý', fontsize=11)
                ax.set_ylabel('Tỷ lệ (%)', fontsize=11)
                ax.legend(title='Nhóm tuổi', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
                ax.tick_params(axis='x', rotation=45)
                ax.grid(axis='y', alpha=0.3, linestyle='--')
                plt.tight_layout()
                st.pyplot(fig)

# ============================================================================
# TRANG 8: TỔNG KẾT
# ============================================================================
elif page == "📋 Tổng kết":
    st.header("📋 Tổng kết và Insights")
    
    # Thống kê tổng hợp
    st.subheader("1️⃣ Thống kê Tổng hợp")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Tổng số hồ sơ", f"{len(df):,}")
    with col2:
        st.metric("Số loại bệnh lý", f"{df['chuan_doan'].nunique()}")
    with col3:
        nam_count = len(df[df['gioi_tinh'] == 'Nam'])
        nam_pct = nam_count / len(df) * 100
        st.metric("Bệnh nhân Nam", f"{nam_count:,}", f"{nam_pct:.1f}%")
    with col4:
        nu_count = len(df[df['gioi_tinh'] == 'Nữ'])
        nu_pct = nu_count / len(df) * 100
        st.metric("Bệnh nhân Nữ", f"{nu_count:,}", f"{nu_pct:.1f}%")
    
    st.markdown("---")
    
    # Top 5 bệnh lý
    st.subheader("2️⃣ Top 5 Bệnh lý Phổ biến nhất")
    
    top_5 = df['chuan_doan'].value_counts().head(5)
    top_5_df = pd.DataFrame({
        'STT': range(1, 6),
        'Bệnh lý': top_5.index,
        'Số lượng': top_5.values,
        'Tỷ lệ (%)': (top_5.values / len(df) * 100).round(2)
    })
    st.dataframe(top_5_df.set_index('STT'), use_container_width=True)
    
    # Biểu đồ top 5
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(range(len(top_5)), top_5.values, color='steelblue')
    ax.set_yticks(range(len(top_5)))
    ax.set_yticklabels(top_5.index, fontsize=11)
    ax.set_title('Top 5 Bệnh lý phổ biến nhất', fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Số lượng', fontsize=12)
    ax.set_ylabel('Bệnh lý', fontsize=12)
    ax.invert_yaxis()
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    for i, v in enumerate(top_5.values):
        ax.text(v, i, f' {v:,}', va='center', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    st.pyplot(fig)
    
    st.markdown("---")
    
    # Phát hiện quan trọng
    st.subheader("3️⃣ Phát hiện Quan trọng")
    
    # Khác biệt theo giới tính
    st.write("**🔍 Bệnh lý có sự khác biệt giữa Nam và Nữ:**")
    differences = []
    for disease in top_5.index[:3]:
        gender_dist = df[df['chuan_doan'] == disease]['gioi_tinh'].value_counts(normalize=True)
        if 'Nam' in gender_dist.index and 'Nữ' in gender_dist.index:
            diff = abs(gender_dist['Nam'] - gender_dist['Nữ'])
            if diff > 0.1:  # Chênh lệch > 10%
                differences.append({
                    'Bệnh lý': disease,
                    'Nam (%)': round(gender_dist['Nam'] * 100, 1),
                    'Nữ (%)': round(gender_dist['Nữ'] * 100, 1),
                    'Chênh lệch (%)': round(diff * 100, 1)
                })
    
    if differences:
        diff_df = pd.DataFrame(differences)
        st.dataframe(diff_df, use_container_width=True, hide_index=True)
    else:
        st.info("Không có bệnh lý nào có sự khác biệt rõ rệt giữa Nam và Nữ (>10%) trong top 3 bệnh phổ biến.")
    
    # Khác biệt theo nhóm tuổi
    st.write("**🔍 Bệnh lý có sự khác biệt theo Nhóm tuổi:**")
    age_differences = []
    for disease in top_5.index[:3]:
        age_dist = df[df['chuan_doan'] == disease]['nhom_tuoi'].value_counts(normalize=True)
        if len(age_dist) > 0:
            dominant_age = age_dist.idxmax()
            age_differences.append({
                'Bệnh lý': disease,
                'Nhóm tuổi phổ biến nhất': dominant_age,
                'Tỷ lệ (%)': round(age_dist[dominant_age] * 100, 1)
            })
    
    if age_differences:
        age_diff_df = pd.DataFrame(age_differences)
        st.dataframe(age_diff_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Đề xuất
    st.subheader("4️⃣ Đề xuất")
    st.info("""
    - **Tiếp tục phân tích**: Có thể mở rộng phân tích với các biến khác như tiền sử bệnh, 
      triệu chứng, xét nghiệm
    - **Machine Learning**: Sử dụng dữ liệu này để xây dựng mô hình dự đoán bệnh lý 
      dựa trên đặc điểm nhân khẩu học
    - **Visualization nâng cao**: Có thể tạo interactive charts với Plotly để tăng 
      tính tương tác
    - **Phân tích thời gian**: Nếu có dữ liệu thời gian, có thể phân tích xu hướng 
      bệnh lý theo thời gian
    """)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray; padding: 1rem;'>
        <p>🏥 Phân tích Nhóm Bệnh lý theo Đặc điểm Nhân khẩu học | Streamlit Dashboard</p>
        <p style='font-size: 0.8rem;'>Dữ liệu từ result.csv | {:,} hồ sơ | {:,} loại bệnh lý</p>
    </div>
""".format(len(df), df['chuan_doan'].nunique()), unsafe_allow_html=True)


