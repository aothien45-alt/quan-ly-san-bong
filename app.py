# SPDX-FileCopyrightText: 2026 Nguyễn Văn Quân
# SPDX-License-Identifier: MIT
"""Ứng dụng quản lý sân bóng, phiên bản v0.1 (Chương 3: Flask căn bản)."""

from flask import Flask, url_for
from markupsafe import escape

from du_lieu_mau import DANH_SACH_SAN

app = Flask(__name__)
app.json.ensure_ascii = False  # JSON hiển thị tiếng Việt có dấu thay vì \uXXXX


def tim_san(ma_san):
    """Trả về sân có mã tương ứng, hoặc None nếu không có."""
    for san in DANH_SACH_SAN:
        if san["ma_san"] == ma_san:
            return san
    return None


def dinh_dang_tien(so_tien):
    """Đổi 300000 thành "300.000 đ" cho dễ đọc. Chương 4 sẽ chuyển thành filter vnd."""
    return f"{so_tien:,}".replace(",", ".") + " đ"


def dung_khung_trang(tieu_de, noi_dung):
    """Ghép phần đầu trang và menu dùng chung. Chương 4 sẽ thay bằng template Jinja2."""
    return f"""<!doctype html>
<html lang="vi">
<head><meta charset="utf-8">
<title>{escape(tieu_de)} - Quản lý sân bóng</title></head>
<body>
  <nav>
    <a href="{url_for('trang_chu')}">Trang chủ</a>
  </nav>
  <hr>
  {noi_dung}
</body>
</html>"""


@app.get("/")
def trang_chu():
    so_san_hoat_dong = 0
    for san in DANH_SACH_SAN:
        if san["trang_thai"] == "ACTIVE":
            so_san_hoat_dong += 1
    noi_dung = (
        "<h1>Quản lý sân bóng</h1>"
        f"<p>Tổng số sân: {len(DANH_SACH_SAN)}</p>"
        f"<p>Số sân đang hoạt động: {so_san_hoat_dong}</p>"
    )
    return dung_khung_trang("Trang chủ", noi_dung)
