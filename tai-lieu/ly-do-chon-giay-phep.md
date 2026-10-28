# Lý do chọn Giấy phép MIT

Bản nháp, ngày 27/10/2026. Viết theo Bài thực hành 2.3 (slide Bài 2).

## 1. Lập luận

Đồ án là web app quản lý sân bóng, làm để học và để người khác tham khảo. Mình chọn MIT vì ba lý do.

**Một, MIT là giấy phép dễ dãi.** Ai cũng được dùng, sửa, phát hành lại, kể cả trong phần mềm thương mại đóng nguồn. Nghĩa vụ duy nhất là giữ dòng bản quyền và văn bản giấy phép.

**Hai, MIT hợp với các thư viện đang dùng.** Flask, Jinja2 và các gói phụ thuộc đều là BSD-3-Clause hoặc MIT, cùng nhóm dễ dãi, nên ghép chung không xung đột.

**Ba, MIT ngắn và dễ hiểu.** Chỉ có ba đoạn, mình tự giải thích được từng câu.

**Vì sao không chọn GPL?** GPL là copyleft mạnh: ai phân phối bản sửa đổi thì phải mở toàn bộ mã nguồn theo GPL. Điều này có ích khi muốn mọi cải tiến luôn mở, nhưng với đồ án học tập thì chỉ khiến người khác ngại dùng lại.

**Vì sao không chọn AGPL?** AGPL còn chặt hơn: chỉ cần cho người dùng truy cập qua mạng là phải công bố mã nguồn. Nhiều doanh nghiệp cấm dùng phần mềm AGPL, nên code khó được dùng lại.

## 2. Giấy phép của các thành phần

| Thành phần | Giấy phép | Nhóm | Trạng thái |
|---|---|---|---|
| Python | PSF-2.0 | Dễ dãi | Đang dùng |
| Flask | BSD-3-Clause | Dễ dãi | Đang dùng |
| Jinja2 | BSD-3-Clause | Dễ dãi | Đang dùng |
| Werkzeug | BSD-3-Clause | Dễ dãi | Đang dùng |
| MarkupSafe | BSD-3-Clause | Dễ dãi | Đang dùng |
| click | BSD-3-Clause | Dễ dãi | Đang dùng |
| itsdangerous | BSD-3-Clause | Dễ dãi | Đang dùng |
| blinker | MIT | Dễ dãi | Đang dùng |
| Bootstrap 5 | MIT | Dễ dãi | Dự kiến |
| SQLAlchemy | MIT | Dễ dãi | Dự kiến |
| SQLite | Public domain | Phạm vi công cộng | Dự kiến |
| pytest | MIT | Dễ dãi | Dự kiến |

"Đang dùng" là các gói đã có trong `requirements.txt` (cùng Python). "Dự kiến" là các thành phần sẽ thêm khi slide dạy đến.

Kết luận: không có thành phần nào thuộc nhóm copyleft, nên phát hành đồ án theo MIT không vi phạm giấy phép nào. Khi phân phối, chỉ cần giữ thông báo bản quyền và giấy phép của các thư viện (slide Bài 2, ví dụ chuỗi phụ thuộc của Flask).

## 3. Câu hỏi thầy có thể hỏi

**Chọn MIT thì người khác lấy code của em đem bán được không?**
Được. MIT cho phép dùng thương mại, chỉ yêu cầu giữ dòng bản quyền và văn bản giấy phép. Em chấp nhận điều này vì mục tiêu là để code được dùng lại càng nhiều càng tốt.

**Làm sao em biết các thư viện không có gói nào là GPL?**
Em xem thông tin giấy phép của từng gói trong `.venv`, ví dụ `.\.venv\Scripts\python.exe -m pip show flask`. Cả 7 gói đều là BSD-3-Clause hoặc MIT. Slide có giới thiệu công cụ `pip-licenses` để liệt kê tự động; em sẽ xin phép thêm khi cần.

**Vì sao không chọn Apache-2.0, cũng là giấy phép dễ dãi?**
Apache-2.0 có thêm điều khoản sáng chế, bắt buộc ghi rõ thay đổi và giữ file NOTICE. Những điều này hữu ích cho dự án lớn có doanh nghiệp tham gia. Đồ án của em nhỏ, không liên quan sáng chế, nên MIT ngắn gọn là đủ.

**Em có được sửa vài chữ trong file LICENSE cho phù hợp không?**
Không. Sửa nội dung giấy phép chuẩn sẽ tạo ra một giấy phép mới, không được OSI công nhận và không tương thích với giấy phép khác. Chỉ được điền năm và tên chủ sở hữu vào dòng bản quyền.
