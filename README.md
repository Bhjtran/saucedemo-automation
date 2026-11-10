# Dự án kiểm thử tự động SauceDemo với Selenium

## Chức năng đã kiểm thử

- Đăng nhập thành công.
- Đăng nhập thất bại với dữ liệu sai hoặc thiếu.
- Thêm một hoặc nhiều sản phẩm vào giỏ hàng.
- Xóa sản phẩm khỏi giỏ hàng.
- Kiểm tra tên sản phẩm trong giỏ.
- Sắp xếp sản phẩm theo giá và tên.
- Kiểm tra validation ở trang checkout.
- Hoàn tất toàn bộ luồng đặt hàng.
- Tự động chụp ảnh khi test thất bại.
- Xuất báo cáo HTML tại `reports/report.html`.

## Cấu trúc

```text
saucedemo_selenium_project/
├── pages/                  # Page Object Model
├── tests/                  # Test cases pytest
├── screenshots/            # Ảnh kết quả/lỗi
├── reports/                # Báo cáo HTML
├── config.py
├── conftest.py
├── main.py                 # Demo end-to-end
├── pytest.ini
├── requirements.txt
└── run_tests.bat
```

## Cách chạy trên Windows

```bash
cd saucedemo_selenium_project
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pytest
```

Hoặc nhấp đúp `run_tests.bat`.

Chạy riêng luồng demo:

```bash
python main.py
```

Chạy nhóm smoke test:

```bash
pytest -m smoke
```

Chạy test đăng nhập:

```bash
pytest tests/test_login.py
```

## Kết quả

Sau khi chạy xong, mở file:

```text
reports/report.html
```

ChromeDriver thường được Selenium Manager tự tải và quản lý. Máy cần cài Google Chrome và có kết nối Internet trong lần chạy đầu tiên.
