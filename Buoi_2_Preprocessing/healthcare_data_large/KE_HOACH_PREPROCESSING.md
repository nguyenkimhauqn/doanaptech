# KẾ HOẠCH PREPROCESSING DỮ LIỆU Y TẾ

## 📋 TỔNG QUAN

Tài liệu này hướng dẫn từng bước thực hiện preprocessing cho 5 file CSV trong thư mục `healthcare_data_large`:
1. `patients.csv` (80,000 dòng, 15 cột)
2. `doctors.csv` (80,000 dòng, 12 cột)
3. `medical_records.csv` (400,000 dòng, 22 cột) - Bảng chính
4. `medications.csv` (80,000 dòng, 10 cột)
5. `diagnoses.csv` (80,000 dòng, 10 cột)

---

## 🎯 MỤC TIÊU PREPROCESSING

1. **Kiểm tra và xử lý dữ liệu thiếu (Missing Values)**
2. **Kiểm tra và xử lý dữ liệu trùng lặp (Duplicates)**
3. **Kiểm tra tính nhất quán dữ liệu (Data Consistency)**
4. **Kiểm tra tính toàn vẹn tham chiếu (Referential Integrity)**
5. **Chuẩn hóa định dạng dữ liệu (Data Formatting)**
6. **Xử lý dữ liệu ngoại lai (Outliers)**
7. **Tạo báo cáo tổng hợp về chất lượng dữ liệu**

---

## 📝 CÁC BƯỚC THỰC HIỆN

### **BƯỚC 1: THIẾT LẬP MÔI TRƯỜNG VÀ IMPORT THƯ VIỆN**

#### 1.1. Tạo file Python mới
```python
# preprocessing_healthcare_data.py
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Thiết lập hiển thị
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)
pd.set_option('display.width', None)
```

#### 1.2. Định nghĩa đường dẫn và biến
```python
# Đường dẫn thư mục
DATA_DIR = "healthcare_data_large/"

# Danh sách các file cần xử lý
FILES = {
    'patients': 'patients.csv',
    'doctors': 'doctors.csv',
    'medical_records': 'medical_records.csv',
    'medications': 'medications.csv',
    'diagnoses': 'diagnoses.csv'
}
```

---

### **BƯỚC 2: ĐỌC DỮ LIỆU VÀ KIỂM TRA CƠ BẢN**

#### 2.1. Đọc tất cả các file CSV
```python
def load_data():
    """Đọc tất cả các file CSV"""
    data = {}
    for name, filename in FILES.items():
        filepath = DATA_DIR + filename
        try:
            # Đọc với encoding UTF-8-BOM
            data[name] = pd.read_csv(filepath, encoding='utf-8-sig')
            print(f"✓ Đã đọc {filename}: {len(data[name])} dòng, {len(data[name].columns)} cột")
        except Exception as e:
            print(f"✗ Lỗi khi đọc {filename}: {e}")
    return data

# Thực hiện đọc dữ liệu
data = load_data()
```

#### 2.2. Kiểm tra thông tin cơ bản của từng bảng
```python
def basic_info(data):
    """Hiển thị thông tin cơ bản của từng bảng"""
    for name, df in data.items():
        print(f"\n{'='*60}")
        print(f"BẢNG: {name.upper()}")
        print(f"{'='*60}")
        print(f"Kích thước: {df.shape[0]} dòng x {df.shape[1]} cột")
        print(f"\nKiểu dữ liệu:")
        print(df.dtypes)
        print(f"\n5 dòng đầu tiên:")
        print(df.head())
        print(f"\nThống kê mô tả:")
        print(df.describe(include='all'))
        
basic_info(data)
```

---

### **BƯỚC 3: KIỂM TRA DỮ LIỆU THIẾU (MISSING VALUES)**

#### 3.1. Đếm số lượng giá trị thiếu
```python
def check_missing_values(data):
    """Kiểm tra và báo cáo giá trị thiếu"""
    print("\n" + "="*80)
    print("KIỂM TRA DỮ LIỆU THIẾU")
    print("="*80)
    
    missing_report = {}
    
    for name, df in data.items():
        missing_count = df.isnull().sum()
        missing_percent = (missing_count / len(df)) * 100
        
        missing_df = pd.DataFrame({
            'Cột': missing_count.index,
            'Số lượng thiếu': missing_count.values,
            'Tỷ lệ (%)': missing_percent.values
        })
        missing_df = missing_df[missing_df['Số lượng thiếu'] > 0].sort_values('Số lượng thiếu', ascending=False)
        
        if len(missing_df) > 0:
            print(f"\n{name.upper()}:")
            print(missing_df.to_string(index=False))
            missing_report[name] = missing_df
        else:
            print(f"\n{name.upper()}: Không có dữ liệu thiếu ✓")
            missing_report[name] = None
    
    return missing_report

missing_report = check_missing_values(data)
```

#### 3.2. Xử lý dữ liệu thiếu theo từng bảng

**3.2.1. Bảng PATIENTS**
```python
def handle_missing_patients(df):
    """Xử lý dữ liệu thiếu trong bảng patients"""
    df_clean = df.copy()
    
    # Email: Thay thế bằng giá trị mặc định hoặc tạo từ patient_id
    if df_clean['email'].isnull().any():
        mask = df_clean['email'].isnull()
        df_clean.loc[mask, 'email'] = df_clean.loc[mask, 'patient_id'].str.lower() + '@email.com'
    
    # Tiền sử bệnh: Thay thế 'Không' nếu thiếu
    if df_clean['tien_su_benh'].isnull().any():
        df_clean['tien_su_benh'].fillna('Không', inplace=True)
    
    # Dị ứng: Thay thế 'Không' nếu thiếu
    if df_clean['di_ung'].isnull().any():
        df_clean['di_ung'].fillna('Không', inplace=True)
    
    return df_clean
```

**3.2.2. Bảng MEDICAL_RECORDS**
```python
def handle_missing_medical_records(df):
    """Xử lý dữ liệu thiếu trong bảng medical_records"""
    df_clean = df.copy()
    
    # Ghi chú: Thay thế bằng chuỗi rỗng nếu thiếu
    if df_clean['ghi_chu'].isnull().any():
        df_clean['ghi_chu'].fillna('', inplace=True)
    
    # Kết quả xét nghiệm: Thay thế 'Chưa có kết quả' nếu thiếu
    if df_clean['ket_qua_xet_nghiem'].isnull().any():
        df_clean['ket_qua_xet_nghiem'].fillna('Chưa có kết quả', inplace=True)
    
    return df_clean
```

**3.2.3. Bảng DIAGNOSES**
```python
def handle_missing_diagnoses(df):
    """Xử lý dữ liệu thiếu trong bảng diagnoses"""
    df_clean = df.copy()
    
    # Ghi chú: Thay thế bằng chuỗi rỗng nếu thiếu
    if df_clean['ghi_chu'].isnull().any():
        df_clean['ghi_chu'].fillna('', inplace=True)
    
    return df_clean
```

---

### **BƯỚC 4: KIỂM TRA DỮ LIỆU TRÙNG LẶP (DUPLICATES)**

#### 4.1. Kiểm tra dòng trùng lặp
```python
def check_duplicates(data):
    """Kiểm tra và báo cáo dữ liệu trùng lặp"""
    print("\n" + "="*80)
    print("KIỂM TRA DỮ LIỆU TRÙNG LẶP")
    print("="*80)
    
    duplicate_report = {}
    
    for name, df in data.items():
        # Tìm khóa chính của từng bảng
        if name == 'patients':
            key_col = 'patient_id'
        elif name == 'doctors':
            key_col = 'doctor_id'
        elif name == 'medical_records':
            key_col = 'record_id'
        elif name == 'medications':
            key_col = 'medication_id'
        elif name == 'diagnoses':
            key_col = 'diagnosis_id'
        else:
            key_col = None
        
        # Kiểm tra trùng lặp theo khóa chính
        if key_col:
            duplicate_keys = df[df.duplicated(subset=[key_col], keep=False)]
            if len(duplicate_keys) > 0:
                print(f"\n{name.upper()}: Có {len(duplicate_keys)} dòng trùng lặp theo {key_col}")
                duplicate_report[name] = duplicate_keys
            else:
                print(f"\n{name.upper()}: Không có trùng lặp theo {key_col} ✓")
        
        # Kiểm tra dòng hoàn toàn trùng lặp
        full_duplicates = df[df.duplicated(keep=False)]
        if len(full_duplicates) > 0:
            print(f"{name.upper()}: Có {len(full_duplicates)} dòng hoàn toàn trùng lặp")
        else:
            print(f"{name.upper()}: Không có dòng hoàn toàn trùng lặp ✓")
    
    return duplicate_report

duplicate_report = check_duplicates(data)
```

#### 4.2. Xóa dữ liệu trùng lặp
```python
def remove_duplicates(data):
    """Xóa dữ liệu trùng lặp"""
    data_clean = {}
    
    for name, df in data.items():
        df_clean = df.copy()
        
        # Xác định khóa chính
        if name == 'patients':
            key_col = 'patient_id'
        elif name == 'doctors':
            key_col = 'doctor_id'
        elif name == 'medical_records':
            key_col = 'record_id'
        elif name == 'medications':
            key_col = 'medication_id'
        elif name == 'diagnoses':
            key_col = 'diagnosis_id'
        else:
            key_col = None
        
        # Xóa trùng lặp theo khóa chính (giữ dòng đầu tiên)
        if key_col:
            before = len(df_clean)
            df_clean = df_clean.drop_duplicates(subset=[key_col], keep='first')
            after = len(df_clean)
            if before != after:
                print(f"{name}: Đã xóa {before - after} dòng trùng lặp")
        
        # Xóa dòng hoàn toàn trùng lặp
        before = len(df_clean)
        df_clean = df_clean.drop_duplicates(keep='first')
        
        data_clean[name] = df_clean
    
    return data_clean

data = remove_duplicates(data)
```

---

### **BƯỚC 5: KIỂM TRA TÍNH TOÀN VẸN THAM CHIẾU (REFERENTIAL INTEGRITY)**

#### 5.1. Kiểm tra foreign keys trong MEDICAL_RECORDS
```python
def check_referential_integrity(data):
    """Kiểm tra tính toàn vẹn tham chiếu giữa các bảng"""
    print("\n" + "="*80)
    print("KIỂM TRA TÍNH TOÀN VẸN THAM CHIẾU")
    print("="*80)
    
    integrity_issues = {}
    
    # Kiểm tra patient_id trong medical_records
    mr = data['medical_records']
    patients = data['patients']
    
    invalid_patient_ids = mr[~mr['patient_id'].isin(patients['patient_id'])]
    if len(invalid_patient_ids) > 0:
        print(f"\n✗ MEDICAL_RECORDS: {len(invalid_patient_ids)} dòng có patient_id không tồn tại trong PATIENTS")
        integrity_issues['invalid_patient_ids'] = invalid_patient_ids
    else:
        print(f"\n✓ MEDICAL_RECORDS: Tất cả patient_id đều hợp lệ")
    
    # Kiểm tra doctor_id trong medical_records
    doctors = data['doctors']
    invalid_doctor_ids = mr[~mr['doctor_id'].isin(doctors['doctor_id'])]
    if len(invalid_doctor_ids) > 0:
        print(f"✗ MEDICAL_RECORDS: {len(invalid_doctor_ids)} dòng có doctor_id không tồn tại trong DOCTORS")
        integrity_issues['invalid_doctor_ids'] = invalid_doctor_ids
    else:
        print(f"✓ MEDICAL_RECORDS: Tất cả doctor_id đều hợp lệ")
    
    # Kiểm tra diagnosis_id trong medical_records
    diagnoses = data['diagnoses']
    invalid_diagnosis_ids = mr[~mr['diagnosis_id'].isin(diagnoses['diagnosis_id'])]
    if len(invalid_diagnosis_ids) > 0:
        print(f"✗ MEDICAL_RECORDS: {len(invalid_diagnosis_ids)} dòng có diagnosis_id không tồn tại trong DIAGNOSES")
        integrity_issues['invalid_diagnosis_ids'] = invalid_diagnosis_ids
    else:
        print(f"✓ MEDICAL_RECORDS: Tất cả diagnosis_id đều hợp lệ")
    
    # Kiểm tra medication_id trong medical_records
    medications = data['medications']
    invalid_medication_ids = mr[~mr['medication_id'].isin(medications['medication_id'])]
    if len(invalid_medication_ids) > 0:
        print(f"✗ MEDICAL_RECORDS: {len(invalid_medication_ids)} dòng có medication_id không tồn tại trong MEDICATIONS")
        integrity_issues['invalid_medication_ids'] = invalid_medication_ids
    else:
        print(f"✓ MEDICAL_RECORDS: Tất cả medication_id đều hợp lệ")
    
    return integrity_issues

integrity_issues = check_referential_integrity(data)
```

#### 5.2. Xử lý các vấn đề về tính toàn vẹn tham chiếu
```python
def fix_referential_integrity(data, integrity_issues):
    """Xử lý các vấn đề về tính toàn vẹn tham chiếu"""
    data_clean = data.copy()
    mr = data_clean['medical_records'].copy()
    
    # Xóa các dòng có foreign key không hợp lệ
    if 'invalid_patient_ids' in integrity_issues:
        invalid_indices = integrity_issues['invalid_patient_ids'].index
        mr = mr.drop(invalid_indices)
        print(f"Đã xóa {len(invalid_indices)} dòng có patient_id không hợp lệ")
    
    if 'invalid_doctor_ids' in integrity_issues:
        invalid_indices = integrity_issues['invalid_doctor_ids'].index
        mr = mr.drop(invalid_indices)
        print(f"Đã xóa {len(invalid_indices)} dòng có doctor_id không hợp lệ")
    
    if 'invalid_diagnosis_ids' in integrity_issues:
        invalid_indices = integrity_issues['invalid_diagnosis_ids'].index
        mr = mr.drop(invalid_indices)
        print(f"Đã xóa {len(invalid_indices)} dòng có diagnosis_id không hợp lệ")
    
    if 'invalid_medication_ids' in integrity_issues:
        invalid_indices = integrity_issues['invalid_medication_ids'].index
        mr = mr.drop(invalid_indices)
        print(f"Đã xóa {len(invalid_indices)} dòng có medication_id không hợp lệ")
    
    data_clean['medical_records'] = mr
    return data_clean

if integrity_issues:
    data = fix_referential_integrity(data, integrity_issues)
```

---

### **BƯỚC 6: CHUẨN HÓA ĐỊNH DẠNG DỮ LIỆU**

#### 6.1. Chuẩn hóa định dạng ngày tháng
```python
def standardize_dates(data):
    """Chuẩn hóa định dạng ngày tháng"""
    data_clean = data.copy()
    
    # Bảng PATIENTS
    if 'ngay_sinh' in data_clean['patients'].columns:
        data_clean['patients']['ngay_sinh'] = pd.to_datetime(
            data_clean['patients']['ngay_sinh'], 
            errors='coerce',
            format='%Y-%m-%d'
        )
    
    if 'ngay_dang_ky' in data_clean['patients'].columns:
        data_clean['patients']['ngay_dang_ky'] = pd.to_datetime(
            data_clean['patients']['ngay_dang_ky'],
            errors='coerce',
            format='%Y-%m-%d'
        )
    
    # Bảng DOCTORS
    if 'ngay_sinh' in data_clean['doctors'].columns:
        data_clean['doctors']['ngay_sinh'] = pd.to_datetime(
            data_clean['doctors']['ngay_sinh'],
            errors='coerce',
            format='%Y-%m-%d'
        )
    
    # Bảng MEDICAL_RECORDS
    if 'ngay_kham' in data_clean['medical_records'].columns:
        data_clean['medical_records']['ngay_kham'] = pd.to_datetime(
            data_clean['medical_records']['ngay_kham'],
            errors='coerce',
            format='%Y-%m-%d'
        )
    
    # Bảng MEDICATIONS
    if 'han_su_dung' in data_clean['medications'].columns:
        data_clean['medications']['han_su_dung'] = pd.to_datetime(
            data_clean['medications']['han_su_dung'],
            errors='coerce',
            format='%Y-%m-%d'
        )
    
    return data_clean

data = standardize_dates(data)
```

#### 6.2. Chuẩn hóa định dạng số
```python
def standardize_numeric(data):
    """Chuẩn hóa định dạng số"""
    data_clean = data.copy()
    
    # Bảng PATIENTS
    if 'tuoi' in data_clean['patients'].columns:
        data_clean['patients']['tuoi'] = pd.to_numeric(
            data_clean['patients']['tuoi'],
            errors='coerce'
        )
    
    # Bảng DOCTORS
    if 'tuoi' in data_clean['doctors'].columns:
        data_clean['doctors']['tuoi'] = pd.to_numeric(
            data_clean['doctors']['tuoi'],
            errors='coerce'
        )
    
    if 'nam_kinh_nghiem' in data_clean['doctors'].columns:
        data_clean['doctors']['nam_kinh_nghiem'] = pd.to_numeric(
            data_clean['doctors']['nam_kinh_nghiem'],
            errors='coerce'
        )
    
    # Bảng MEDICAL_RECORDS
    numeric_cols = ['chi_phi_kham', 'chi_phi_thuoc', 'tong_chi_phi', 'so_ngay_dung_thuoc']
    for col in numeric_cols:
        if col in data_clean['medical_records'].columns:
            data_clean['medical_records'][col] = pd.to_numeric(
                data_clean['medical_records'][col],
                errors='coerce'
            )
    
    # Bảng MEDICATIONS
    if 'gia_ban' in data_clean['medications'].columns:
        data_clean['medications']['gia_ban'] = pd.to_numeric(
            data_clean['medications']['gia_ban'],
            errors='coerce'
        )
    
    # Bảng DIAGNOSES
    if 'ty_le_hoi_phuc' in data_clean['diagnoses'].columns:
        # Loại bỏ ký tự % và chuyển sang số
        data_clean['diagnoses']['ty_le_hoi_phuc'] = data_clean['diagnoses']['ty_le_hoi_phuc'].str.rstrip('%')
        data_clean['diagnoses']['ty_le_hoi_phuc'] = pd.to_numeric(
            data_clean['diagnoses']['ty_le_hoi_phuc'],
            errors='coerce'
        )
    
    return data_clean

data = standardize_numeric(data)
```

#### 6.3. Chuẩn hóa định dạng chuỗi (loại bỏ khoảng trắng thừa)
```python
def standardize_strings(data):
    """Chuẩn hóa định dạng chuỗi"""
    data_clean = data.copy()
    
    for name, df in data_clean.items():
        # Áp dụng cho tất cả các cột kiểu object (string)
        string_cols = df.select_dtypes(include=['object']).columns
        for col in string_cols:
            if df[col].dtype == 'object':
                data_clean[name][col] = df[col].astype(str).str.strip()
                # Thay thế nhiều khoảng trắng bằng một khoảng trắng
                data_clean[name][col] = data_clean[name][col].str.replace(r'\s+', ' ', regex=True)
    
    return data_clean

data = standardize_strings(data)
```

---

### **BƯỚC 7: KIỂM TRA TÍNH NHẤT QUÁN DỮ LIỆU**

#### 7.1. Kiểm tra tính nhất quán giữa các cột liên quan
```python
def check_data_consistency(data):
    """Kiểm tra tính nhất quán dữ liệu"""
    print("\n" + "="*80)
    print("KIỂM TRA TÍNH NHẤT QUÁN DỮ LIỆU")
    print("="*80)
    
    issues = []
    
    # Kiểm tra tuổi và ngày sinh trong PATIENTS
    patients = data['patients']
    if 'ngay_sinh' in patients.columns and 'tuoi' in patients.columns:
        current_year = datetime.now().year
        calculated_age = current_year - patients['ngay_sinh'].dt.year
        age_diff = abs(calculated_age - patients['tuoi'])
        inconsistent_age = patients[age_diff > 1]  # Cho phép sai lệch 1 năm
        
        if len(inconsistent_age) > 0:
            print(f"\n✗ PATIENTS: {len(inconsistent_age)} dòng có tuổi không khớp với ngày sinh")
            issues.append(('patients_age', inconsistent_age))
        else:
            print(f"\n✓ PATIENTS: Tuổi và ngày sinh nhất quán")
    
    # Kiểm tra tuổi và ngày sinh trong DOCTORS
    doctors = data['doctors']
    if 'ngay_sinh' in doctors.columns and 'tuoi' in doctors.columns:
        calculated_age = current_year - doctors['ngay_sinh'].dt.year
        age_diff = abs(calculated_age - doctors['tuoi'])
        inconsistent_age = doctors[age_diff > 1]
        
        if len(inconsistent_age) > 0:
            print(f"✗ DOCTORS: {len(inconsistent_age)} dòng có tuổi không khớp với ngày sinh")
            issues.append(('doctors_age', inconsistent_age))
        else:
            print(f"✓ DOCTORS: Tuổi và ngày sinh nhất quán")
    
    # Kiểm tra tổng chi phí trong MEDICAL_RECORDS
    mr = data['medical_records']
    if all(col in mr.columns for col in ['chi_phi_kham', 'chi_phi_thuoc', 'tong_chi_phi']):
        calculated_total = mr['chi_phi_kham'] + mr['chi_phi_thuoc']
        total_diff = abs(calculated_total - mr['tong_chi_phi'])
        inconsistent_total = mr[total_diff > 1000]  # Cho phép sai lệch 1000 VNĐ
        
        if len(inconsistent_total) > 0:
            print(f"✗ MEDICAL_RECORDS: {len(inconsistent_total)} dòng có tổng chi phí không khớp")
            issues.append(('medical_records_total', inconsistent_total))
        else:
            print(f"✓ MEDICAL_RECORDS: Tổng chi phí nhất quán")
    
    # Kiểm tra chuyên khoa giữa các bảng
    # Kiểm tra chuyên khoa trong MEDICAL_RECORDS có khớp với DOCTORS không
    if 'chuyen_khoa' in mr.columns and 'chuyen_khoa' in doctors.columns:
        mr_doctors = mr.merge(doctors[['doctor_id', 'chuyen_khoa']], 
                             on='doctor_id', 
                             suffixes=('_mr', '_doctor'))
        inconsistent_dept = mr_doctors[mr_doctors['chuyen_khoa_mr'] != mr_doctors['chuyen_khoa_doctor']]
        
        if len(inconsistent_dept) > 0:
            print(f"✗ MEDICAL_RECORDS: {len(inconsistent_dept)} dòng có chuyên khoa không khớp với bác sĩ")
            issues.append(('medical_records_department', inconsistent_dept))
        else:
            print(f"✓ MEDICAL_RECORDS: Chuyên khoa nhất quán với bác sĩ")
    
    return issues

consistency_issues = check_data_consistency(data)
```

#### 7.2. Sửa các vấn đề về tính nhất quán
```python
def fix_consistency(data, consistency_issues):
    """Sửa các vấn đề về tính nhất quán"""
    data_clean = data.copy()
    
    # Sửa tuổi trong PATIENTS
    if 'patients_age' in [issue[0] for issue in consistency_issues]:
        patients = data_clean['patients']
        if 'ngay_sinh' in patients.columns and 'tuoi' in patients.columns:
            current_year = datetime.now().year
            calculated_age = current_year - patients['ngay_sinh'].dt.year
            data_clean['patients']['tuoi'] = calculated_age
            print("Đã cập nhật tuổi trong PATIENTS dựa trên ngày sinh")
    
    # Sửa tuổi trong DOCTORS
    if 'doctors_age' in [issue[0] for issue in consistency_issues]:
        doctors = data_clean['doctors']
        if 'ngay_sinh' in doctors.columns and 'tuoi' in doctors.columns:
            current_year = datetime.now().year
            calculated_age = current_year - doctors['ngay_sinh'].dt.year
            data_clean['doctors']['tuoi'] = calculated_age
            print("Đã cập nhật tuổi trong DOCTORS dựa trên ngày sinh")
    
    # Sửa tổng chi phí trong MEDICAL_RECORDS
    if 'medical_records_total' in [issue[0] for issue in consistency_issues]:
        mr = data_clean['medical_records']
        if all(col in mr.columns for col in ['chi_phi_kham', 'chi_phi_thuoc', 'tong_chi_phi']):
            data_clean['medical_records']['tong_chi_phi'] = (
                mr['chi_phi_kham'] + mr['chi_phi_thuoc']
            )
            print("Đã cập nhật tổng chi phí trong MEDICAL_RECORDS")
    
    return data_clean

if consistency_issues:
    data = fix_consistency(data, consistency_issues)
```

---

### **BƯỚC 8: XỬ LÝ DỮ LIỆU NGOẠI LAI (OUTLIERS)**

#### 8.1. Phát hiện outliers trong các cột số
```python
def detect_outliers(data):
    """Phát hiện dữ liệu ngoại lai"""
    print("\n" + "="*80)
    print("PHÁT HIỆN DỮ LIỆU NGOẠI LAI")
    print("="*80)
    
    outliers_report = {}
    
    # Kiểm tra tuổi trong PATIENTS
    patients = data['patients']
    if 'tuoi' in patients.columns:
        Q1 = patients['tuoi'].quantile(0.25)
        Q3 = patients['tuoi'].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = patients[(patients['tuoi'] < lower_bound) | (patients['tuoi'] > upper_bound)]
        if len(outliers) > 0:
            print(f"\nPATIENTS - Tuổi: {len(outliers)} giá trị ngoại lai")
            print(f"  Phạm vi bình thường: {lower_bound:.1f} - {upper_bound:.1f}")
            outliers_report['patients_age'] = outliers
        else:
            print(f"\nPATIENTS - Tuổi: Không có giá trị ngoại lai ✓")
    
    # Kiểm tra chi phí trong MEDICAL_RECORDS
    mr = data['medical_records']
    cost_cols = ['chi_phi_kham', 'chi_phi_thuoc', 'tong_chi_phi']
    
    for col in cost_cols:
        if col in mr.columns:
            Q1 = mr[col].quantile(0.25)
            Q3 = mr[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = mr[(mr[col] < lower_bound) | (mr[col] > upper_bound)]
            if len(outliers) > 0:
                print(f"\nMEDICAL_RECORDS - {col}: {len(outliers)} giá trị ngoại lai")
                print(f"  Phạm vi bình thường: {lower_bound:,.0f} - {upper_bound:,.0f} VNĐ")
                outliers_report[f'mr_{col}'] = outliers
            else:
                print(f"\nMEDICAL_RECORDS - {col}: Không có giá trị ngoại lai ✓")
    
    # Kiểm tra giá bán trong MEDICATIONS
    medications = data['medications']
    if 'gia_ban' in medications.columns:
        Q1 = medications['gia_ban'].quantile(0.25)
        Q3 = medications['gia_ban'].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = medications[(medications['gia_ban'] < lower_bound) | (medications['gia_ban'] > upper_bound)]
        if len(outliers) > 0:
            print(f"\nMEDICATIONS - Giá bán: {len(outliers)} giá trị ngoại lai")
            print(f"  Phạm vi bình thường: {lower_bound:,.0f} - {upper_bound:,.0f} VNĐ")
            outliers_report['medications_price'] = outliers
        else:
            print(f"\nMEDICATIONS - Giá bán: Không có giá trị ngoại lai ✓")
    
    return outliers_report

outliers_report = detect_outliers(data)
```

#### 8.2. Xử lý outliers (tùy chọn: capping hoặc loại bỏ)
```python
def handle_outliers(data, outliers_report, method='cap'):
    """
    Xử lý outliers
    method: 'cap' (giới hạn) hoặc 'remove' (xóa)
    """
    data_clean = data.copy()
    
    if method == 'cap':
        # Giới hạn giá trị ngoại lai bằng giá trị min/max hợp lý
        # (Có thể implement nếu cần)
        print("Phương pháp capping chưa được implement")
    elif method == 'remove':
        # Xóa các dòng có outliers (cẩn thận với phương pháp này)
        print("Cảnh báo: Xóa outliers có thể làm mất dữ liệu quan trọng")
        # (Có thể implement nếu cần)
    
    return data_clean

# Ghi chú: Thông thường nên giữ lại outliers trừ khi chắc chắn là lỗi
# data = handle_outliers(data, outliers_report, method='cap')
```

---

### **BƯỚC 9: KIỂM TRA ĐỊNH DẠNG VÀ GIÁ TRỊ HỢP LỆ**

#### 9.1. Kiểm tra định dạng email
```python
def validate_emails(data):
    """Kiểm tra định dạng email"""
    print("\n" + "="*80)
    print("KIỂM TRA ĐỊNH DẠNG EMAIL")
    print("="*80)
    
    import re
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # Kiểm tra email trong PATIENTS
    patients = data['patients']
    if 'email' in patients.columns:
        invalid_emails = patients[~patients['email'].str.match(email_pattern, na=False)]
        if len(invalid_emails) > 0:
            print(f"\nPATIENTS: {len(invalid_emails)} email không hợp lệ")
        else:
            print(f"\nPATIENTS: Tất cả email đều hợp lệ ✓")
    
    # Kiểm tra email trong DOCTORS
    doctors = data['doctors']
    if 'email' in doctors.columns:
        invalid_emails = doctors[~doctors['email'].str.match(email_pattern, na=False)]
        if len(invalid_emails) > 0:
            print(f"DOCTORS: {len(invalid_emails)} email không hợp lệ")
        else:
            print(f"DOCTORS: Tất cả email đều hợp lệ ✓")

validate_emails(data)
```

#### 9.2. Kiểm tra định dạng số điện thoại
```python
def validate_phone_numbers(data):
    """Kiểm tra định dạng số điện thoại Việt Nam"""
    print("\n" + "="*80)
    print("KIỂM TRA ĐỊNH DẠNG SỐ ĐIỆN THOẠI")
    print("="*80)
    
    import re
    # Số điện thoại Việt Nam: 10 số, bắt đầu bằng 0
    phone_pattern = r'^0\d{9}$'
    
    # Kiểm tra trong PATIENTS
    patients = data['patients']
    if 'so_dien_thoai' in patients.columns:
        invalid_phones = patients[~patients['so_dien_thoai'].str.match(phone_pattern, na=False)]
        if len(invalid_phones) > 0:
            print(f"\nPATIENTS: {len(invalid_phones)} số điện thoại không hợp lệ")
        else:
            print(f"\nPATIENTS: Tất cả số điện thoại đều hợp lệ ✓")
    
    # Kiểm tra trong DOCTORS
    doctors = data['doctors']
    if 'so_dien_thoai' in doctors.columns:
        invalid_phones = doctors[~doctors['so_dien_thoai'].str.match(phone_pattern, na=False)]
        if len(invalid_phones) > 0:
            print(f"DOCTORS: {len(invalid_phones)} số điện thoại không hợp lệ")
        else:
            print(f"DOCTORS: Tất cả số điện thoại đều hợp lệ ✓")

validate_phone_numbers(data)
```

#### 9.3. Kiểm tra giá trị trong các cột phân loại
```python
def validate_categorical_values(data):
    """Kiểm tra giá trị trong các cột phân loại"""
    print("\n" + "="*80)
    print("KIỂM TRA GIÁ TRỊ PHÂN LOẠI")
    print("="*80)
    
    # Kiểm tra giới tính
    patients = data['patients']
    if 'gioi_tinh' in patients.columns:
        valid_genders = ['Nam', 'Nữ']
        invalid_genders = patients[~patients['gioi_tinh'].isin(valid_genders)]
        if len(invalid_genders) > 0:
            print(f"\nPATIENTS - Giới tính: {len(invalid_genders)} giá trị không hợp lệ")
            print(f"  Giá trị hợp lệ: {valid_genders}")
        else:
            print(f"\nPATIENTS - Giới tính: Tất cả giá trị đều hợp lệ ✓")
    
    # Kiểm tra nhóm tuổi
    if 'nhom_tuoi' in patients.columns:
        valid_age_groups = ['Trẻ em', 'Thanh niên', 'Trung niên', 'Cao tuổi']
        invalid_age_groups = patients[~patients['nhom_tuoi'].isin(valid_age_groups)]
        if len(invalid_age_groups) > 0:
            print(f"PATIENTS - Nhóm tuổi: {len(invalid_age_groups)} giá trị không hợp lệ")
        else:
            print(f"PATIENTS - Nhóm tuổi: Tất cả giá trị đều hợp lệ ✓")
    
    # Kiểm tra loại khám trong MEDICAL_RECORDS
    mr = data['medical_records']
    if 'loai_kham' in mr.columns:
        valid_visit_types = ['Khám mới', 'Tái khám', 'Cấp cứu', 'Khám định kỳ', 'Tư vấn']
        invalid_visit_types = mr[~mr['loai_kham'].isin(valid_visit_types)]
        if len(invalid_visit_types) > 0:
            print(f"\nMEDICAL_RECORDS - Loại khám: {len(invalid_visit_types)} giá trị không hợp lệ")
        else:
            print(f"\nMEDICAL_RECORDS - Loại khám: Tất cả giá trị đều hợp lệ ✓")

validate_categorical_values(data)
```

---

### **BƯỚC 10: TẠO BÁO CÁO TỔNG HỢP**

#### 10.1. Tạo báo cáo tổng hợp về chất lượng dữ liệu
```python
def generate_summary_report(data, missing_report, duplicate_report, integrity_issues, consistency_issues, outliers_report):
    """Tạo báo cáo tổng hợp về chất lượng dữ liệu"""
    
    print("\n" + "="*80)
    print("BÁO CÁO TỔNG HỢP CHẤT LƯỢNG DỮ LIỆU")
    print("="*80)
    
    report = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'tables': {}
    }
    
    for name, df in data.items():
        table_report = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'missing_values': df.isnull().sum().sum(),
            'duplicate_rows': df.duplicated().sum(),
            'data_types': df.dtypes.to_dict()
        }
        
        # Thêm thông tin cụ thể về missing values
        missing_cols = df.columns[df.isnull().any()].tolist()
        if missing_cols:
            table_report['columns_with_missing'] = {
                col: int(df[col].isnull().sum()) 
                for col in missing_cols
            }
        
        report['tables'][name] = table_report
        
        print(f"\n{name.upper()}:")
        print(f"  - Tổng số dòng: {table_report['total_rows']:,}")
        print(f"  - Tổng số cột: {table_report['total_columns']}")
        print(f"  - Tổng giá trị thiếu: {table_report['missing_values']}")
        print(f"  - Dòng trùng lặp: {table_report['duplicate_rows']}")
    
    # Lưu báo cáo ra file
    import json
    with open('data_quality_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"\n✓ Đã lưu báo cáo vào file: data_quality_report.json")
    
    return report

summary_report = generate_summary_report(
    data, missing_report, duplicate_report, 
    integrity_issues, consistency_issues, outliers_report
)
```

---

### **BƯỚC 11: LƯU DỮ LIỆU ĐÃ PREPROCESSING**

#### 11.1. Lưu các bảng đã được làm sạch
```python
def save_cleaned_data(data, output_dir='healthcare_data_large_cleaned/'):
    """Lưu dữ liệu đã được làm sạch"""
    import os
    
    # Tạo thư mục output nếu chưa có
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n" + "="*80)
    print("LƯU DỮ LIỆU ĐÃ LÀM SẠCH")
    print("="*80)
    
    for name, df in data.items():
        output_file = os.path.join(output_dir, f"{name}_cleaned.csv")
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"✓ Đã lưu {output_file}: {len(df):,} dòng")
    
    print(f"\n✓ Hoàn tất! Tất cả dữ liệu đã được lưu vào thư mục: {output_dir}")

save_cleaned_data(data)
```

---

## 📊 TÓM TẮT QUY TRÌNH

1. ✅ **Bước 1**: Thiết lập môi trường và import thư viện
2. ✅ **Bước 2**: Đọc dữ liệu và kiểm tra cơ bản
3. ✅ **Bước 3**: Kiểm tra và xử lý dữ liệu thiếu
4. ✅ **Bước 4**: Kiểm tra và xóa dữ liệu trùng lặp
5. ✅ **Bước 5**: Kiểm tra tính toàn vẹn tham chiếu
6. ✅ **Bước 6**: Chuẩn hóa định dạng dữ liệu
7. ✅ **Bước 7**: Kiểm tra tính nhất quán dữ liệu
8. ✅ **Bước 8**: Phát hiện và xử lý outliers
9. ✅ **Bước 9**: Kiểm tra định dạng và giá trị hợp lệ
10. ✅ **Bước 10**: Tạo báo cáo tổng hợp
11. ✅ **Bước 11**: Lưu dữ liệu đã preprocessing

---

## 🔧 LƯU Ý KHI THỰC HIỆN

1. **Backup dữ liệu gốc**: Luôn giữ bản sao của dữ liệu gốc trước khi preprocessing
2. **Kiểm tra từng bước**: Chạy và kiểm tra kết quả sau mỗi bước
3. **Ghi chú các quyết định**: Ghi lại lý do cho các quyết định xử lý dữ liệu
4. **Xử lý outliers cẩn thận**: Không nên xóa outliers một cách tùy tiện
5. **Kiểm tra lại sau khi xử lý**: Đảm bảo không làm mất dữ liệu quan trọng

---

## 📁 CẤU TRÚC FILE SAU KHI HOÀN THÀNH

```
healthcare_data_large/
├── patients.csv (gốc)
├── doctors.csv (gốc)
├── medical_records.csv (gốc)
├── medications.csv (gốc)
├── diagnoses.csv (gốc)
└── README.md

healthcare_data_large_cleaned/
├── patients_cleaned.csv
├── doctors_cleaned.csv
├── medical_records_cleaned.csv
├── medications_cleaned.csv
└── diagnoses_cleaned.csv

data_quality_report.json
preprocessing_healthcare_data.py
```

---

**Chúc bạn thực hiện preprocessing thành công! 🎉**

