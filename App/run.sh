#!/bin/bash

# Script chạy Streamlit Dashboard nhanh
# Tác giả: Nguyễn Kim Hậu
# Ngày: 31/12/2025

echo "🏥 =================================="
echo "   STREAMLIT DASHBOARD - DỮ LIỆU Y TẾ"
echo "   ==================================🏥"
echo ""
echo "📊 Đang khởi động dashboard..."
echo ""
echo "✅ Dashboard sẽ tự động mở trong browser"
echo "🌐 URL: http://localhost:8501"
echo ""
echo "⚠️  Để dừng: Nhấn Ctrl+C"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Kiểm tra file result.csv
if [ ! -f "result.csv" ]; then
    echo "❌ CẢNH BÁO: Không tìm thấy file result.csv"
    echo "   Vui lòng đảm bảo file result.csv nằm trong thư mục App/"
    echo ""
    exit 1
fi

# Kiểm tra Streamlit đã cài
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit chưa được cài đặt!"
    echo "   Chạy: pip install -r requirements.txt"
    echo ""
    exit 1
fi

# Chạy dashboard
streamlit run analysis_dashboard.py

