# Quy ước nhánh Git và đặt tên

Mọi AI và Quân đều phải theo file này khi tạo nhánh, thư mục, file, hàm hay biến.
Phiên bản 1.0, ngày 27/10/2026.

## 1. Nguyên tắc chung

1. **Tên viết bằng tiếng Việt KHÔNG DẤU, chữ thường.** Ví dụ: `dat_san.py`, `tinh-nang/c03-flask-can-ban`.
   Lý do bỏ dấu: chữ có dấu dễ gây lỗi trên Windows, trong URL, trong Git và trên máy chủ Linux khi chạy CI hoặc deploy.
2. **Chọn dấu nối theo một quy tắc duy nhất:**
   - Thứ gì Python cần `import` (file `.py`, thư mục chứa code) thì dùng **gạch dưới `_`**, vì Python không chấp nhận tên module có dấu `-`.
   - Mọi thứ còn lại (nhánh Git, URL, tài liệu `.md`, thư mục không chứa code) thì dùng **gạch ngang `-`**.
   - Riêng template `.html` dùng gạch dưới cho đồng bộ với tên hàm Python.
3. Không dùng khoảng trắng, không viết hoa (trừ các tên cố định ở mục 2), không viết tắt khó hiểu.
4. Tên phải tự giải thích. Đọc tên `tinh_tien_coc()` là biết hàm làm gì; tên như `xu_ly()` hay `ham1()` thì không được.

## 2. Những tên PHẢI giữ nguyên tiếng Anh (vì công cụ quy định)

| Tên | Lý do không đổi |
|---|---|
| `README.md`, `LICENSE`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md` | GitHub tự nhận diện các file này; thầy cũng yêu cầu đúng tên |
| `.gitignore`, `.env`, `.env.example` | Git và thư viện đọc biến môi trường tìm đúng các tên này |
| `requirements.txt`, `pyproject.toml` | pip và các công cụ Python tìm đúng tên |
| `app.py` | `flask run` tự tìm file này (slide Chương 3: "có thể bỏ --app nếu file tên app.py") |
| `templates/`, `static/` | Flask mặc định tìm template và file tĩnh ở đây |
| `__init__.py` | Python quy định |
| `tests/`, file `test_*.py`, hàm `test_*` | pytest chỉ tự tìm test theo mẫu này. Phần sau `test_` thì viết tiếng Việt, ví dụ `test_tinh_tien_coc.py` |
| `migrations/` | Alembic/Flask-Migrate tạo ra |
| `.github/workflows/`, `Dockerfile` | GitHub Actions và Docker quy định |
| `CLAUDE.md`, `.claude/` | Claude Code quy định |
| `.venv/` | Tên môi trường ảo theo slide Chương 3 |
| Từ khóa và API của thư viện (`Flask`, `render_template`, `db.Model`…) | Là code của thư viện, không đổi được |
| Tiền tố commit `feat:`, `fix:`, `docs:`… | Chuẩn Conventional Commits, thầy dùng trong slide. Phần mô tả sau tiền tố viết tiếng Việt |

## 3. Nhánh Git

### 3.1. Các loại nhánh

| Nhánh | Dùng khi | Ví dụ |
|---|---|---|
| `main` | Nhánh chính, luôn chạy được. **Không code trực tiếp trên main**; chỉ nhận thay đổi qua Pull Request | `main` |
| `cau-hinh/...` | Khởi tạo, cấu hình, môi trường, CI, Docker | `cau-hinh/khoi-tao-kho-ma` |
| `tinh-nang/cXX-...` | Làm phần đồ án của chương XX theo slide | `tinh-nang/c03-flask-can-ban` |
| `sua-loi/...` | Sửa lỗi phát hiện SAU KHI đã gộp vào main | `sua-loi/tinh-sai-tien-coc` |
| `tai-lieu/...` | Chỉ sửa tài liệu (README, hướng dẫn) | `tai-lieu/huong-dan-cai-dat` |
| `kiem-thu/...` | Chỉ bổ sung test | `kiem-thu/them-test-huy-don` |

Mẫu tên: `<loai>/<cXX->mo-ta-ngan`. Tối đa khoảng 40 ký tự, chữ thường, không dấu, nối bằng gạch ngang.
`cXX` là số chương của slide (c03, c04…), dùng cho nhánh `tinh-nang/` để biết nhánh thuộc buổi nào.

### 3.2. Lộ trình nhánh và phiên bản (giống cách thầy làm với LibraryMS)

| Slide | Nhánh | Tag khi gộp | Nội dung chính |
|---|---|---|---|
| Bài 1–2 | `cau-hinh/khoi-tao-kho-ma` | (không gắn) | README, LICENSE MIT kèm lập luận, `.gitignore`, `.venv`, `requirements.txt` |
| Chương 3 | `tinh-nang/c03-flask-can-ban` | `v0.1` | Route xem sân, dữ liệu tạm trong list, API JSON, trang 404 |
| Chương 4 | `tinh-nang/c04-giao-dien-jinja2` | `v0.2` | Template, Bootstrap, macro, filter `vnd`, context processor |
| Chương 5 trở đi | `tinh-nang/c05-...` | `v0.3`, … | Đặt tên khi có slide |

Chỉ đặt tên tag là `v0.1`, `v0.2`… **Không đặt tên nhánh trùng tên tag**, vì Git sẽ báo "ambiguous" (mơ hồ).

### 3.3. Quy trình cho mỗi chương

Các lệnh dưới đây chạy trong PowerShell (terminal của VS Code):

```powershell
git switch main                                 # về nhánh chính
git pull                                        # lấy bản mới nhất (khi đã có GitHub)
git switch -c tinh-nang/c03-flask-can-ban       # tạo nhánh mới và chuyển sang
# ... /lam-theo-slide → kiểm tra → commit từng phần nhỏ ...
# ... @agent-reviewer → /hoan-thien → commit sửa lỗi ...
git push -u origin tinh-nang/c03-flask-can-ban  # đẩy nhánh lên GitHub
# Trên GitHub: tạo Pull Request vào main → dán báo cáo review làm comment → Merge
git switch main
git pull
git tag v0.1
git push --tags
```

### 3.4. Commit

- Mỗi commit là một thay đổi nhỏ và chạy được. Commit message theo dạng `<tien-to>: <mô tả tiếng Việt>`.
- Các tiền tố dùng: `feat` (tính năng), `fix` (sửa lỗi), `docs` (tài liệu), `test` (kiểm thử), `refactor` (sửa cấu trúc, không đổi chức năng), `chore` (cấu hình, phụ thuộc), `style` (định dạng code).
- Ví dụ:
  - `feat(san): trang danh sách sân có lọc theo loại sân`
  - `fix(dat-san): chặn đặt khung giờ đã bắt đầu`
  - `chore: tạo môi trường ảo và requirements.txt`

## 4. Đặt tên trong code

| Thành phần | Kiểu chữ | Ví dụ |
|---|---|---|
| File và thư mục Python | `snake_case` | `du_lieu_mau.py`, `nghiep_vu/` |
| Hàm, biến | `snake_case` | `tinh_tien_coc()`, `ma_san`, `danh_sach_san` |
| Hằng số | `CHU_HOA` | `THOI_GIAN_GIU_CHO_PHUT = 10`, `TY_LE_COC = 0.3` |
| Lớp (class) | `PascalCase` | `San`, `DonDatSan`, `NguoiDung` |
| Endpoint (tên hàm view) | `snake_case` | `chi_tiet_san` → `url_for("chi_tiet_san", ma_san=1)` |
| URL | `kebab-case` | `/san`, `/san/<int:ma_san>`, `/san/<int:ma_san>/lich-trong`, `/api/san` |
| Template | `snake_case.html`; file dùng chung có tiền tố `_` | `trang_khung.html`, `_thanh_menu.html`, `_macro.html`, `danh_sach_san.html`, `loi_404.html` |
| Bảng CSDL | `snake_case` số ít | `nguoi_dung`, `san`, `bang_gia`, `don_dat_san`, `khung_gio_dat`, `thanh_toan` |
| Cột CSDL | `snake_case` | `ma_san`, `ten_san`, `loai_san`, `trang_thai`, `thoi_diem_tao` |
| Cột ngày, giờ | Cột kiểu `date` đặt `ngay_...`; cột kiểu `datetime` đặt `thoi_diem_...` | `ngay_tao`, `thoi_diem_tao` |
| Giá trị trạng thái | `CHU_HOA` (giữ như trong SRS) | `HOLDING`, `CONFIRMED`, `CANCELLED`, `ACTIVE` |

Giá trị trạng thái giữ nguyên chữ hoa tiếng Anh như SRS HUSC-18, để đối chiếu với tài liệu được dễ.

## 5. Cấu trúc thư mục

### 5.1. Giai đoạn v0.1–v0.2 (Chương 3–4: một file `app.py`, giống LibraryMS)

```
quan-ly-san-bong/                  ← tên repo trên GitHub
├── .claude/                       ← cấu hình các AI (giữ tên)
├── .venv/                         ← môi trường ảo (KHÔNG commit)
├── slide-cua-thay/                ← slide thầy (KHÔNG commit, có trong .gitignore)
├── tai-lieu/
│   ├── ke-hoach-do-an.md
│   ├── quy-uoc-nhanh-va-dat-ten.md
│   ├── y-tuong-cua-quan.md
│   ├── ly-do-chon-giay-phep.md
│   └── review/                    ← báo cáo của AI review, mỗi lần một file
├── static/
│   ├── css/giao_dien.css
│   └── hinh_anh/logo.svg
├── templates/                     ← có từ Chương 4
│   ├── trang_khung.html           ← khung chung (base)
│   ├── _thanh_menu.html
│   ├── _macro.html
│   ├── trang_chu.html
│   ├── danh_sach_san.html
│   ├── chi_tiet_san.html
│   └── loi_404.html
├── app.py                         ← route, view
├── du_lieu_mau.py                 ← danh sách sân tạm trong list (bỏ khi có CSDL)
├── .gitignore
├── CLAUDE.md
├── LICENSE
├── README.md
└── requirements.txt
```

### 5.2. Giai đoạn sau (CHỈ tạo khi slide yêu cầu; dự kiến, có thể đổi theo slide)

```
quan-ly-san-bong/
├── ung_dung/                      ← gói ứng dụng (khi slide dạy blueprint hoặc application factory)
│   ├── __init__.py
│   ├── mo_hinh/                   ← model CSDL: nguoi_dung.py, san.py, don_dat_san.py...
│   ├── nghiep_vu/                 ← logic thuần, dễ test: tinh_tien.py, kiem_tra_lich.py, dat_san.py
│   ├── tuyen/                     ← route/blueprint: tai_khoan.py, san.py, dat_san.py, nhan_vien.py, quan_tri.py, api.py
│   ├── templates/
│   └── static/
├── migrations/
├── tests/
│   ├── test_tinh_tien_coc.py
│   └── test_dat_san.py
├── .github/workflows/
└── ...
```

## 6. Ghi bản quyền và giấy phép (theo slide Bài 2)

Đầu mỗi file `.py` có hai dòng SPDX:

```python
# SPDX-FileCopyrightText: 2026 Nguyễn Văn Quân
# SPDX-License-Identifier: MIT
```
