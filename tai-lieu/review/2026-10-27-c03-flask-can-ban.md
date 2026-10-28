# Review nhánh `tinh-nang/c03-flask-can-ban` (27/10/2026)

- So với nhánh: `cau-hinh/khoi-tao-kho-ma`
- Đối chiếu: `slide-cua-thay/c03-flask-can-ban.txt`, `CLAUDE.md`, `tai-lieu/ke-hoach-do-an.md`, `tai-lieu/quy-uoc-nhanh-va-dat-ten.md`
- Người review: subagent `reviewer` (Claude Code)
- Phạm vi: 8 commit, 3 file: `app.py` (mới), `du_lieu_mau.py` (mới), `README.md`

## Tóm tắt

- Nghiêm trọng: 0, Cao: 0, Trung bình: 1, Gợi ý: 4.
- **Kết luận: Có thể commit.** Không có lỗi sai nghiệp vụ hay lỗ hổng bảo mật. Nên sửa mục Trung bình trước khi tạo PR và gắn tag `v0.1`.

Reviewer đã kiểm tra:
- `flask --app app routes` chạy được, đủ 6 route (`trang_chu`, `danh_sach_san`, `chi_tiet_san`, `api_danh_sach_san`, `api_chi_tiet_san`, `static`).
- Thử từng URL trong bảng của README bằng `app.test_client()`: mọi dòng đúng mã trạng thái và nội dung. `/san?loai_san=<b>x</b>` đã được escape.
- Ruff, mypy, pytest chưa cài trong `.venv` nên chưa kiểm tra được (slide chưa dạy).
- Git không theo dõi `.env`, `.venv`, `slide-cua-thay/`. Hai file `.py` đều có 2 dòng SPDX.

## Các vấn đề

### 🟡 [Trung bình] Tham số lọc chưa bỏ khoảng trắng: `app.py:61`
- **Vấn đề:** `request.args.get("loai_san", "")` lấy nguyên chuỗi người dùng gửi. Chuỗi chỉ có dấu cách vẫn được coi là "đã chọn loại".
- **Tình huống gây lỗi:** `/san?loai_san=%20` ra `Loại sân:  , có 0 sân.` và bảng trống. Gõ thừa dấu cách ở cuối như `?loai_san=Sân 7 người ` cũng ra 0 sân, dù loại này có 2 sân.
- **Lý do:** slide Lab 3 Bước 8 (trang 67) làm mẫu `request.args.get("q", "").strip()`.
- **Cách sửa:** `loai_dang_chon = request.args.get("loai_san", "").strip()`. Thêm dòng `/san?loai_san=%20` cho kết quả 200 và "Tất cả: 5 sân" vào bảng kiểm thử trong README.

### 🔵 [Gợi ý 1] Lỗi 404 dạng JSON được viết ở hai chỗ: `app.py:136-138` và `app.py:151-152`
- **Vấn đề:** `api_chi_tiet_san` tự trả `{"error": ...}, 404`, trong khi `trang_loi_404` cũng đã trả JSON cho mọi đường dẫn bắt đầu bằng `/api/`.
- **Lý do:** tiêu chí chấm (trang 73) có mục "Mã nguồn rõ ràng, không lặp".
- **Cách sửa:** dùng `abort(404, description=f"Không có sân với mã = {ma_san}")` như trang HTML, để `trang_loi_404` lo phần JSON. Kết quả `/api/san/99` không đổi.

### 🔵 [Gợi ý 2] Điều kiện `type(loi).description` khó giải thích: `app.py:144-146`
- **Vấn đề:** đúng và có comment, nhưng hơi "khéo léo" so với mục tiêu số 1 trong `CLAUDE.md`. Dòng comment 145 dài 103 ký tự.
- **Cách sửa (chọn một):** (a) giữ code, chuẩn bị câu trả lời; hoặc (b) `from werkzeug.exceptions import NotFound` rồi `if loi.description == NotFound.description:`. Nên tách dòng 145 thành 2 dòng.

### 🔵 [Gợi ý 3] Lọc ra 0 sân thì bảng trống mà không có câu báo: `app.py:80-104`
- **Vấn đề:** `/san?loai_san=xyz` hiện bảng chỉ có dòng tiêu đề. Slide Lab Bước 7 (trang 66) làm mẫu một dòng báo riêng khi không có dữ liệu.
- **Cách sửa:** nếu `cac_dong` rỗng thì gán `<tr><td colspan='5'>Không có sân nào thuộc loại này.</td></tr>`.

### 🔵 [Gợi ý 4] `/api` (không có `/` cuối) trả 404 dạng HTML: `app.py:151`
- **Vấn đề:** `/api/` và `/api/san/` trả JSON, còn `/api` trả HTML vì `startswith("/api/")` cần dấu `/` cuối. Rất hiếm gặp, slide không yêu cầu.
- **Cách sửa (nếu muốn):** `request.path == "/api" or request.path.startswith("/api/")`.

*Ngoài phạm vi, không tính là lỗi:* POST tới `/san` hay `/api/san` nhận trang 405 mặc định tiếng Anh của Flask. Slide chỉ yêu cầu trang 404.

## Đối chiếu yêu cầu slide Chương 3 (trang 73–74)

| # | Yêu cầu | Trạng thái |
|---|---|---|
| 1 | List dữ liệu ít nhất 4 phần tử, đủ trường | Đạt (5 sân, 6 trường) |
| 2 | `/`: tổng số và số đang sẵn sàng | Đạt |
| 3 | Danh sách: bảng, tên là link chi tiết, lọc bằng query string, thanh lọc theo loại | Đạt (nên thêm `.strip()`) |
| 4 | Chi tiết `<int:id>`, không có thì 404 kèm câu báo riêng | Đạt |
| 5 | API danh sách và chi tiết JSON, không có thì `{"error": ...}` mã 404 | Đạt |
| 6 | Trang 404 tùy biến có menu chung | Đạt |
| 7 | Mọi link dùng `url_for`, mọi dữ liệu escape | Đạt |
| 8 | Commit và gắn tag `v0.1` | Commit đã có; tag gắn sau khi merge vào `main` |
| - | README ghi URL/curl đã kiểm thử | Đạt |
| - | JSON hiển thị tiếng Việt (`ensure_ascii = False`) | Đạt |

## Checklist xử lý (`/hoan-thien`)

Ký hiệu: ✅ đã sửa, ⏭ để sau, ❌ không sửa.

- [x] ✅ 🟡 `app.py:61`: thêm `.strip()`; thêm dòng `/san?loai_san=%20` (và thừa dấu cách ở cuối) vào README
- [x] ✅ 🔵 Gợi ý 1, `app.py:136-138`: đổi sang `abort(404, description=...)`, kết quả `/api/san/99` không đổi
- [x] ✅ 🔵 Gợi ý 2, `app.py:144-146`: chọn cách (b) `NotFound.description`, mỗi dòng comment dưới 100 ký tự
- [x] ✅ 🔵 Gợi ý 3, `app.py:80-104`: hiện dòng "Không có sân nào thuộc loại này." khi lọc ra 0 sân; thêm dòng `/san?loai_san=xyz` vào README

Kiểm thử sau khi sửa: chạy lại toàn bộ bảng URL trong README bằng `curl.exe`, tất cả khớp kết quả mong đợi.
Chưa có pytest/Ruff nên chưa có số liệu độ bao phủ. Không review vòng 2 vì không có mục 🔴 hoặc 🟠.

### Để sau
- ⏭ Gợi ý 4, `app.py:151`: `/api` không có `/` cuối trả HTML. Quân quyết định không sửa vì rất hiếm gặp và slide không yêu cầu.
- ⏭ Gắn tag `v0.1` và ghi dòng nguồn AI vào mô tả PR, sau khi merge vào `main`.
- ⏭ Trang 405 tiếng Anh khi gửi POST: ngoài phạm vi Chương 3.
