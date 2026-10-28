# Báo cáo review: nhánh `tinh-nang/c04-giao-dien-jinja2` so với `main`

## Tóm tắt

Có 0 lỗi nghiêm trọng, 0 lỗi cao, 1 lỗi trung bình và 4 gợi ý.

**Kết luận: Có thể commit, nhánh sẵn sàng tạo PR.** Cả 7 yêu cầu chấm điểm của "Bài tập dự án LibraryMS v0.2" trong slide (trang 59) đều đã làm đủ. Lỗi trung bình chỉ cần sửa 1–2 dòng, nên sửa trước khi merge. Các gợi ý thì không bắt buộc.

**Những gì tôi đã kiểm tra:**
- **Đọc diff:** 8 commit, 15 file.
- **`flask routes`:** đủ 6 route.
- **Kiểm thử HTTP bằng `curl.exe`:** chạy server ở cổng 8765 rồi đã tắt. Kết quả:
  - `/`, `/san`, `/san?loai_san=...` (đúng loại, dấu cách, `xyz`, `<b>x</b>`), `/san/2`, `/san/3` trả 200.
  - `/san/99`, `/san/abc`, `/san/-1`, `/abc`, `/static/khong-co.css` trả 404.
  - `/api/san` và `/api/san/3` trả 200 kiểu JSON, có `"ngay_tao":"2026-04-20"`. `/api/san/99`, `/api/san/abc`, `/api/khong-co` trả 404 kiểu JSON. `POST /api/san` trả 405.
  - `<b>x</b>` hiện thành `&lt;b&gt;x&lt;/b&gt;`.
  - Thứ tự 3 sân mới là C1, B2, B1. Giá hiện "500.000 đ", ngày "20/04/2026", A2 có nhãn xám.
  - Menu "Sân" vẫn được đánh dấu khi đang ở trang chi tiết.
- **Chạy được từng commit:** tôi xuất cả 8 commit bằng `git archive` ra thư mục tạm rồi chạy thử. Commit nào cũng chạy đúng, đáp ứng mục 3.4 "mỗi commit chạy được".
- **Cấu hình:** `autoescape` đang bật cho `.html` và `app.debug = False`.
- **Không có trong code:** không có `|safe`, `Markup` hay `escape()` nào trong code. Mọi URL nội bộ đều sinh bằng `url_for`, chỉ còn 2 link CDN của Bootstrap là viết thẳng, đúng như slide.
- **Git:** `.env` và `slide-cua-thay/` đều nằm trong `.gitignore` và không bị commit. `app.py` và `du_lieu_mau.py` có SPDX. Commit message đúng mục 3.4.
- **Chưa kiểm tra được:** Ruff, pytest và mypy chưa có trong `.venv`. Đây cũng là các công cụ slide chưa dạy đến nên không tính là lỗi.

---

### [TRUNG BÌNH] Filter `vnd` hiển thị sai với số thực và lỗi 500 với None: `e:\DoAn\quan-ly-san-bong\app.py:34`
- **Vấn đề:** `f"{so_tien:,}"` chỉ cho kết quả đúng với số nguyên. Gặp số thực thì phần thập phân vẫn còn, rồi `.replace(",", ".")` biến nó thành một dấu chấm hàng nghìn giả. Gặp `None` thì Python báo `TypeError` và trang sập với mã 500. Tôi đã chạy thử filter:
  - `300000.0` thành `"300.000.0 đ"`
  - `1500.5` thành `"1.500.5 đ"`, người xem dễ đọc thành 1,5 triệu
  - `None` gây `TypeError: unsupported format string passed to NoneType.__format__`
- **Tình huống gây lỗi:** dữ liệu mẫu hiện tại toàn số nguyên nên chưa lỗi. Nhưng đến lúc tính tiền cọc, nếu viết `gia * 0.3` mà quên làm tròn thì kết quả là `float`, và trang sẽ hiện số tiền sai mà không báo gì. Còn khi có CSDL, một cột giá để trống (`None`) sẽ làm sập cả trang danh sách.
- **Cách sửa:**
  1. Làm theo gợi ý của slide Bài 5 (trang 18): dùng `:,.0f` để số thực cũng có dạng đúng.
  2. Trả chuỗi rỗng khi gặp `None`, giống cách filter `ngay` đang làm.
  3. Nhớ quy tắc nghiệp vụ số 7: tiền phải là số nguyên. Việc làm tròn (ví dụ `math.ceil` cho tiền cọc) phải xong trong Python trước khi đưa vào template. Filter chỉ lo phần hiển thị.
  ```python
  @app.template_filter("vnd")
  def dinh_dang_vnd(so_tien):
      """Đổi 300000 thành "300.000 đ". Chưa có giá (None) thì trả chuỗi rỗng."""
      if so_tien is None:
          return ""
      return f"{so_tien:,.0f}".replace(",", ".") + " đ"
  ```
- **Test nên thêm (khi slide dạy pytest):**
  - `test_dinh_dang_vnd_so_nguyen`: 0 thành "0 đ", 1000 thành "1.000 đ", 1500000 thành "1.500.000 đ".
  - `test_dinh_dang_vnd_so_thuc`: 300000.0 thành "300.000 đ".
  - `test_dinh_dang_vnd_none`: None thành "".
- **Câu hỏi tự kiểm tra cho Quân:** Vì sao `f"{1500.5:,}".replace(",", ".")` lại cho ra chuỗi có hai dấu chấm?

### [GỢI Ý] Tên `ngay_tao` khác quy ước `thoi_diem_tao`, cần tính trước múi giờ cho Chương 6: `e:\DoAn\quan-ly-san-bong\du_lieu_mau.py:9`
- **Vấn đề:** bảng ở mục 4 của file quy ước lấy `thoi_diem_tao` làm ví dụ tên cột. Nhánh này dùng `ngay_tao` kiểu `date`, và kế hoạch dòng 117 đã ghi theo tên này. Với `date` (chỉ có ngày) thì tên `ngay_tao` hợp lý. Tuy nhiên `created_at` trong DB Design là thời điểm (`datetime`) lưu theo UTC.
- **Tình huống gây lỗi (khi sang Chương 6):** nếu đổi sang `datetime` UTC mà filter `ngay` vẫn gọi thẳng `strftime`, một sân thêm lúc 05:00 ngày 01/09 giờ Việt Nam (tức 22:00 ngày 31/08 UTC) sẽ hiện là "31/08/2026", trái quy tắc nghiệp vụ số 7.
- **Cách sửa:** hiện tại chưa cần sửa code. Nên thống nhất ngay một tên giữa file quy ước và kế hoạch, và ghi chú lại: khi sang `datetime` UTC, filter phải đổi về `Asia/Ho_Chi_Minh` trước khi định dạng.
- **Câu hỏi tự kiểm tra cho Quân:** Lưu UTC nhưng hiển thị ngày theo giờ Việt Nam thì ngày hiển thị có thể lệch so với ngày lưu trong khoảng giờ nào?

### [GỢI Ý] Năm ở chân trang lấy theo giờ máy chủ: `e:\DoAn\quan-ly-san-bong\app.py:60`
- **Vấn đề:** `date.today()` lấy theo múi giờ của máy chạy server. Máy của Quân dùng giờ Việt Nam nên hiện đúng. Nếu deploy lên máy chủ chạy UTC thì từ 00:00 đến 06:59 ngày 01/01 (giờ Việt Nam), chân trang vẫn hiện năm cũ.
- **Cách sửa:** chưa cần sửa ngay vì slide cũng viết như vậy. Đến buổi deploy thì đổi sang `datetime.now(ZoneInfo("Asia/Ho_Chi_Minh")).year` (`zoneinfo` có sẵn trong Python, trên Windows có thể cần thêm gói `tzdata`).
- **Câu hỏi tự kiểm tra cho Quân:** `date.today()` dựa vào cái gì để biết hôm nay là ngày nào?

### [GỢI Ý] Link CDN của Bootstrap chưa có `integrity`: `e:\DoAn\quan-ly-san-bong\templates\trang_khung.html:9` và `:23`
- **Vấn đề:** nếu CDN bị chèn mã độc, trình duyệt vẫn chạy file JS đó. Thuộc tính `integrity="sha384-..."` kèm `crossorigin="anonymous"` (trang chủ Bootstrap cung cấp sẵn) buộc trình duyệt kiểm tra file trước khi chạy. Slide không yêu cầu nên đây chỉ là gợi ý.
- **Câu hỏi tự kiểm tra cho Quân:** Vì sao file JS tải từ máy chủ của người khác lại là một rủi ro bảo mật?

### [GỢI Ý] Một số dòng code dài hơn 88 ký tự: `e:\DoAn\quan-ly-san-bong\app.py:72` (89 ký tự), `:92` (96 ký tự)
- **Vấn đề:** Ruff chưa cài nên tôi chưa kiểm tra được. Khi slide dạy Ruff, `ruff format` sẽ tự xuống dòng ở hai dòng code này. Các dòng comment hay docstring dài (`:26`, `:57`, `:121`...) thì phải tự ngắt tay. Hiện tại không cần làm gì, chỉ ghi nhận trước.

---

## Thiếu so với slide Chương 4

**Bài tập dự án (trang 59): đã làm đủ 7/7 yêu cầu.**
1. Đã có khung chung, menu đánh dấu cả trang chi tiết, chân trang, Bootstrap và CSS riêng.
2. Đã có hai macro `the_san` và `nhan_trang_thai`, mỗi macro được dùng ở ít nhất 2 trang.
3. Trang chủ có tổng số sân, số sân đang hoạt động và 3 sân mới dạng card.
4. Lưới 1/2/3 cột, thanh lọc dạng nút có tô đậm, danh sách loại sân lấy qua context processor.
5. Trang chi tiết dạng bảng, loại sân là liên kết sang danh sách đã lọc.
6. Trang 404 dùng template và hiển thị `description`.
7. API vẫn chạy, `app.py` không còn HTML và không còn `escape()`.

README đã có bảng URL đã kiểm thử và 2 ảnh chụp (máy tính, điện thoại). Tôi đã xem hai ảnh, đúng giao diện v0.2.

**Còn lại:**
- Bước 8 "Commit, tag v0.2": gắn tag sau khi merge vào `main`, theo mục 3.3 của file quy ước.

**Có trong slide nhưng dự án không bắt buộc (chỉ cần hiểu để trả lời câu hỏi ôn tập):**
- `{{ super() }}`: `block head` đã khai báo nhưng chưa trang nào dùng (Bài 7, câu ôn tập 10).
- Sinh menu bằng vòng lặp `for` (Lab bước 4, Bài 12): menu hiện viết tay 2 mục. Với 2 mục thì chấp nhận được.
- `loop.index`, các phép kiểm tra `is none` / `is defined`, filter `default(..., true)` (Bài 3, 5).

## Điểm làm tốt
- Chia commit nhỏ, đúng thứ tự, commit nào cũng chạy được, message đúng quy ước.
- Bám rất sát slide: `chuyen_san_sang_json` dùng `dict(san, ...)` như Lab bước 8, filter `ngay` xử lý `None` đúng yêu cầu Bài 5, và comment giải thích "vì sao" rõ ràng (ví dụ comment ở `app.py:129` về mã 404).
- Phần nhập liệu được xử lý cẩn thận: `strip()` cho tham số lọc, autoescape được kiểm chứng bằng `<b>x</b>`, API và trang HTML trả lỗi 404 theo hai kiểu riêng.

## Danh sách việc cần sửa
- [ ] (Trung bình) `e:\DoAn\quan-ly-san-bong\app.py:31-34`: filter `vnd` trả `""` khi gặp `None` và dùng `:,.0f` để số thực không hiện thành `"1.500.5 đ"`. Sửa docstring cho khớp.
- [ ] (Gợi ý, không bắt buộc) Thống nhất tên `ngay_tao` / `thoi_diem_tao` giữa `e:\DoAn\quan-ly-san-bong\tai-lieu\quy-uoc-nhanh-va-dat-ten.md` (dòng 101) và `e:\DoAn\quan-ly-san-bong\tai-lieu\ke-hoach-do-an.md` (dòng 117); ghi chú việc đổi múi giờ cho Chương 6.
- [ ] (Gợi ý, không bắt buộc) Thêm `integrity` và `crossorigin` cho 2 link CDN trong `e:\DoAn\quan-ly-san-bong\templates\trang_khung.html`.
- [ ] (Sau khi merge) Gắn tag `v0.2` trên `main`. Trong mô tả PR nhớ thêm dòng ghi nguồn AI theo CLAUDE.md.

## Checklist xử lý (`/hoan-thien`)

Ký hiệu: ✅ đã sửa, ⏭ để sau, ❌ không sửa.

- [x] ✅ 🟡 `app.py:31-36`: filter `vnd` dùng `:,.0f` và trả `""` khi gặp `None`, theo đúng code mẫu ở trên (commit `945d144`). Kiểm tra trước và sau bằng `python -c`: `1500.5` từ `"1.500.5 đ"` thành `"1.500 đ"`, `None` từ `TypeError` thành `""`.
- [x] ✅ 🔵 Tên `ngay_tao` / `thoi_diem_tao`: Quân chọn giữ `ngay_tao`, không sửa code và kế hoạch. Thêm dòng "Cột ngày, giờ" vào bảng mục 4 của `tai-lieu/quy-uoc-nhanh-va-dat-ten.md`: cột kiểu `date` đặt `ngay_...`, cột kiểu `datetime` đặt `thoi_diem_...` (commit `5e5d653`).

Kiểm thử sau khi sửa: chạy server rồi gọi bằng `curl.exe` các URL `/`, `/san`, `/san?loai_san=xyz`, `/san?loai_san=<b>x</b>`, `/san/2`, `/san/3`, `/api/san`, `/api/san/3` (200) và `/san/99`, `/san/abc`, `/abc`, `/api/san/99`, `/api/khong-co` (404). Tất cả đúng mã trạng thái. Giá trên `/san` hiện `300.000 đ`, `500.000 đ`, `1.200.000 đ`; `<b>x</b>` hiện thành `&lt;b&gt;x&lt;/b&gt;`.
Chưa có pytest/Ruff nên chưa có số liệu độ bao phủ. Không review vòng 2 vì không có mục 🔴 hoặc 🟠.

### Để sau
- ⏭ 🔵 Năm ở chân trang lấy theo giờ máy chủ (`app.py:60`): sửa ở buổi deploy (buổi 13). Slide Chương 4 cũng viết như vậy.
- ⏭ 🔵 `integrity` và `crossorigin` cho 2 link CDN trong `templates/trang_khung.html`: Quân để sau vì slide không yêu cầu. Khi làm phải chép đúng mã băm từ getbootstrap.com theo đúng phiên bản.
- ⏭ 🔵 Dòng dài hơn 88 ký tự (`app.py:72`, `:92`): xử lý khi slide dạy Ruff.
- ⏭ Test pytest cho filter `vnd` (3 test nêu ở trên): viết khi slide dạy pytest.
- ⏭ Gắn tag `v0.2` và ghi dòng nguồn AI vào mô tả PR, sau khi merge vào `main`.

### Không sửa
- ❌ `{{ super() }}`, sinh menu bằng `for`, `loop.index`, `is none` / `is defined`, `default(..., true)`: slide có nhưng bài tập dự án không bắt buộc. Menu chỉ có 2 mục nên viết tay vẫn dễ đọc hơn. Chỉ cần hiểu để trả lời câu hỏi ôn tập.
