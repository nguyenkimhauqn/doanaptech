#!/bin/bash

# Script cài đặt và chạy Streamlit Dashboard
# Tự động kiểm tra và cài đặt dependencies

echo "🏥 =========================================="
echo "   CÀI ĐẶT VÀ CHẠY STREAMLIT DASHBOARD"
echo "   ========================================== 🏥"
echo ""

# Bước 1: Kiểm tra Python
echo "📌 Bước 1: Kiểm tra Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 không được cài đặt!"
    exit 1
fi
echo "✅ Python: $(python3 --version)"
echo ""

# Bước 2: Kiểm tra pip
echo "📌 Bước 2: Kiểm tra pip..."
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "❌ pip không được cài đặt!"
    exit 1
fi
echo "✅ pip sẵn sàng"
echo ""

# Bước 3: Cài đặt dependencies
echo "📌 Bước 3: Cài đặt dependencies..."
echo "   (Có thể mất vài phút...)"
echo ""

pip install streamlit pandas numpy matplotlib seaborn scikit-learn plotly

echo ""
echo "✅ Đã cài đặt tất cả dependencies!"
echo ""

# Bước 4: Kiểm tra file
echo "📌 Bước 4: Kiểm tra file..."
if [ ! -f "analysis_dashboard.py" ]; then
    echo "❌ Không tìm thấy file analysis_dashboard.py"
    echo "   Đảm bảo bạn đang ở thư mục App/"
    exit 1
fi

if [ ! -f "result.csv" ]; then
    echo "⚠️  CẢNH BÁO: Không tìm thấy file result.csv"
    echo "   Dashboard có thể không hoạt động!"
    echo ""
fi

echo "✅ File analysis_dashboard.py tồn tại"
echo ""

# Bước 5: Chạy dashboard
echo "📌 Bước 5: Khởi động Dashboard..."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🌐 Dashboard sẽ mở tại: http://localhost:8501"
echo "⚠️  Để dừng: Nhấn Ctrl+C"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

streamlit run analysis_dashboard.py

