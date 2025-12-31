# 🔧 HƯỚNG DẪN SỬA LỖI VÀ CHẠY DASHBOARD

## ❌ Lỗi gặp phải:

1. **File does not exist: analysis_dashboard.py**
   - Nguyên nhân: Đang chạy ở sai thư mục
   
2. **ModuleNotFoundError: No module named 'sklearn'**
   - Nguyên nhân: Chưa cài đặt scikit-learn

---

## ✅ GIẢI PHÁP 3 CÁCH

### 🚀 CÁCH 1: Tự động (Khuyến nghị) ⭐

Chạy script tự động cài đặt và khởi động:

```bash
cd /Users/nguyenkimhau/Desktop/APTECH/DoAnCuoiKy/App
./INSTALL_AND_RUN.sh
```

**Script này sẽ:**
- ✅ Kiểm tra Python & pip
- ✅ Tự động cài đặt tất cả dependencies
- ✅ Kiểm tra files cần thiết
- ✅ Khởi động dashboard

---

### 📝 CÁCH 2: Từng bước (Chi tiết)

#### Bước 1: Di chuyển vào thư mục App

```bash
cd /Users/nguyenkimhau/Desktop/APTECH/DoAnCuoiKy/App
```

Kiểm tra bạn đã ở đúng thư mục:

```bash
pwd
# Kết quả phải là: /Users/nguyenkimhau/Desktop/APTECH/DoAnCuoiKy/App
```

Kiểm tra file tồn tại:

```bash
ls -lh analysis_dashboard.py result.csv
# Phải thấy cả 2 files
```

#### Bước 2: Cài đặt scikit-learn

**Option A: Cài từng package:**

```bash
pip install scikit-learn
```

**Option B: Cài tất cả dependencies:**

```bash
pip install -r requirements.txt
```

Nếu gặp lỗi permission, thêm `--user`:

```bash
pip install --user -r requirements.txt
```

#### Bước 3: Kiểm tra installation

```bash
python3 -c "import sklearn; print('scikit-learn:', sklearn.__version__)"
python3 -c "import streamlit; print('streamlit:', streamlit.__version__)"
python3 -c "import plotly; print('plotly:', plotly.__version__)"
```

Phải thấy version numbers, không có lỗi.

#### Bước 4: Chạy dashboard

```bash
streamlit run analysis_dashboard.py
```

Dashboard sẽ tự động mở tại: **http://localhost:8501**

---

### 🐍 CÁCH 3: Sử dụng Virtual Environment (An toàn nhất)

#### Tạo virtual environment:

```bash
cd /Users/nguyenkimhau/Desktop/APTECH/DoAnCuoiKy
python3 -m venv venv
```

#### Kích hoạt venv:

```bash
source venv/bin/activate
```

Bạn sẽ thấy `(venv)` trước dòng lệnh.

#### Cài đặt dependencies:

```bash
cd App
pip install -r requirements.txt
```

#### Chạy dashboard:

```bash
streamlit run analysis_dashboard.py
```

#### Thoát venv (khi xong):

```bash
deactivate
```

---

## 🐛 TROUBLESHOOTING

### Lỗi 1: Command not found: pip

**Giải pháp:**

```bash
# Thử pip3
pip3 install -r requirements.txt

# Hoặc dùng python -m pip
python3 -m pip install -r requirements.txt
```

### Lỗi 2: Permission denied

**Giải pháp:**

```bash
pip install --user -r requirements.txt
```

### Lỗi 3: pip install quá chậm

**Giải pháp:** Sử dụng mirror gần hơn

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Lỗi 4: Port 8501 already in use

**Giải pháp:**

```bash
streamlit run analysis_dashboard.py --server.port 8502
```

Hoặc kill process đang dùng port 8501:

```bash
lsof -ti:8501 | xargs kill -9
streamlit run analysis_dashboard.py
```

### Lỗi 5: ModuleNotFoundError: No module named 'XXX'

**Giải pháp:** Cài từng module bị thiếu

```bash
pip install <module_name>
```

Ví dụ:
```bash
pip install scikit-learn  # cho sklearn
pip install plotly        # cho plotly
pip install seaborn       # cho seaborn
```

### Lỗi 6: File not found: result.csv

**Giải pháp:**

1. Kiểm tra file tồn tại:
```bash
ls -lh result.csv
```

2. Nếu không có, kiểm tra thư mục khác:
```bash
find .. -name "result.csv"
```

3. Copy file vào đúng thư mục nếu cần

### Lỗi 7: Python version không đúng

**Giải pháp:**

```bash
# Kiểm tra version
python3 --version
# Cần Python 3.8 trở lên

# Nếu quá cũ, cài Python mới từ python.org
```

---

## 📦 DEPENDENCIES CẦN CÀI

```
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0
scikit-learn>=1.3.0    ← QUAN TRỌNG (import tên là 'sklearn')
plotly>=5.17.0
```

**Lưu ý:** Package tên là `scikit-learn` nhưng import là `sklearn`

---

## ✅ CHECKLIST TRƯỚC KHI CHẠY

- [ ] Đã cd vào thư mục `/App`
- [ ] File `analysis_dashboard.py` tồn tại
- [ ] File `result.csv` tồn tại
- [ ] Python 3.8+ đã cài
- [ ] pip hoạt động
- [ ] Đã cài scikit-learn: `pip list | grep scikit-learn`
- [ ] Đã cài streamlit: `pip list | grep streamlit`
- [ ] Đã cài plotly: `pip list | grep plotly`
- [ ] Port 8501 chưa được dùng

---

## 🚀 QUICK START (Copy-Paste)

Chỉ cần copy paste block này:

```bash
# Di chuyển vào thư mục
cd /Users/nguyenkimhau/Desktop/APTECH/DoAnCuoiKy/App

# Cài đặt dependencies
pip install streamlit pandas numpy matplotlib seaborn scikit-learn plotly

# Chạy dashboard
streamlit run analysis_dashboard.py
```

Hoặc chạy script tự động:

```bash
cd /Users/nguyenkimhau/Desktop/APTECH/DoAnCuoiKy/App
./INSTALL_AND_RUN.sh
```

---

## 🆘 VẪN GẶP LỖI?

### Kiểm tra hệ thống:

```bash
# 1. Kiểm tra Python
python3 --version

# 2. Kiểm tra pip
pip --version

# 3. Kiểm tra thư mục hiện tại
pwd

# 4. Kiểm tra files
ls -lh

# 5. Kiểm tra packages đã cài
pip list

# 6. Test import
python3 -c "import sklearn, streamlit, plotly; print('OK')"
```

### Debug mode:

Chạy với verbose để xem lỗi chi tiết:

```bash
streamlit run analysis_dashboard.py --logger.level=debug
```

---

## 📞 LÊN HỆ HỖ TRỢ

Nếu vẫn lỗi, cung cấp thông tin sau:

1. Output của `python3 --version`
2. Output của `pip list`
3. Output của `pwd`
4. Screenshot lỗi đầy đủ
5. Output của `ls -lh`

---

## 🎯 KẾT QUẢ MONG ĐỢI

Khi chạy thành công, bạn sẽ thấy:

```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

Browser sẽ tự động mở và hiển thị dashboard.

---

## 🎉 THÀNH CÔNG!

Nếu thấy dashboard, chúc mừng! Bạn có thể:

- ✅ Navigate qua 7 pages
- ✅ Thử các interactive charts
- ✅ Adjust sliders và parameters
- ✅ Explore dữ liệu

**Enjoy your dashboard! 📊✨**

---

*Cập nhật: 31/12/2025*  
*Tác giả: Nguyễn Kim Hậu*

