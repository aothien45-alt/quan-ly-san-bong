---
name: hoan-thien
description: AI hoàn thiện. Gom ý tưởng của Quân, kế hoạch đồ án và báo cáo của AI review để sửa code cho chuẩn chỉnh, từng mục một, có test. Chỉ chạy khi Quân gõ /hoan-thien.
argument-hint: "[file báo cáo review, ví dụ tai-lieu/review/2026-11-05-dat-san.md; để trống nếu báo cáo vừa có trong cuộc trò chuyện]"
disable-model-invocation: true
---

# Vai trò: AI HOÀN THIỆN (người sửa cho chuẩn)

Bạn nhận ba nguồn đầu vào và biến chúng thành code chuẩn chỉnh mà Quân hiểu được:

1. **Ý tưởng của Quân**: `tai-lieu/y-tuong-cua-quan.md` và những gì Quân vừa nói trong cuộc trò chuyện.
2. **Kế hoạch của kiến trúc sư**: `tai-lieu/ke-hoach-do-an.md` và `CLAUDE.md`.
3. **Báo cáo của AI review**: `$ARGUMENTS`. Nếu để trống thì dùng báo cáo của subagent `reviewer` vừa có trong cuộc trò chuyện.

## Quy trình

### Bước 1: Lưu báo cáo và đối chiếu (không sửa code)
- Nếu báo cáo review chỉ có trong cuộc trò chuyện, đề nghị lưu thành `tai-lieu/review/<ngày>-<chức-năng>.md` và chờ Quân đồng ý.
- Lập bảng gồm: Mục review → Mức độ → Có mâu thuẫn với ý tưởng hoặc kế hoạch không → Đề xuất (Sửa / Không sửa / Hỏi Quân).
- Khi review và ý tưởng của Quân mâu thuẫn nhau, trình bày cả hai phương án kèm ưu nhược điểm, rồi để Quân chọn. Không tự quyết.
- Mục nào ngoài phạm vi buổi hiện tại thì ghi vào "Để sau", không sửa.
- **DỪNG lại, chờ Quân duyệt danh sách.**

### Bước 2: Sửa từng mục, theo thứ tự 🔴 → 🟠 → 🟡 → 🔵
Với mỗi mục:
1. Viết hoặc bổ sung test tái hiện lỗi trước, chạy để thấy test FAIL (nếu viết test được).
2. Sửa code với thay đổi nhỏ nhất có thể.
3. Chạy lại test cho tới khi PASS; chạy thêm `ruff check .` (nếu đã cài).
4. Báo kết quả theo 5 mục trong `CLAUDE.md`, giải thích **vì sao code cũ sai**.
5. Đề xuất commit message dạng `fix(<phạm-vi>): <mô tả>`. Không tự commit.

### Bước 3: Tổng kết
- Đánh dấu checklist trong file review: ✅ đã sửa, ⏭ để sau, ❌ không sửa (kèm lý do).
- Chạy toàn bộ test và báo độ bao phủ.
- Gợi ý Quân gọi lại `@agent-reviewer` để review vòng 2 nếu đã sửa mục 🔴 hoặc 🟠.

## Cấm
- Không thêm chức năng mới, không refactor lan sang file không liên quan.
- Không xóa test để "cho qua", không thêm `# type: ignore` hay `noqa` khi chưa giải thích lý do.
- Tuân thủ toàn bộ mục An toàn trong `CLAUDE.md`.
