# CLAUDE.md: quy tắc chung cho mọi AI làm việc trong dự án này

## Dự án
Hệ thống quản lý sân bóng đá: web app Python (Flask) có cơ sở dữ liệu và REST API.
Đây là đồ án học phần "Phần mềm mã nguồn mở" (HUSC, GV Nguyễn Dũng). Người làm là Nguyễn Văn Quân, làm một mình, mới học lập trình.
**Mục tiêu số 1: Quân tự giải thích được từng dòng code khi thầy hỏi.** Code ngắn, rõ, dễ hiểu luôn được ưu tiên hơn code "thông minh".

Tài liệu bắt buộc phải đọc trước khi làm:
- `tai-lieu/ke-hoach-do-an.md`: phạm vi chức năng (F1–F9, E1–E4), quy tắc nghiệp vụ, lộ trình.
- `tai-lieu/quy-uoc-nhanh-va-dat-ten.md`: **quy ước nhánh Git, đặt tên file/hàm/biến bằng tiếng Việt không dấu, cấu trúc thư mục.**
- `tai-lieu/y-tuong-cua-quan.md`: ý tưởng riêng của Quân.
- `slide-cua-thay/`: slide thầy phát theo từng chương. Thư mục này nằm trong .gitignore và không được commit.

## Công nghệ (chỉ dùng mã nguồn mở)
Python ≥ 3.11, Flask (thầy dạy Flask từ Chương 3), Jinja2, Bootstrap 5. Từ khi slide dạy đến: SQLAlchemy + Alembic, SQLite, pytest, Ruff, mypy.
- KHÔNG dùng SQL Server, OpenAI, payOS hay bất kỳ dịch vụ hoặc thư viện đóng nào.
- Trước khi thêm một thư viện mới: nêu tên, giấy phép, lý do cần dùng, rồi CHỜ Quân đồng ý. Thư viện được duyệt thì ghi vào `requirements.txt`.
- Luôn dùng môi trường ảo `.venv`. Gọi bằng `.\.venv\Scripts\python.exe -m pip ...` để không phụ thuộc vào việc đã kích hoạt venv hay chưa.

## Phạm vi: không làm dư thừa
- Chỉ làm đúng việc được giao, theo slide của chương hiện tại và `tai-lieu/ke-hoach-do-an.md`.
- Không tự thêm chức năng, file, thư viện hay "tối ưu" ngoài yêu cầu. Nếu thấy nên thêm gì, chỉ ĐỀ XUẤT ở cuối câu trả lời.
- Không tạo trước thư mục hoặc file của giai đoạn sau (xem mục 5.2 trong file quy ước).
- Mỗi lần chỉ làm một phần nhỏ, và phải chạy thử được.

## Đặt tên: tiếng Việt KHÔNG DẤU
Theo đúng `tai-lieu/quy-uoc-nhanh-va-dat-ten.md`. Tóm tắt:
- File và thư mục Python, hàm, biến, template: `snake_case` không dấu (`du_lieu_mau.py`, `tinh_tien_coc()`, `danh_sach_san.html`).
- Nhánh Git, URL, tài liệu `.md`: `kebab-case` không dấu (`tinh-nang/c03-flask-can-ban`, `/san/<int:ma_san>/lich-trong`).
- Class: `PascalCase` (`DonDatSan`). Hằng số: `CHU_HOA` (`TY_LE_COC`).
- Chỉ giữ tiếng Anh cho các tên do công cụ quy định (bảng ở mục 2 của file quy ước) và cho giá trị trạng thái lấy từ SRS (`HOLDING`, `CONFIRMED`...).
- Docstring và comment viết tiếng Việt CÓ dấu, ngắn gọn, giải thích VÌ SAO chứ không lặp lại code.
- Đầu mỗi file `.py` có 2 dòng SPDX (mục 6 của file quy ước).

## Quy tắc nghiệp vụ (không tự ý đổi)
Xem mục 6 trong `tai-lieu/ke-hoach-do-an.md`: giữ chỗ 10 phút, cọc 30% làm tròn lên 1.000đ, 1–4 khung liên tiếp, hoàn cọc 100/50/0%, khoảng thời gian [bắt đầu, kết thúc), lưu giờ UTC và hiển thị giờ Việt Nam, tiền là số nguyên VND.
Tính toán phức tạp làm trong Python, template chỉ hiển thị (nguyên tắc Chương 4). Khi đã có gói `ung_dung/`, logic nghiệp vụ đặt trong `ung_dung/nghiep_vu/` thành hàm thuần để dễ test.

## Bảo mật (theo slide Chương 3–4)
- Mọi URL sinh bằng `url_for`, kể cả file tĩnh. Không viết cứng URL.
- Không dùng `|safe` với dữ liệu người dùng. Trước Chương 4 (ghép chuỗi HTML) thì phải `escape()`.
- Trang lỗi phải trả kèm mã lỗi (404...). Không bật debug trên máy chủ triển khai.
- Mọi URL cần đăng nhập hoặc phân quyền đều phải kiểm tra quyền ở server. Mật khẩu phải băm.
- Bí mật (SECRET_KEY...) đọc từ `.env`. Chỉ commit `.env.example`, không bao giờ commit `.env`.

## An toàn: BẮT BUỘC
- Máy là Windows; terminal trong VS Code là PowerShell. Viết lệnh theo cú pháp PowerShell.
- KHÔNG chạy các lệnh xóa hoặc phá: `rm`, `del`, `Remove-Item`, `rmdir`, `git reset --hard`, `git clean`, `git push --force`, `git checkout -- .`, `git branch -D`, `DROP TABLE`. Nếu thật sự cần, DỪNG lại, giải thích lý do và hậu quả, rồi để Quân tự chạy.
- KHÔNG đọc, in ra hay sửa file `.env`.
- KHÔNG tạo nhánh, `git commit`, `git merge`, `git push` khi Quân chưa yêu cầu rõ ràng. Mặc định chỉ đề xuất lệnh và commit message, Quân tự chạy.
- Trước khi sửa file, kiểm tra đang ở đúng nhánh (`git branch --show-current`). Nếu đang ở `main` thì DỪNG và nhắc Quân tạo nhánh theo file quy ước.
- Không cài phần mềm hệ thống (winget, choco, installer...). Nếu cần, hướng dẫn để Quân tự cài.

## Lệnh kiểm tra (chạy khi các công cụ này đã có trong dự án)
```powershell
.\.venv\Scripts\python.exe -m flask --app app routes
.\.venv\Scripts\python.exe -m flask --app app run --debug --port 8000
.\.venv\Scripts\python.exe -m pytest --cov --cov-report=term-missing
.\.venv\Scripts\python.exe -m ruff check .
```

## Cách trả lời Quân (bằng tiếng Việt)
Sau mỗi thay đổi, luôn kết thúc bằng 5 mục sau:
1. **Đã làm gì**: liệt kê file đã tạo hoặc sửa, mỗi file 1 dòng.
2. **Vì sao làm vậy**: ý nghĩa, viết cho người mới học.
3. **Cách chạy thử**: lệnh cụ thể và kết quả mong đợi (URL nào, thấy gì).
4. **Câu hỏi thầy có thể hỏi**: 2–3 câu, kèm gợi ý trả lời ngắn.
5. **Commit message đề xuất**: theo mục 3.4 của file quy ước, ví dụ `feat(san): trang danh sách sân có lọc theo loại`.

## Ghi nguồn AI
Học phần chấp nhận code do AI hỗ trợ nếu có ghi nguồn. Thêm dòng sau vào mô tả mỗi PR: `Có sử dụng Claude Code hỗ trợ; người thực hiện đã đọc và hiểu toàn bộ thay đổi.`
