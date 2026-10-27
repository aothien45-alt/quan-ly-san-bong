# SPDX-FileCopyrightText: 2026 Nguyễn Văn Quân
# SPDX-License-Identifier: MIT
"""Ứng dụng quản lý sân bóng, phiên bản v0.1 (Chương 3: Flask căn bản)."""

from flask import Flask, request, url_for
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
    <a href="{url_for('trang_chu')}">Trang chủ</a> |
    <a href="{url_for('danh_sach_san')}">Danh sách sân</a>
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


@app.get("/san")
def danh_sach_san():
    loai_dang_chon = request.args.get("loai_san", "")

    # Lấy các loại sân không trùng nhau, giữ thứ tự xuất hiện trong dữ liệu.
    cac_loai_san = []
    for san in DANH_SACH_SAN:
        if san["loai_san"] not in cac_loai_san:
            cac_loai_san.append(san["loai_san"])

    thanh_loc = f'<a href="{url_for("danh_sach_san")}">Tất cả</a>'
    for loai_san in cac_loai_san:
        link = url_for("danh_sach_san", loai_san=loai_san)
        thanh_loc += f' | <a href="{link}">{escape(loai_san)}</a>'

    # Không chọn loại thì hiện tất cả; có chọn thì chỉ giữ các sân đúng loại.
    if loai_dang_chon:
        cac_san = [san for san in DANH_SACH_SAN if san["loai_san"] == loai_dang_chon]
    else:
        cac_san = DANH_SACH_SAN

    cac_dong = ""
    for san in cac_san:
        cac_dong += (
            f"<tr><td>{escape(san['ten_san'])}</td>"
            f"<td>{escape(san['loai_san'])}</td>"
            f"<td>{escape(san['dia_chi'])}</td>"
            f"<td>{dinh_dang_tien(san['gia_thue_mot_gio'])}</td>"
            f"<td>{escape(san['trang_thai'])}</td></tr>"
        )

    if loai_dang_chon:
        thong_bao = f"<p>Loại sân: {escape(loai_dang_chon)}, có {len(cac_san)} sân.</p>"
    else:
        thong_bao = f"<p>Tất cả: {len(cac_san)} sân.</p>"

    noi_dung = (
        "<h1>Danh sách sân</h1>"
        f"<p>Lọc theo loại: {thanh_loc}</p>"
        f"{thong_bao}"
        "<table border='1'>"
        "<tr><th>Tên sân</th><th>Loại sân</th><th>Địa chỉ</th>"
        "<th>Giá thuê một giờ</th><th>Trạng thái</th></tr>"
        f"{cac_dong}"
        "</table>"
    )
    return dung_khung_trang("Danh sách sân", noi_dung)
