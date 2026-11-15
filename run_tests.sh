#!/bin/bash
# Chạy test bằng pytest, lưu log có ngày giờ và in tóm tắt kết quả.
#
# Cách dùng:
#   ./run_tests.sh               chạy toàn bộ test
#   ./run_tests.sh smoke         chỉ chạy nhóm smoke
#   ./run_tests.sh api           chỉ chạy test API
#   ./run_tests.sh "smoke or negative"
#
# Hẹn giờ bằng cron, ví dụ chạy smoke lúc 2 giờ sáng mỗi ngày:
#   0 2 * * * /home/tran/saucedemo_selenium_project_full/run_tests.sh smoke

MARKER="$1"
LABEL="${MARKER:-all}"
LABEL="${LABEL// /_}"          # "smoke or negative" -> "smoke_or_negative" để đặt tên file

# Luôn chạy từ thư mục chứa script, kể cả khi cron gọi từ nơi khác.
cd "$(dirname "$0")" || exit 1

# Chọn lệnh Python chạy được và đã cài pytest. Trên Windows, "python3" có thể chỉ là
# lối tắt tới Microsoft Store, nên phải chạy thử chứ không chỉ kiểm tra lệnh có tồn tại.
if python3 -c "import pytest" > /dev/null 2>&1; then
    PYTHON=python3
elif python -c "import pytest" > /dev/null 2>&1; then
    PYTHON=python
else
    echo "Error: pytest not found. Activate the virtual environment and run: pip install -r requirements.txt"
    exit 1
fi

mkdir -p logs
LOG_FILE="logs/test_${LABEL}_$(date +%Y%m%d_%H%M%S).log"

echo "Start:  $(date '+%Y-%m-%d %H:%M:%S')"
echo "Marker: $LABEL"
echo "Log:    $LOG_FILE"

if [ -n "$MARKER" ]; then
    $PYTHON -m pytest -m "$MARKER" > "$LOG_FILE" 2>&1
else
    $PYTHON -m pytest > "$LOG_FILE" 2>&1
fi
EXIT_CODE=$?

# pytest -v in mỗi test một dòng, kết thúc bằng PASSED hoặc FAILED.
PASSED=$(grep -c " PASSED" "$LOG_FILE")
FAILED=$(grep -c " FAILED" "$LOG_FILE")

echo "Passed: $PASSED"
echo "Failed: $FAILED"

if [ "$FAILED" -gt 0 ]; then
    echo "Failed tests:"
    grep " FAILED" "$LOG_FILE" | awk '{print "  - " $1}'
fi

# Xóa log cũ hơn 7 ngày để thư mục logs không đầy dần.
find logs -name "*.log" -mtime +7 -delete

if [ "$EXIT_CODE" -eq 0 ]; then
    echo "Result: PASS"
else
    echo "Result: FAIL (pytest exit code $EXIT_CODE)"
fi

# Trả mã thoát của pytest để cron hoặc CI biết lần chạy có lỗi.
exit "$EXIT_CODE"
