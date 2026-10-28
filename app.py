# SPDX-FileCopyrightText: 2026 Nguyễn Văn Quân
# SPDX-License-Identifier: MIT
"""Ứng dụng quản lý sân bóng, phiên bản v0.1 (Chương 3: Flask căn bản)."""

from flask import Flask, abort, request, url_for
from markupsafe import escape
from werkzeug.exceptions import NotFound

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
    <a href="{url_for('danh_sach_san')}">Danh sách sân</a> |
    <a href="{url_for('api_danh_sach_san')}">API sân</a>
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
    # strip() bỏ dấu cách thừa ở hai đầu, để "?loai_san= " được coi như không chọn loại.
    loai_dang_chon = request.args.get("loai_san", "").strip()

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
        link_chi_tiet = url_for("chi_tiet_san", ma_san=san["ma_san"])
        cac_dong += (
            f"<tr><td><a href=\"{link_chi_tiet}\">{escape(san['ten_san'])}</a></td>"
            f"<td>{escape(san['loai_san'])}</td>"
            f"<td>{escape(san['dia_chi'])}</td>"
            f"<td>{dinh_dang_tien(san['gia_thue_mot_gio'])}</td>"
            f"<td>{escape(san['trang_thai'])}</td></tr>"
        )

    # Bảng không có dòng nào thì người dùng tưởng trang bị lỗi, nên báo rõ là không có sân.
    if not cac_dong:
        cac_dong = "<tr><td colspan='5'>Không có sân nào thuộc loại này.</td></tr>"

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


@app.get("/san/<int:ma_san>")
def chi_tiet_san(ma_san):
    san = tim_san(ma_san)
    if san is None:
        abort(404, description=f"Không có sân với mã = {ma_san}")
    noi_dung = (
        f"<h1>{escape(san['ten_san'])}</h1>"
        "<ul>"
        f"<li>Mã sân: {san['ma_san']}</li>"
        f"<li>Loại sân: {escape(san['loai_san'])}</li>"
        f"<li>Địa chỉ: {escape(san['dia_chi'])}</li>"
        f"<li>Giá thuê một giờ: {dinh_dang_tien(san['gia_thue_mot_gio'])}</li>"
        f"<li>Trạng thái: {escape(san['trang_thai'])}</li>"
        "</ul>"
        f"<p><a href=\"{url_for('danh_sach_san')}\">Quay lại danh sách sân</a></p>"
    )
    return dung_khung_trang(san["ten_san"], noi_dung)


@app.get("/api/san")
def api_danh_sach_san():
    return DANH_SACH_SAN  # Flask tự chuyển list thành JSON


@app.get("/api/san/<int:ma_san>")
def api_chi_tiet_san(ma_san):
    san = tim_san(ma_san)
    if san is None:
        # Giống trang HTML: trang_loi_404 thấy URL bắt đầu bằng /api/ nên tự trả JSON.
        abort(404, description=f"Không có sân với mã = {ma_san}")
    return san


@app.errorhandler(404)
def trang_loi_404(loi):
    # NotFound.description là câu báo 404 mặc định bằng tiếng Anh của Flask.
    # Trùng câu đó nghĩa là không có abort(404, description=...) riêng, nên dùng câu tiếng Việt.
    if loi.description == NotFound.description:
        mo_ta = "Trang bạn tìm không tồn tại."
    else:
        mo_ta = loi.description
    # URL của API (ví dụ /api/san/abc) thì trả JSON để chương trình gọi API đọc được.
    if request.path.startswith("/api/"):
        return {"error": mo_ta}, 404
    noi_dung = (
        "<h1>404 - Không tìm thấy trang</h1>"
        f"<p>{escape(mo_ta)}</p>"
        f"<p><a href=\"{url_for('trang_chu')}\">Về trang chủ</a></p>"
    )
    # Phải trả kèm mã 404, nếu không Flask trả 200 và trình duyệt tưởng trang vẫn tồn tại.
    return dung_khung_trang("Không tìm thấy", noi_dung), 404
