# Kế hoạch đồ án: Hệ thống quản lý sân bóng đá

Học phần: Phần mềm mã nguồn mở (GV: Nguyễn Dũng, HUSC), học kỳ I 2026–2027.
Người thực hiện: Nguyễn Văn Quân. Hiện làm **một mình** và tự review (có AI review hỗ trợ).
Phiên bản: 1.1 (27/10/2026, tuần 8). Bản 1.1: chốt Flask, đổi lộ trình theo chương slide, đặt tên tiếng Việt không dấu. File này là "bản thiết kế" mà mọi AI trong dự án phải bám theo.

## 1. Nguồn ý tưởng

Các chức năng dưới đây được rút gọn từ tài liệu môn Đồ án CNPM của nhóm HUSC-18:

- `HUSC-18_SRS_v2.0` (7 module M01–M07, 40+ use case)
- `SRS_M04` (Đặt sân và thanh toán, Quân viết)
- `HUSC-18_DB_Design_v1.0` (thiết kế CSDL cho SQL Server)
- Báo cáo niên luận đặt sân online (React + Node + Supabase + Redis + RAG chatbot)

Bộ SRS gốc được viết cho một nhóm nhiều người, nên không thể làm hết trong 7 tuần. Đồ án này lấy **lõi M04** (phần Quân nắm rõ nhất) cùng những gì tối thiểu để lõi đó chạy được. Code được viết lại bằng **Python**, vì học phần yêu cầu Python. Trong README phải ghi nguồn là các tài liệu SRS ở trên.

## 2. Vai trò người dùng

| Vai trò | Được làm gì |
|---|---|
| Khách (chưa đăng nhập) | Xem danh sách sân, xem lịch trống, đăng ký, đăng nhập |
| Khách hàng | Đặt sân, trả cọc (mô phỏng), xem đơn của mình, hủy đơn |
| Nhân viên | Xem lịch vận hành theo ngày, check-in, hoàn tất, đánh dấu không đến, thu tiền còn lại |
| Quản trị viên | Quản lý sân, giờ mở cửa, bảng giá, xem báo cáo |

Phân quyền phải được kiểm tra **ở server**, không được chỉ ẩn nút trên giao diện (theo CBR-M03-01).

## 3. Chức năng BẮT BUỘC (MVP)

| Mã | Chức năng | Lấy từ | Điểm hay để trình bày khi bảo vệ |
|---|---|---|---|
| F1 | Đăng ký, đăng nhập, đăng xuất, phân quyền 3 vai trò | UC-M00-01/02, M01-01 | Mật khẩu được băm, không lưu dạng chữ thường |
| F2 | Quản lý sân: thêm, sửa, ngừng khai thác (ACTIVE/INACTIVE) | UC-M03-01 | Tên sân không được trùng |
| F3 | Giờ mở/đóng cửa, độ dài khung giờ, bảng giá theo khung (giờ thường, giờ cao điểm) | UC-M03-02/03 | Khung giờ tính theo nửa khoảng [bắt đầu, kết thúc) |
| F4 | Tìm sân và xem lịch trống theo ngày | UC-M02-01/02 | Khung đã qua hoặc đang bị giữ thì không bán |
| F5 | Đặt sân: 1 sân, 1 ngày, 1–4 khung liên tiếp. Giữ chỗ 10 phút, cọc 30%, chống trùng lịch | UC-M04-01, BR-M04-02/03/05/06/07 | Đây là "trái tim" của đồ án |
| F6 | Xem đơn của tôi, hủy đơn, tính tiền hoàn cọc 100/50/0% | UC-M04-04/05, BR-M04-19/21 | Hàm thuần, rất dễ viết unit test |
| F7 | Nhân viên: lịch theo ngày, check-in, hoàn tất, không đến, thu tiền còn lại | UC-M03-04..07, M04-06 | Máy trạng thái đơn đặt sân |
| F8 | REST API JSON cho sân, lịch trống, đơn đặt | Yêu cầu học phần | Kiểm thử được bằng pytest hoặc Postman |
| F9 | Báo cáo số đơn và doanh thu theo ngày/tháng | UC-M07-01/02 | Truy vấn GROUP BY |

## 4. Chức năng MỞ RỘNG (chỉ làm nếu MVP xong trước tuần 14)

| Mã | Chức năng | Lấy từ | Ghi chú |
|---|---|---|---|
| E1 | Chatbot FAQ: admin nhập câu hỏi/đáp, khách hỏi thì hệ thống tìm FAQ gần nhất theo từ khóa | UC-M02-03/04 | Không dùng OpenAI vì là dịch vụ đóng, tốn phí và cần khóa API |
| E2 | Tìm đội đối thủ: đăng bài từ đơn đã xác nhận, đội khác gửi yêu cầu, chủ bài chọn | UC-M05-01..06 | Hợp làm chuyên đề buổi 14 |
| E3 | Thông báo trong hệ thống (đặt thành công, bị hủy...) | UC-M06-01 | |
| E4 | Nhân viên đặt sân giúp khách vãng lai, thu cọc tiền mặt | UC-M04-03 | |

## 5. KHÔNG làm (lý do để trả lời thầy)

- **Cổng thanh toán thật (payOS/VietQR):** cần tài khoản doanh nghiệp và khóa bí mật. Thay bằng nút "Thanh toán cọc (mô phỏng)" có ghi chú rõ ràng.
- **Redis, Socket.IO, cập nhật thời gian thực:** nhiều công cụ cần cài. Thay bằng kiểm tra hạn giữ chỗ ngay khi truy vấn và chống trùng trong một transaction.
- **RAG/GPT:** dịch vụ đóng, không hợp tinh thần môn học.
- **Quên mật khẩu qua email, gia hạn giờ, xử lý sự cố sân, hoàn tiền qua ngân hàng chi tiết, audit log:** vượt quá sức một người trong 7 tuần.

## 6. Quy tắc nghiệp vụ cốt lõi (code và test phải theo đúng)

1. Một yêu cầu đặt gồm 1 sân, 1 ngày, 1–4 khung giờ **liên tiếp**, chưa bắt đầu (BR-M04-02).
2. Kiểm tra lại toàn bộ khung giờ ngay lúc xác nhận. Chỉ cần một khung bận là không giữ khung nào (BR-M04-03).
3. Hạn giữ chỗ = min(lúc tạo + 10 phút, giờ bắt đầu khung đầu tiên) (BR-M04-05).
4. Giá từng khung được chốt (snapshot) tại lúc giữ chỗ (BR-M04-06).
5. Tiền cọc = 30% tổng giá, **làm tròn lên bội số 1.000đ** (theo DB Design; SRS để TBD).
6. Chỉ hủy được toàn bộ đơn CONFIRMED, trước giờ bắt đầu. Hoàn cọc theo thời gian còn lại: ≥24h hoàn 100%; từ 12h đến dưới 24h hoàn 50%; dưới 12h hoàn 0%. Đúng 24h tính mức 100%, đúng 12h tính mức 50% (BR-M04-19/21).
7. Lưu thời gian theo UTC, hiển thị theo giờ `Asia/Ho_Chi_Minh`. Tiền là số nguyên, đơn vị VND.

Trạng thái đơn đặt sân (bản rút gọn, gộp "lượt giữ chỗ" vào "đơn"):

```
HOLDING --trả cọc--> CONFIRMED --check-in--> CHECKED_IN --hoàn tất--> COMPLETED
HOLDING --quá hạn giữ--> EXPIRED
CONFIRMED --hủy trước giờ--> CANCELLED
CONFIRMED --quá giờ, khách không đến--> NO_SHOW
```

## 7. Cơ sở dữ liệu MVP (6 bảng, chi tiết làm ở Bước 2)

Tên bảng đặt bằng tiếng Việt không dấu (xem `tai-lieu/quy-uoc-nhanh-va-dat-ten.md`), có đối chiếu với DB Design gốc:

| Bảng đồ án | Bảng trong DB Design HUSC-18 |
|---|---|
| `nguoi_dung` | `users` |
| `san` | `fields` |
| `bang_gia` | `field_prices` (rút gọn: giá theo khoảng giờ, không theo từng slot) |
| `don_dat_san` | `holds` + `bookings` (gộp làm một) |
| `khung_gio_dat` | `hold_slots` + `booking_slots` |
| `thanh_toan` | `payments` |
Bản DB Design gốc dùng kiểu dữ liệu riêng của SQL Server (NVARCHAR, DATETIME2, SYSUTCDATETIME). Ở đây chuyển sang kiểu chung của SQLAlchemy để chạy được trên cả SQLite và PostgreSQL.

## 8. Công nghệ và giấy phép

| Thành phần | Công nghệ | Giấy phép |
|---|---|---|
| Ngôn ngữ | Python ≥ 3.11 (máy đang có 3.13) | PSF License |
| Web framework | Flask (thầy dạy từ Chương 3) | BSD-3-Clause |
| Giao diện | Bootstrap 5 (Chương 4) | MIT |
| Template | Jinja2 | BSD-3-Clause |
| ORM / migration | SQLAlchemy 2.x / Alembic | MIT / MIT |
| CSDL dev/test | SQLite (có sẵn trong Python) | Public domain |
| CSDL triển khai | PostgreSQL (chốt ở buổi 13) | PostgreSQL License |
| Kiểm thử / chất lượng | pytest, pytest-cov, Ruff, mypy | MIT |
| Đóng gói / CI | Docker, GitHub Actions | Apache-2.0 / dịch vụ GitHub |
| Giấy phép của đồ án | Đề xuất MIT (chốt và lập luận ở buổi 15) | |

**Không dùng SQL Server 2014**: đây là phần mềm đóng, không hợp yêu cầu mã nguồn mở và đã hết hỗ trợ. MySQL Community (GPLv2) là mã nguồn mở nhưng không nằm trong ngăn xếp thầy dùng, nên chỉ để dự phòng.

## 9. Lộ trình theo chương slide (mỗi chương là một phiên bản)

Nhánh và tag đặt theo `tai-lieu/quy-uoc-nhanh-va-dat-ten.md`. Mỗi chương làm bản sân bóng **tương đương** với bài tập dự án LibraryMS của chương đó.

| Slide | Nhánh | Tag | Việc của đồ án |
|---|---|---|---|
| Bài 1–2 | `cau-hinh/khoi-tao-kho-ma` | | Repo công khai, README, LICENSE MIT kèm lập luận, `.gitignore`, `.venv` |
| Chương 3 | `tinh-nang/c03-flask-can-ban` | v0.1 | Dữ liệu sân tạm trong list; `/` thống kê, `/san` lọc theo loại, `/san/<id>` chi tiết, `/api/san`, `/api/san/<id>`; trang 404; `url_for`, `escape` |
| Chương 4 | `tinh-nang/c04-giao-dien-jinja2` | v0.2 | Template kế thừa, Bootstrap, macro thẻ sân và nhãn trạng thái, filter `vnd`, context processor |
| Chương 5 (Form) | `tinh-nang/c05-...` | v0.3 | Dự kiến: form thêm/sửa sân (F2) |
| Chương 6 (CSDL) | `tinh-nang/c06-...` | v0.4 | Dự kiến: chuyển dữ liệu từ list sang CSDL |
| Các chương sau | | | Đặt tên khi có slide: F1, F3–F9, kiểm thử, CI/CD, triển khai |

Nếu slide yêu cầu khác với bảng trên thì **làm theo slide** và cập nhật lại bảng này.
Hạn bảo vệ là tuần 15 (14–20/12/2026). Chương 3 và 4 đang bị trễ, cần làm xong v0.1 và v0.2 trong tuần 8–9.

## 10. Việc còn treo

- [x] Làm một mình, tự review (27/10). Vẫn nên hỏi thầy cách tính "lượt review".
- [x] Framework: Flask (slide Chương 3–4).
- [ ] Nơi triển khai: chốt theo slide buổi 13.
