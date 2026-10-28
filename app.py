# SPDX-FileCopyrightText: 2026 Nguyễn Văn Quân
# SPDX-License-Identifier: MIT
"""Ứng dụng quản lý sân bóng, phiên bản v0.2 (Chương 4: template Jinja2, Bootstrap 5)."""

from datetime import date

from flask import Flask, abort, render_template, request
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


def chuyen_san_sang_json(san):
    """Trả về bản sao của sân, trong đó ngay_tao đổi thành chuỗi "YYYY-MM-DD" cho API."""
    # Flask tự đổi date thành chuỗi kiểu "Tue, 01 Sep 2026 00:00:00 GMT", khó đọc và có giờ thừa.
    # dict(san, ...) tạo dict mới nên sân gốc trong DANH_SACH_SAN vẫn giữ kiểu date.
    return dict(san, ngay_tao=san["ngay_tao"].isoformat())


@app.template_filter("vnd")
def dinh_dang_vnd(so_tien):
    """Đổi 300000 thành "300.000 đ". Chưa có giá (None) thì trả chuỗi rỗng."""
    if so_tien is None:
        return ""
    return f"{so_tien:,.0f}".replace(",", ".") + " đ"


@app.template_filter("ngay")
def dinh_dang_ngay(gia_tri, mau="%d/%m/%Y"):
    """Đổi date(2026, 9, 1) thành "01/09/2026". Chưa có ngày (None) thì trả chuỗi rỗng."""
    if gia_tri is None:
        return ""
    return gia_tri.strftime(mau)


def lay_cac_loai_san():
    """Lấy các loại sân không trùng nhau, giữ thứ tự xuất hiện trong dữ liệu."""
    cac_loai_san = []
    for san in DANH_SACH_SAN:
        if san["loai_san"] not in cac_loai_san:
            cac_loai_san.append(san["loai_san"])
    return cac_loai_san


@app.context_processor
def them_bien_chung():
    """Các biến trả về ở đây dùng được trong mọi template, khỏi truyền lại ở từng view."""
    # Chạy ở mọi lần dựng trang; với list 5 sân thì nhẹ. Khi có CSDL (Chương 6) cần xem lại.
    return {
        "ten_he_thong": "Quản lý sân bóng",
        "nam_hien_tai": date.today().year,
        "cac_loai_san": lay_cac_loai_san(),
    }


@app.get("/")
def trang_chu():
    so_san_hoat_dong = 0
    for san in DANH_SACH_SAN:
        if san["trang_thai"] == "ACTIVE":
            so_san_hoat_dong += 1
    # Sắp xếp theo ngay_tao, mới nhất lên đầu, rồi lấy 3 sân đầu tiên.
    ba_san_moi = sorted(DANH_SACH_SAN, key=lambda san: san["ngay_tao"], reverse=True)[:3]
    return render_template(
        "trang_chu.html",
        tong_so_san=len(DANH_SACH_SAN),
        so_san_hoat_dong=so_san_hoat_dong,
        ba_san_moi=ba_san_moi,
    )


@app.get("/san")
def danh_sach_san():
    # strip() bỏ dấu cách thừa ở hai đầu, để "?loai_san= " được coi như không chọn loại.
    loai_dang_chon = request.args.get("loai_san", "").strip()

    # Không chọn loại thì hiện tất cả; có chọn thì chỉ giữ các sân đúng loại.
    if loai_dang_chon:
        cac_san = [san for san in DANH_SACH_SAN if san["loai_san"] == loai_dang_chon]
    else:
        cac_san = DANH_SACH_SAN

    return render_template("danh_sach_san.html", cac_san=cac_san, loai_dang_chon=loai_dang_chon)


@app.get("/san/<int:ma_san>")
def chi_tiet_san(ma_san):
    san = tim_san(ma_san)
    if san is None:
        abort(404, description=f"Không có sân với mã = {ma_san}")
    return render_template("chi_tiet_san.html", san=san)


@app.get("/api/san")
def api_danh_sach_san():
    # Flask tự chuyển list thành JSON
    return [chuyen_san_sang_json(san) for san in DANH_SACH_SAN]


@app.get("/api/san/<int:ma_san>")
def api_chi_tiet_san(ma_san):
    san = tim_san(ma_san)
    if san is None:
        # Giống trang HTML: trang_loi_404 thấy URL bắt đầu bằng /api/ nên tự trả JSON.
        abort(404, description=f"Không có sân với mã = {ma_san}")
    return chuyen_san_sang_json(san)


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
    # Phải trả kèm mã 404, nếu không Flask trả 200 và trình duyệt tưởng trang vẫn tồn tại.
    return render_template("loi_404.html", mo_ta=mo_ta), 404
