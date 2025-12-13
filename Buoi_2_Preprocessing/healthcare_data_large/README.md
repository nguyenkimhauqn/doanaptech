# TẬP DỮ LIỆU Y TẾ - HEALTHCARE DATASET

## 📊 TỔNG QUAN

Tập dữ liệu y tế bao gồm **5 bảng CSV** có quan hệ với nhau, tổng cộng **720,000 dòng dữ liệu**.

---

## 📁 CÁC BẢNG DỮ LIỆU

### 1️⃣ **MEDICAL_RECORDS.CSV** - BẢNG CHÍNH ⭐
- **Số lượng:** 400,000 dòng
- **Số cột:** 22 cột
- **Mô tả:** Hồ sơ bệnh án chi tiết của bệnh nhân

**Các cột:**
1. `record_id` - Mã hồ sơ (HS00000001...)
2. `patient_id` - Mã bệnh nhân (khóa ngoại → patients)
3. `doctor_id` - Mã bác sĩ (khóa ngoại → doctors)
4. `diagnosis_id` - Mã chẩn đoán (khóa ngoại → diagnoses)
5. `medication_id` - Mã thuốc (khóa ngoại → medications)
6. `ngay_kham` - Ngày khám (YYYY-MM-DD)
7. `gio_kham` - Giờ khám (HH:MM)
8. `chuyen_khoa` - Chuyên khoa khám
9. `trieu_chung` - Triệu chứng của bệnh nhân
10. `chan_doan` - Chẩn đoán bệnh
11. `don_thuoc` - Tên thuốc được kê
12. `lieu_luong` - Liều lượng sử dụng
13. `so_ngay_dung_thuoc` - Số ngày dùng thuốc
14. `xet_nghiem` - Loại xét nghiệm
15. `ket_qua_xet_nghiem` - Kết quả xét nghiệm
16. `loai_kham` - Loại khám (Khám mới, Tái khám, Cấp cứu...)
17. `chi_phi_kham` - Chi phí khám bệnh (VNĐ)
18. `chi_phi_thuoc` - Chi phí thuốc (VNĐ)
19. `tong_chi_phi` - Tổng chi phí (VNĐ)
20. `loai_bao_hiem` - Loại bảo hiểm
21. `trang_thai` - Trạng thái (Đã hoàn thành, Đang điều trị...)
22. `ghi_chu` - Ghi chú thêm

---

### 2️⃣ **PATIENTS.CSV** - THÔNG TIN BỆNH NHÂN
- **Số lượng:** 80,000 dòng
- **Số cột:** 15 cột
- **Mô tả:** Thông tin cá nhân và y tế của bệnh nhân

**Các cột:**
1. `patient_id` - Mã bệnh nhân (KHÓA CHÍNH)
2. `ho_ten` - Họ và tên
3. `gioi_tinh` - Giới tính (Nam/Nữ)
4. `ngay_sinh` - Ngày sinh
5. `tuoi` - Tuổi
6. `nhom_tuoi` - Nhóm tuổi (Trẻ em, Thanh niên, Trung niên, Cao tuổi)
7. `nhom_mau` - Nhóm máu (A+, B+, O+, AB+...)
8. `so_dien_thoai` - Số điện thoại
9. `email` - Email
10. `dia_chi` - Địa chỉ chi tiết
11. `thanh_pho` - Thành phố
12. `tien_su_benh` - Tiền sử bệnh
13. `di_ung` - Dị ứng
14. `ngay_dang_ky` - Ngày đăng ký
15. `trang_thai` - Trạng thái sức khỏe

---

### 3️⃣ **DOCTORS.CSV** - THÔNG TIN BÁC SĨ
- **Số lượng:** 80,000 dòng
- **Số cột:** 12 cột
- **Mô tả:** Thông tin chi tiết về bác sĩ

**Các cột:**
1. `doctor_id` - Mã bác sĩ (KHÓA CHÍNH)
2. `ho_ten` - Họ và tên
3. `gioi_tinh` - Giới tính
4. `ngay_sinh` - Ngày sinh
5. `tuoi` - Tuổi
6. `chuyen_khoa` - Chuyên khoa
7. `trinh_do` - Trình độ (Bác sĩ, Thạc sĩ, Tiến sĩ, Giáo sư...)
8. `nam_kinh_nghiem` - Số năm kinh nghiệm
9. `so_dien_thoai` - Số điện thoại
10. `email` - Email
11. `phong_kham` - Phòng khám
12. `trang_thai` - Trạng thái làm việc

---

### 4️⃣ **MEDICATIONS.CSV** - DANH MỤC THUỐC
- **Số lượng:** 80,000 dòng
- **Số cột:** 10 cột
- **Mô tả:** Thông tin về các loại thuốc

**Các cột:**
1. `medication_id` - Mã thuốc (KHÓA CHÍNH)
2. `ten_thuoc` - Tên thuốc
3. `chuyen_khoa` - Chuyên khoa sử dụng
4. `hoat_chat` - Hoạt chất chính
5. `nha_san_xuat` - Nhà sản xuất
6. `gia_ban` - Giá bán (VNĐ)
7. `don_vi` - Đơn vị (Viên, Hộp, Chai...)
8. `quy_cach` - Quy cách đóng gói
9. `han_su_dung` - Hạn sử dụng
10. `trang_thai` - Trạng thái (Còn hàng, Hết hàng...)

---

### 5️⃣ **DIAGNOSES.CSV** - CHẨN ĐOÁN BỆNH
- **Số lượng:** 80,000 dòng
- **Số cột:** 10 cột
- **Mô tả:** Thông tin về các bệnh lý và chẩn đoán

**Các cột:**
1. `diagnosis_id` - Mã chẩn đoán (KHÓA CHÍNH)
2. `ma_benh` - Mã bệnh (ICD code)
3. `ten_benh` - Tên bệnh
4. `chuyen_khoa` - Chuyên khoa
5. `trieu_chung` - Triệu chứng điển hình
6. `mo_ta` - Mô tả bệnh
7. `muc_do_nghiem_trong` - Mức độ (Nhẹ, Trung bình, Nặng, Rất nặng)
8. `thoi_gian_dieu_tri_trung_binh` - Thời gian điều trị
9. `ty_le_hoi_phuc` - Tỷ lệ hồi phục (%)
10. `ghi_chu` - Ghi chú

---

## 🔗 QUAN HỆ GIỮA CÁC BẢNG

```
MEDICAL_RECORDS (Bảng chính - 400,000 dòng)
    ├─── patient_id ──→ PATIENTS.patient_id
    ├─── doctor_id ──→ DOCTORS.doctor_id
    ├─── diagnosis_id ──→ DIAGNOSES.diagnosis_id
    └─── medication_id ──→ MEDICATIONS.medication_id
```

---

## 🏥 CÁC CHUYÊN KHOA

1. **Tim mạch** - Các bệnh về tim và mạch máu
2. **Nội khoa** - Tiểu đường, thận, gan...
3. **Ngoại khoa** - Phẫu thuật, chấn thương...
4. **Nhi khoa** - Bệnh trẻ em
5. **Sản phụ khoa** - Thai nghén, phụ nữ
6. **Hô hấp** - Phổi, đường hô hấp
7. **Tiêu hóa** - Dạ dày, ruột, gan...
8. **Thần kinh** - Não, thần kinh

---

## ✅ ĐẶC ĐIỂM DỮ LIỆU

### Logic y khoa chính xác:
- ✓ Bệnh nhân được khám đúng chuyên khoa theo độ tuổi
- ✓ Triệu chứng phù hợp với chẩn đoán
- ✓ Thuốc phù hợp với bệnh và chuyên khoa
- ✓ Xét nghiệm phù hợp với chuyên khoa
- ✓ Chi phí phù hợp với loại khám

### Dữ liệu thực tế:
- ✓ Tên người Việt Nam
- ✓ Số điện thoại Việt Nam (090, 091, 093...)
- ✓ Địa chỉ Việt Nam
- ✓ Tên thuốc phổ biến tại VN
- ✓ Nhà sản xuất thuốc VN và quốc tế

---

## 📈 SỬ DỤNG DỮ LIỆU

### Phân tích có thể thực hiện:
- 📊 Phân tích xu hướng bệnh theo tuổi, giới tính
- 💰 Phân tích chi phí điều trị
- 📅 Phân tích lượng bệnh nhân theo thời gian
- 🏥 Hiệu suất làm việc của bác sĩ
- 💊 Phân tích sử dụng thuốc
- 🔬 Phân tích kết quả xét nghiệm
- 📍 Phân tích phân bố bệnh theo địa lý

### Ứng dụng:
- Machine Learning (dự đoán bệnh, chi phí...)
- Data Warehousing
- Business Intelligence (BI)
- Báo cáo thống kê
- Học tập và nghiên cứu

---

## 📂 VỊ TRÍ FILE

Tất cả các file CSV được lưu trong thư mục: **`healthcare_data_large/`**

---

## 🎯 YÊU CẦU ĐÃ HOÀN THÀNH

✅ 5 bảng dữ liệu có quan hệ  
✅ Bảng chính: 400,000 dòng, 22 cột (>20 cột)  
✅ Các bảng còn lại: 80,000 dòng mỗi bảng (>80,000 dòng)  
✅ Các bảng có tối thiểu 10 cột  
✅ Định dạng CSV với encoding UTF-8-BOM  
✅ Dữ liệu có logic y khoa chính xác  

---

**Tạo bởi:** generate_large_healthcare_data.py  
**Ngày tạo:** 2025-12-11  
**Tổng số dòng:** 720,000 dòng
