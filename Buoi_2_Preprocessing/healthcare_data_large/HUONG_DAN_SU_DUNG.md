# HƯỚNG DẪN SỬ DỤNG SCRIPT PREPROCESSING

## 📋 YÊU CẦU

- Python 3.7 trở lên
- Các thư viện: `pandas`, `numpy`

Cài đặt thư viện:
```bash
pip install pandas numpy
```

## 🚀 CÁCH SỬ DỤNG

### Cách 1: Chạy toàn bộ script tự động

```bash
cd healthcare_data_large
python preprocessing_healthcare_data.py
```

Script sẽ tự động thực hiện tất cả 11 bước preprocessing và lưu kết quả vào thư mục `healthcare_data_large_cleaned/`.

### Cách 2: Chạy từng bước riêng lẻ

Mở file `preprocessing_healthcare_data.py` trong Python và chạy từng hàm theo thứ tự:

```python
# 1. Đọc dữ liệu
data = load_data()

# 2. Kiểm tra dữ liệu thiếu
missing_report = check_missing_values(data)
data = handle_all_missing_values(data)

# 3. Kiểm tra trùng lặp
duplicate_report = check_duplicates(data)
data = remove_duplicates(data)

# ... và tiếp tục các bước khác
```

## 📁 KẾT QUẢ

Sau khi chạy xong, bạn sẽ có:

1. **Thư mục `healthcare_data_large_cleaned/`** chứa các file CSV đã được làm sạch:
   - `patients_cleaned.csv`
   - `doctors_cleaned.csv`
   - `medical_records_cleaned.csv`
   - `medications_cleaned.csv`
   - `diagnoses_cleaned.csv`

2. **File `data_quality_report.json`** chứa báo cáo tổng hợp về chất lượng dữ liệu

## 📖 CHI TIẾT CÁC BƯỚC

Xem file `KE_HOACH_PREPROCESSING.md` để biết chi tiết từng bước preprocessing.

## ⚠️ LƯU Ý

- Script sẽ **KHÔNG** thay đổi dữ liệu gốc
- Dữ liệu đã làm sạch được lưu vào thư mục riêng
- Luôn kiểm tra kết quả sau khi chạy script
- Nếu có lỗi, kiểm tra đường dẫn thư mục và encoding file

## 🔧 TÙY CHỈNH

Bạn có thể tùy chỉnh script bằng cách:

1. Thay đổi đường dẫn thư mục trong biến `DATA_DIR`
2. Thay đổi thư mục output trong hàm `save_cleaned_data()`
3. Điều chỉnh các ngưỡng phát hiện outliers
4. Thêm các bước xử lý tùy chỉnh khác

