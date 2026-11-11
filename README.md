# Dự án kiểm thử tự động SauceDemo với Selenium

[![Regression Suite](https://github.com/Bhjtran/saucedemo-automation/actions/workflows/regression.yml/badge.svg)](https://github.com/Bhjtran/saucedemo-automation/actions/workflows/regression.yml)

Bộ test tự động cho trang demo [SauceDemo](https://www.saucedemo.com/) viết bằng
Python, Selenium WebDriver và Pytest theo mô hình Page Object Model.
Gồm 12 test UI (Selenium) và 4 test API (requests), kèm script Bash
`run_tests.sh` để chạy test và lưu log.

## CI/CD

Repo có pipeline GitHub Actions (`.github/workflows/regression.yml`) tự động
chạy mỗi khi push hoặc mở Pull Request vào nhánh `main`:

1. Cài Python + dependencies.
2. Cài Chrome for Testing (headless, không cần GUI).
3. Chạy bộ regression (`smoke` + `negative`) bằng `pytest`.
4. Upload báo cáo HTML (`reports/report.html`) và ảnh chụp lỗi (nếu có)
   thành artifact để xem lại ngay trên GitHub, không cần chạy local.

### Chạy riêng một test trên GitHub Actions

Vào tab **Actions** → **SauceDemo Regression Suite** → **Run workflow**, rồi
gõ test muốn chạy vào ô `test_target`, ví dụ:

- `tests/test_login.py` (cả file)
- `tests/test_cart.py::test_add_product_to_cart` (một test)

Để trống thì chạy nhóm `smoke` + `negative` như khi push.

## Chức năng đã kiểm thử

- Đăng nhập thành công.
- Đăng nhập thất bại với dữ liệu sai hoặc thiếu.
- Thêm một hoặc nhiều sản phẩm vào giỏ hàng.
- Xóa sản phẩm khỏi giỏ hàng.
- Kiểm tra tên sản phẩm trong giỏ.
- Sắp xếp sản phẩm theo giá và tên.
- Kiểm tra validation ở trang checkout (phải hiện lỗi thật trên trang).
- Kiểm tra tổng tiền: Total = Item total + Tax.
- Hoàn tất toàn bộ luồng đặt hàng.
- Đăng xuất.
- Tự động chụp ảnh khi test thất bại.
- Xuất báo cáo HTML tại `reports/report.html`.

## Test API

Thư mục `tests/api/` chứa 4 test API viết bằng thư viện `requests`, gọi
API công khai [JSONPlaceholder](https://jsonplaceholder.typicode.com):

- `GET /posts/1`: kiểm tra status 200 và dữ liệu trả về.
- `GET /posts?userId=1`: kiểm tra mọi bài viết trả về đều của user 1.
- `POST /posts`: kiểm tra status 201 và dữ liệu gửi lên được trả lại đúng.
- `GET /posts/99999`: kiểm tra status 404 (negative).

Test API không mở trình duyệt. Chạy riêng bằng:

```bash
pytest -m api
```

## Script Bash `run_tests.sh`

Script chạy pytest, lưu log có ngày giờ vào thư mục `logs/`, in số test
pass/fail, liệt kê test fail và trả mã thoát của pytest (dùng được với cron
hoặc CI). Log cũ hơn 7 ngày tự xóa.

```bash
./run_tests.sh                      # toàn bộ test
./run_tests.sh smoke                # nhóm smoke
./run_tests.sh api                  # test API
./run_tests.sh "smoke or negative"
```

Trên Windows chạy bằng Git Bash: `bash run_tests.sh smoke`.

Hẹn giờ bằng cron (Linux), ví dụ chạy smoke lúc 2 giờ sáng mỗi ngày:

```bash
0 2 * * * /home/tran/saucedemo_selenium_project_full/run_tests.sh smoke
```

## Cấu trúc

```text
saucedemo_selenium_project_full/
├── .github/workflows/      # Pipeline CI/CD (GitHub Actions)
│   └── regression.yml
├── .gitignore
├── .gitattributes          # Giữ xuống dòng kiểu Linux cho file .sh
├── pages/                  # Page Object Model
├── tests/                  # Test UI (pytest + Selenium)
│   └── api/                # Test API (pytest + requests)
├── screenshots/            # Ảnh kết quả/lỗi
├── reports/                # Báo cáo HTML
├── config.py
├── conftest.py
├── main.py                 # Demo end-to-end
├── pytest.ini
├── requirements.txt
├── run_tests.bat
└── run_tests.sh            # Script Bash chạy test, lưu log
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

Chạy một test cụ thể, hoặc lọc theo tên:

```bash
pytest tests/test_login.py::test_login_successfully
pytest -k sort
```

Chạy ẩn trình duyệt (headless) trên máy:

```bash
set HEADLESS=1 && pytest        # Windows (cmd)
HEADLESS=1 pytest               # Linux / macOS
```

## Kết quả

Sau khi chạy xong, mở file:

```text
reports/report.html
```

ChromeDriver thường được Selenium Manager tự tải và quản lý. Máy cần cài Google Chrome và có kết nối Internet trong lần chạy đầu tiên.
