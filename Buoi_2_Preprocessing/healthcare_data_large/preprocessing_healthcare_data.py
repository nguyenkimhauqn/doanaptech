"""
SCRIPT PREPROCESSING DỮ LIỆU Y TẾ
Hướng dẫn: Xem file KE_HOACH_PREPROCESSING.md để biết chi tiết từng bước
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
import os
import json
import re

warnings.filterwarnings('ignore')

# Thiết lập hiển thị
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)
pd.set_option('display.width', None)

# ============================================================================
# BƯỚC 1: THIẾT LẬP MÔI TRƯỜNG
# ============================================================================

# Đường dẫn thư mục
DATA_DIR = "./"

# Danh sách các file cần xử lý
FILES = {
    'patients': 'patients.csv',
    'doctors': 'doctors.csv',
    'medical_records': 'medical_records.csv',
    'medications': 'medications.csv',
    'diagnoses': 'diagnoses.csv'
}

# ============================================================================
# BƯỚC 2: ĐỌC DỮ LIỆU
# ============================================================================

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

# ============================================================================
# BƯỚC 3: KIỂM TRA DỮ LIỆU THIẾU
# ============================================================================

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

def handle_missing_patients(df):
    """Xử lý dữ liệu thiếu trong bảng patients"""
    df_clean = df.copy()
    
    # Email: Thay thế bằng giá trị mặc định hoặc tạo từ patient_id
    if df_clean['email'].isnull().any():
        mask = df_clean['email'].isnull()
        df_clean.loc[mask, 'email'] = df_clean.loc[mask, 'patient_id'].str.lower() + '@email.com'
    
    # Tiền sử bệnh: Thay thế 'Không' nếu thiếu
    if 'tien_su_benh' in df_clean.columns and df_clean['tien_su_benh'].isnull().any():
        df_clean['tien_su_benh'].fillna('Không', inplace=True)
    
    # Dị ứng: Thay thế 'Không' nếu thiếu
    if 'di_ung' in df_clean.columns and df_clean['di_ung'].isnull().any():
        df_clean['di_ung'].fillna('Không', inplace=True)
    
    return df_clean

def handle_missing_medical_records(df):
    """Xử lý dữ liệu thiếu trong bảng medical_records"""
    df_clean = df.copy()
    
    # Ghi chú: Thay thế bằng chuỗi rỗng nếu thiếu
    if 'ghi_chu' in df_clean.columns and df_clean['ghi_chu'].isnull().any():
        df_clean['ghi_chu'].fillna('', inplace=True)
    
    # Kết quả xét nghiệm: Thay thế 'Chưa có kết quả' nếu thiếu
    if 'ket_qua_xet_nghiem' in df_clean.columns and df_clean['ket_qua_xet_nghiem'].isnull().any():
        df_clean['ket_qua_xet_nghiem'].fillna('Chưa có kết quả', inplace=True)
    
    return df_clean

def handle_missing_diagnoses(df):
    """Xử lý dữ liệu thiếu trong bảng diagnoses"""
    df_clean = df.copy()
    
    # Ghi chú: Thay thế bằng chuỗi rỗng nếu thiếu
    if 'ghi_chu' in df_clean.columns and df_clean['ghi_chu'].isnull().any():
        df_clean['ghi_chu'].fillna('', inplace=True)
    
    return df_clean

def handle_all_missing_values(data):
    """Xử lý tất cả dữ liệu thiếu"""
    data_clean = {}
    data_clean['patients'] = handle_missing_patients(data['patients'])
    data_clean['doctors'] = data['doctors'].copy()  # Giả sử không cần xử lý
    data_clean['medical_records'] = handle_missing_medical_records(data['medical_records'])
    data_clean['medications'] = data['medications'].copy()  # Giả sử không cần xử lý
    data_clean['diagnoses'] = handle_missing_diagnoses(data['diagnoses'])
    
    return data_clean

# ============================================================================
# BƯỚC 4: KIỂM TRA DỮ LIỆU TRÙNG LẶP
# ============================================================================

def check_duplicates(data):
    """Kiểm tra và báo cáo dữ liệu trùng lặp"""
    print("\n" + "="*80)
    print("KIỂM TRA DỮ LIỆU TRÙNG LẶP")
    print("="*80)
    
    duplicate_report = {}
    
    for name, df in data.items():
        # Tìm khóa chính của từng bảng
        key_cols = {
            'patients': 'patient_id',
            'doctors': 'doctor_id',
            'medical_records': 'record_id',
            'medications': 'medication_id',
            'diagnoses': 'diagnosis_id'
        }
        
        key_col = key_cols.get(name)
        
        # Kiểm tra trùng lặp theo khóa chính
        if key_col and key_col in df.columns:
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

def remove_duplicates(data):
    """Xóa dữ liệu trùng lặp"""
    data_clean = {}
    
    key_cols = {
        'patients': 'patient_id',
        'doctors': 'doctor_id',
        'medical_records': 'record_id',
        'medications': 'medication_id',
        'diagnoses': 'diagnosis_id'
    }
    
    for name, df in data.items():
        df_clean = df.copy()
        key_col = key_cols.get(name)
        
        # Xóa trùng lặp theo khóa chính (giữ dòng đầu tiên)
        if key_col and key_col in df_clean.columns:
            before = len(df_clean)
            df_clean = df_clean.drop_duplicates(subset=[key_col], keep='first')
            after = len(df_clean)
            if before != after:
                print(f"{name}: Đã xóa {before - after} dòng trùng lặp")
        
        # Xóa dòng hoàn toàn trùng lặp
        before = len(df_clean)
        df_clean = df_clean.drop_duplicates(keep='first')
        after = len(df_clean)
        if before != after:
            print(f"{name}: Đã xóa {before - after} dòng hoàn toàn trùng lặp")
        
        data_clean[name] = df_clean
    
    return data_clean

# ============================================================================
# BƯỚC 5: KIỂM TRA TÍNH TOÀN VẸN THAM CHIẾU
# ============================================================================

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

# ============================================================================
# BƯỚC 6: CHUẨN HÓA ĐỊNH DẠNG DỮ LIỆU
# ============================================================================

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
        data_clean['diagnoses']['ty_le_hoi_phuc'] = data_clean['diagnoses']['ty_le_hoi_phuc'].astype(str).str.rstrip('%')
        data_clean['diagnoses']['ty_le_hoi_phuc'] = pd.to_numeric(
            data_clean['diagnoses']['ty_le_hoi_phuc'],
            errors='coerce'
        )
    
    return data_clean

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

# ============================================================================
# BƯỚC 7: KIỂM TRA TÍNH NHẤT QUÁN DỮ LIỆU
# ============================================================================

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
        current_year = datetime.now().year
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
    
    return issues

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

# ============================================================================
# BƯỚC 8: PHÁT HIỆN OUTLIERS
# ============================================================================

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
    
    return outliers_report

# ============================================================================
# BƯỚC 9: KIỂM TRA ĐỊNH DẠNG
# ============================================================================

def validate_emails(data):
    """Kiểm tra định dạng email"""
    print("\n" + "="*80)
    print("KIỂM TRA ĐỊNH DẠNG EMAIL")
    print("="*80)
    
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

def validate_phone_numbers(data):
    """Kiểm tra định dạng số điện thoại Việt Nam"""
    print("\n" + "="*80)
    print("KIỂM TRA ĐỊNH DẠNG SỐ ĐIỆN THOẠI")
    print("="*80)
    
    # Số điện thoại Việt Nam: 10 số, bắt đầu bằng 0
    phone_pattern = r'^0\d{9}$'
    
    # Kiểm tra trong PATIENTS
    patients = data['patients']
    if 'so_dien_thoai' in patients.columns:
        phone_str = patients['so_dien_thoai'].astype(str)
        invalid_phones = patients[~phone_str.str.match(phone_pattern, na=False)]
        if len(invalid_phones) > 0:
            print(f"\nPATIENTS: {len(invalid_phones)} số điện thoại không hợp lệ")
        else:
            print(f"\nPATIENTS: Tất cả số điện thoại đều hợp lệ ✓")
    
    # Kiểm tra trong DOCTORS
    doctors = data['doctors']
    if 'so_dien_thoai' in doctors.columns:
        phone_str = doctors['so_dien_thoai'].astype(str)
        invalid_phones = doctors[~phone_str.str.match(phone_pattern, na=False)]
        if len(invalid_phones) > 0:
            print(f"DOCTORS: {len(invalid_phones)} số điện thoại không hợp lệ")
        else:
            print(f"DOCTORS: Tất cả số điện thoại đều hợp lệ ✓")

# ============================================================================
# BƯỚC 10: TẠO BÁO CÁO
# ============================================================================

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
            'missing_values': int(df.isnull().sum().sum()),
            'duplicate_rows': int(df.duplicated().sum())
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
    with open('data_quality_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"\n✓ Đã lưu báo cáo vào file: data_quality_report.json")
    
    return report

# ============================================================================
# BƯỚC 11: LƯU DỮ LIỆU
# ============================================================================

def save_cleaned_data(data, output_dir='healthcare_data_large_cleaned/'):
    """Lưu dữ liệu đã được làm sạch"""
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

# ============================================================================
# HÀM CHÍNH - CHẠY TẤT CẢ CÁC BƯỚC
# ============================================================================

def main():
    """Hàm chính thực hiện toàn bộ quy trình preprocessing"""
    
    print("="*80)
    print("BẮT ĐẦU QUY TRÌNH PREPROCESSING DỮ LIỆU Y TẾ")
    print("="*80)
    
    # Bước 2: Đọc dữ liệu
    print("\n>>> BƯỚC 2: ĐỌC DỮ LIỆU")
    data = load_data()
    basic_info(data)
    
    # Bước 3: Kiểm tra dữ liệu thiếu
    print("\n>>> BƯỚC 3: KIỂM TRA DỮ LIỆU THIẾU")
    missing_report = check_missing_values(data)
    data = handle_all_missing_values(data)
    
    # Bước 4: Kiểm tra trùng lặp
    print("\n>>> BƯỚC 4: KIỂM TRA DỮ LIỆU TRÙNG LẶP")
    duplicate_report = check_duplicates(data)
    data = remove_duplicates(data)
    
    # Bước 5: Kiểm tra tính toàn vẹn tham chiếu
    print("\n>>> BƯỚC 5: KIỂM TRA TÍNH TOÀN VẸN THAM CHIẾU")
    integrity_issues = check_referential_integrity(data)
    if integrity_issues:
        data = fix_referential_integrity(data, integrity_issues)
    
    # Bước 6: Chuẩn hóa định dạng
    print("\n>>> BƯỚC 6: CHUẨN HÓA ĐỊNH DẠNG DỮ LIỆU")
    data = standardize_dates(data)
    data = standardize_numeric(data)
    data = standardize_strings(data)
    
    # Bước 7: Kiểm tra tính nhất quán
    print("\n>>> BƯỚC 7: KIỂM TRA TÍNH NHẤT QUÁN DỮ LIỆU")
    consistency_issues = check_data_consistency(data)
    if consistency_issues:
        data = fix_consistency(data, consistency_issues)
    
    # Bước 8: Phát hiện outliers
    print("\n>>> BƯỚC 8: PHÁT HIỆN DỮ LIỆU NGOẠI LAI")
    outliers_report = detect_outliers(data)
    
    # Bước 9: Kiểm tra định dạng
    print("\n>>> BƯỚC 9: KIỂM TRA ĐỊNH DẠNG")
    validate_emails(data)
    validate_phone_numbers(data)
    
    # Bước 10: Tạo báo cáo
    print("\n>>> BƯỚC 10: TẠO BÁO CÁO TỔNG HỢP")
    summary_report = generate_summary_report(
        data, missing_report, duplicate_report, 
        integrity_issues, consistency_issues, outliers_report
    )
    
    # Bước 11: Lưu dữ liệu
    print("\n>>> BƯỚC 11: LƯU DỮ LIỆU ĐÃ PREPROCESSING")
    save_cleaned_data(data)
    
    print("\n" + "="*80)
    print("HOÀN TẤT QUY TRÌNH PREPROCESSING!")
    print("="*80)
    
    return data

# Chạy chương trình
if __name__ == "__main__":
    cleaned_data = main()

