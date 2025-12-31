# 🚀 HƯỚNG DẪN CHẠY STREAMLIT DASHBOARD

## 📋 Yêu cầu

- Python 3.8+
- Đã cài đặt các thư viện trong `requirements.txt`

## 🔧 Cài đặt

### Bước 1: Cài đặt dependencies

```bash
cd /Users/nguyenkimhau/Desktop/APTECH/DoAnCuoiKy/App
pip install -r requirements.txt
```

Hoặc nếu bạn muốn cài từng thư viện:

```bash
pip install streamlit pandas numpy matplotlib seaborn scikit-learn plotly
```

## 🎯 Chạy Dashboard

### Dashboard Phân tích Toàn diện (Mới)

```bash
cd /Users/nguyenkimhau/Desktop/APTECH/DoAnCuoiKy/App
streamlit run analysis_dashboard.py
```

Dashboard này bao gồm:
- 🏠 Tổng quan dự án
- 📊 EDA 7 bước cơ bản
- 🎯 KMeans Clustering
- 🔍 PCA Analysis
- 🔬 PCA + KMeans
- ⚖️ So sánh Raw vs PCA
- 💡 Insights & Kết luận

### Dashboard EDA Cơ bản (Cũ)

```bash
streamlit run eda_dashboard.py
```

Dashboard này tập trung vào:
- Phân tích nhân khẩu học
- Top bệnh lý
- Phân bố theo giới tính và nhóm tuổi

## 🌐 Truy cập Dashboard

Sau khi chạy lệnh, Streamlit sẽ tự động mở browser tại:

```
Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

Nếu không tự động mở, copy URL vào browser.

## 📊 Các Tính năng Chính

### 1. Tổng quan (🏠)
- Thống kê tổng quan dataset
- Preview dữ liệu
- Cấu trúc dữ liệu

### 2. EDA - 7 Bước (📊)
- Đọc và kiểm tra dữ liệu
- Phát hiện missing values
- Phát hiện duplicates
- Phân tích biến phân loại
- Phân tích biến số
- Phát hiện outliers
- Phân tích mối quan hệ

### 3. KMeans Clustering (🎯)
- Elbow Method
- Silhouette Analysis
- Phân bố clusters
- Đặc điểm từng cluster
- Top diagnoses theo cluster

### 4. PCA Analysis (🔍)
- Scree Plot
- Explained Variance
- PC Loadings
- 2D & 3D Visualization

### 5. PCA + KMeans (🔬)
- Clustering trên PCA space
- Visualization clusters
- Cluster profiles

### 6. So sánh Raw vs PCA (⚖️)
- Metrics comparison
- Performance analysis
- Adjusted Rand Index
- Recommendations

### 7. Insights & Kết luận (💡)
- Key findings
- Practical applications
- Limitations
- Future work

## 🎨 Tính năng Interactive

- **Sliders**: Điều chỉnh số lượng clusters, PCs, top items
- **Selectbox**: Chọn columns, clusters, features
- **Charts**: Interactive Plotly charts (zoom, pan, hover)
- **Tabs**: Organized content
- **Expanders**: Collapse/expand sections
- **Filters**: Dynamic filtering

## 💾 Dữ liệu

Dashboard sẽ tự động load file `result.csv` trong cùng thư mục. Đảm bảo file này tồn tại.

Cấu trúc dữ liệu cần:
- 400,000 rows
- 14 columns
- Các cột: id, gioi_tinh, tuoi, ngay_sinh, nhom_tuoi, nhom_mau, thanh_pho, tien_su_benh, trang_thai, trieu_chung, xet_nghiem, ket_qua, loai_kham, chuan_doan

## ⚡ Performance

Dashboard sử dụng `@st.cache_data` để cache:
- Data loading
- Data preprocessing
- KMeans clustering
- PCA transformation

Lần chạy đầu tiên sẽ chậm hơn do cần tính toán, các lần sau sẽ nhanh hơn.

## 🐛 Troubleshooting

### Lỗi: ModuleNotFoundError
```bash
pip install <missing_module>
```

### Lỗi: File not found
Đảm bảo bạn đang ở đúng thư mục `/App` và file `result.csv` tồn tại.

### Dashboard chạy chậm
- Giảm số lượng sample trong visualization (đã tối ưu sẵn)
- Đảm bảo đủ RAM (khuyến nghị 8GB+)
- Close các ứng dụng khác

### Port 8501 đã được sử dụng
```bash
streamlit run analysis_dashboard.py --server.port 8502
```

## 📸 Screenshots

Dashboard sẽ hiển thị:
- Interactive charts (Bar, Pie, Scatter, Box, Violin, Heatmap)
- Metrics cards
- Tables
- 3D visualizations
- Color-coded clusters

## 🔄 Cập nhật Dữ liệu

Để cập nhật dữ liệu:
1. Thay thế file `result.csv`
2. Refresh browser (Ctrl+R hoặc Cmd+R)
3. Click "Rerun" trong Streamlit

Hoặc click nút ⚙️ > "Clear cache" trong Streamlit menu.

## 📱 Mobile Support

Dashboard responsive, có thể xem trên mobile/tablet.

## 🎓 Tips

1. **Explore tabs**: Mỗi page có nhiều tabs với nội dung chi tiết
2. **Use sidebar**: Điều hướng nhanh giữa các pages
3. **Hover charts**: Di chuột để xem thông tin chi tiết
4. **Download charts**: Click camera icon để download
5. **Fullscreen**: Click expand icon để xem fullscreen

## 📞 Support

Nếu gặp vấn đề, kiểm tra:
1. Python version (python --version)
2. Streamlit version (streamlit --version)
3. Dependencies (pip list)
4. File paths
5. Console errors

## 🌟 Features

- ✅ Real-time interaction
- ✅ Beautiful UI với gradient colors
- ✅ Comprehensive analysis
- ✅ Performance optimized
- ✅ Mobile responsive
- ✅ Export charts
- ✅ Detailed documentation

---

**Happy Analyzing! 📊🎉**

