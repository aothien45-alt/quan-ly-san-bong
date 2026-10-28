# Hệ thống quản lý sân bóng đá

Web app viết bằng Python (Flask) để quản lý việc cho thuê sân bóng đá:

- Khách xem danh sách sân và lịch trống, đặt sân (giữ chỗ 10 phút, trả cọc 30% dạng mô phỏng), xem và hủy đơn của mình.
- Nhân viên xem lịch theo ngày, check-in, thu tiền còn lại.
- Quản trị viên quản lý sân, giờ mở cửa, bảng giá và xem báo cáo doanh thu.

Đồ án học phần **Phần mềm mã nguồn mở**, Trường Đại học Khoa học, Đại học Huế (GV: Nguyễn Dũng).
Người thực hiện: Nguyễn Văn Quân.

## Trạng thái

**Đang phát triển.** Hiện đang ở giai đoạn khởi tạo kho mã (Bài 1–2), chưa có code ứng dụng.
Các trang xem sân đầu tiên sẽ có ở phiên bản `v0.1` (Chương 3).

## Công nghệ

| Thành phần | Công nghệ | Giấy phép | Trạng thái |
|---|---|---|---|
| Ngôn ngữ | Python ≥ 3.11 | PSF-2.0 | Đang dùng |
| Web framework | Flask | BSD-3-Clause | Đang dùng |
| Template | Jinja2 | BSD-3-Clause | Đang dùng |
| Phụ thuộc của Flask | Werkzeug, MarkupSafe, click, itsdangerous | BSD-3-Clause | Đang dùng |
| Phụ thuộc của Flask | blinker | MIT | Đang dùng |
| Giao diện | Bootstrap 5 | MIT | Dự kiến |
| ORM | SQLAlchemy | MIT | Dự kiến |
| Cơ sở dữ liệu | SQLite | Public domain | Dự kiến |
| Kiểm thử | pytest | MIT | Dự kiến |

Danh sách gói và phiên bản cụ thể nằm trong [requirements.txt](requirements.txt).

## Cài đặt và chạy

Cần có sẵn Python 3.11 trở lên và Git. Các lệnh dưới đây chạy trong PowerShell trên Windows:

```powershell
# 1. Tải mã nguồn về máy (thay <duong-dan-kho-ma> bằng địa chỉ kho trên GitHub)
git clone <duong-dan-kho-ma>
cd quan-ly-san-bong

# 2. Tạo môi trường ảo .venv
python -m venv .venv

# 3. Cài các thư viện cần dùng
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# 4. Kiểm tra đã cài được Flask
.\.venv\Scripts\python.exe -m flask --version
```

Hiện chưa có ứng dụng để chạy. Lệnh chạy web sẽ được bổ sung ở Chương 3.

## Nguồn tham khảo

Chức năng và quy tắc nghiệp vụ được rút gọn từ tài liệu môn **Đồ án Công nghệ phần mềm** của nhóm **HUSC-18**:

- `HUSC-18_SRS_v2.0`: đặc tả yêu cầu phần mềm (7 module M01–M07).
- `SRS_M04`: đặc tả module Đặt sân và thanh toán.
- `HUSC-18_DB_Design_v1.0`: thiết kế cơ sở dữ liệu (bản gốc cho SQL Server).

Đồ án này viết lại phần lõi bằng Python và chỉ dùng phần mềm mã nguồn mở. Chi tiết phạm vi xem ở [tai-lieu/ke-hoach-do-an.md](tai-lieu/ke-hoach-do-an.md).

## Sử dụng AI

Có sử dụng Claude Code hỗ trợ; người thực hiện đã đọc và hiểu toàn bộ thay đổi.
Quy tắc làm việc với AI ghi trong [CLAUDE.md](CLAUDE.md).

## Giấy phép

Mã nguồn trong kho này được phát hành theo [Giấy phép MIT](LICENSE).

`SPDX-License-Identifier: MIT`

Lý do chọn MIT xem tại [tai-lieu/ly-do-chon-giay-phep.md](tai-lieu/ly-do-chon-giay-phep.md).
