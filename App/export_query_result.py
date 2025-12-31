"""
SCRIPT EXPORT KẾT QUẢ QUERY
Thực hiện query SQL và export ra file CSV
"""

import pandas as pd
import os
from datetime import datetime

# Thiết lập hiển thị
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)

# ============================================================================
# THIẾT LẬP ĐƯỜNG DẪN
# ============================================================================

# Đường dẫn thư mục cleaned_data
CLEANED_DATA_DIR = "cleaned_data/"

# Đường dẫn file output
OUTPUT_FILE = "result.csv"

# ============================================================================
# ĐỌC DỮ LIỆU
# ============================================================================

print("=" * 80)
print("BẮT ĐẦU XỬ LÝ QUERY")
print("=" * 80)
print(f"Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Đọc file patients_cleaned.csv
print("📖 Đang đọc file patients_cleaned.csv...")
try:
    patients = pd.read_csv(
        os.path.join(CLEANED_DATA_DIR, 'patients_cleaned.csv'),
        encoding='utf-8-sig'
    )
    print(f"✓ Đã đọc patients_cleaned.csv: {len(patients):,} dòng, {len(patients.columns)} cột")
except Exception as e:
    print(f"✗ Lỗi khi đọc patients_cleaned.csv: {e}")
    exit(1)

# Đọc file medical_records_cleaned.csv
print("\n📖 Đang đọc file medical_records_cleaned.csv...")
try:
    medical_records = pd.read_csv(
        os.path.join(CLEANED_DATA_DIR, 'medical_records_cleaned.csv'),
        encoding='utf-8-sig'
    )
    print(f"✓ Đã đọc medical_records_cleaned.csv: {len(medical_records):,} dòng, {len(medical_records.columns)} cột")
except Exception as e:
    print(f"✗ Lỗi khi đọc medical_records_cleaned.csv: {e}")
    exit(1)

# ============================================================================
# THỰC HIỆN QUERY (JOIN)
# ============================================================================

print("\n" + "=" * 80)
print("THỰC HIỆN QUERY - JOIN DỮ LIỆU")
print("=" * 80)

# Đổi tên cột trang_thai trong medical_records để tránh trùng
if 'trang_thai' in medical_records.columns:
    medical_records = medical_records.rename(columns={'trang_thai': 'trang_thai_mr'})

# Thực hiện INNER JOIN
print("\n🔄 Đang thực hiện INNER JOIN...")
df_result = patients.merge(
    medical_records,
    on='patient_id',
    how='inner'
)
print(f"✓ Đã join: {len(df_result):,} bản ghi")

# ============================================================================
# CHỌN CÁC CỘT THEO YÊU CẦU
# ============================================================================

print("\n" + "=" * 80)
print("CHỌN CÁC CỘT THEO QUERY")
print("=" * 80)

# Danh sách các cột cần lấy (theo thứ tự trong query)
columns_needed = [
    'patient_id',      # AS id
    'gioi_tinh',
    'tuoi',
    'ngay_sinh',
    'nhom_tuoi',
    'nhom_mau',
    'thanh_pho',
    'tien_su_benh',
    'trang_thai',      # từ patients
    'trieu_chung',
    'xet_nghiem',
    'ket_qua_xet_nghiem',  # AS ket_qua
    'loai_kham',
    'chan_doan'        # AS chuan_doan
]

# Kiểm tra các cột có tồn tại không
missing_columns = [col for col in columns_needed if col not in df_result.columns]
if missing_columns:
    print(f"⚠ Cảnh báo: Các cột sau không tồn tại: {missing_columns}")
    # Kiểm tra các cột tương tự
    for col in missing_columns:
        similar_cols = [c for c in df_result.columns if col.lower() in c.lower() or c.lower() in col.lower()]
        if similar_cols:
            print(f"   - Có thể dùng: {similar_cols}")
    # Chỉ lấy các cột có sẵn
    columns_needed = [col for col in columns_needed if col in df_result.columns]

# Sắp xếp trước khi chọn cột (nếu có ngay_kham)
if 'ngay_kham' in df_result.columns:
    df_result = df_result.sort_values(['patient_id', 'ngay_kham'])
else:
    df_result = df_result.sort_values('patient_id')

# Chọn các cột
df_final = df_result[columns_needed].copy()

# Đổi tên cột theo yêu cầu
df_final = df_final.rename(columns={
    'patient_id': 'id',
    'ket_qua_xet_nghiem': 'ket_qua',
    'chan_doan': 'chuan_doan'
})

print(f"✓ Đã chọn {len(df_final.columns)} cột")
print(f"✓ Số bản ghi: {len(df_final):,}")

# ============================================================================
# HIỂN THỊ THÔNG TIN KẾT QUẢ
# ============================================================================

print("\n" + "=" * 80)
print("THÔNG TIN KẾT QUẢ")
print("=" * 80)

print(f"\n📊 Số bản ghi: {len(df_final):,}")
print(f"📊 Số cột: {len(df_final.columns)}")
print(f"\n📋 Danh sách cột:")
for i, col in enumerate(df_final.columns, 1):
    print(f"   {i:2d}. {col}")

print(f"\n📋 5 dòng đầu tiên:")
print(df_final.head().to_string())

print(f"\n📋 Thống kê cơ bản:")
print(f"   - Số bệnh nhân duy nhất: {df_final['id'].nunique():,}")
print(f"   - Số giá trị NULL:")
for col in df_final.columns:
    null_count = df_final[col].isnull().sum()
    if null_count > 0:
        print(f"     + {col}: {null_count:,} ({null_count/len(df_final)*100:.2f}%)")

# ============================================================================
# EXPORT RA FILE CSV
# ============================================================================

print("\n" + "=" * 80)
print("EXPORT RA FILE CSV")
print("=" * 80)

try:
    # Export ra file CSV với encoding UTF-8-BOM (để Excel đọc được tiếng Việt)
    df_final.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding='utf-8-sig'
    )
    
    # Kiểm tra kích thước file
    file_size = os.path.getsize(OUTPUT_FILE)
    file_size_mb = file_size / (1024 * 1024)
    
    print(f"\n✓ Đã export thành công!")
    print(f"   📁 File: {OUTPUT_FILE}")
    print(f"   📊 Số dòng: {len(df_final):,}")
    print(f"   📊 Số cột: {len(df_final.columns)}")
    print(f"   💾 Kích thước: {file_size_mb:.2f} MB")
    
except Exception as e:
    print(f"\n✗ Lỗi khi export file: {e}")
    exit(1)

# ============================================================================
# HOÀN TẤT
# ============================================================================

print("\n" + "=" * 80)
print("HOÀN TẤT!")
print("=" * 80)
print(f"Thời gian hoàn thành: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"\n✅ File kết quả: {OUTPUT_FILE}")
print("=" * 80)

