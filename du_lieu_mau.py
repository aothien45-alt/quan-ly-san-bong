# SPDX-FileCopyrightText: 2026 Nguyễn Văn Quân
# SPDX-License-Identifier: MIT
"""Dữ liệu sân lưu tạm trong list. Chương 6 sẽ thay bằng cơ sở dữ liệu."""

from datetime import date

# Mỗi sân là một dict. Tiền là số nguyên, đơn vị VND.
# trang_thai lấy theo SRS: ACTIVE = đang khai thác, INACTIVE = ngừng khai thác.
# ngay_tao ứng với cột created_at của bảng fields trong DB Design; chỉ cần ngày nên dùng date.
DANH_SACH_SAN = [
    {
        "ma_san": 1,
        "ten_san": "Sân A1",
        "loai_san": "Sân 5 người",
        "dia_chi": "12 Nguyễn Huệ, TP Huế",
        "gia_thue_mot_gio": 300000,
        "trang_thai": "ACTIVE",
        "ngay_tao": date(2025, 12, 1),
    },
    {
        "ma_san": 2,
        "ten_san": "Sân A2",
        "loai_san": "Sân 5 người",
        "dia_chi": "12 Nguyễn Huệ, TP Huế",
        "gia_thue_mot_gio": 300000,
        "trang_thai": "INACTIVE",
        "ngay_tao": date(2026, 1, 15),
    },
    {
        "ma_san": 3,
        "ten_san": "Sân B1",
        "loai_san": "Sân 7 người",
        "dia_chi": "45 Lê Lợi, TP Huế",
        "gia_thue_mot_gio": 500000,
        "trang_thai": "ACTIVE",
        "ngay_tao": date(2026, 4, 20),
    },
    {
        "ma_san": 4,
        "ten_san": "Sân B2",
        "loai_san": "Sân 7 người",
        "dia_chi": "45 Lê Lợi, TP Huế",
        "gia_thue_mot_gio": 500000,
        "trang_thai": "ACTIVE",
        "ngay_tao": date(2026, 7, 5),
    },
    {
        "ma_san": 5,
        "ten_san": "Sân C1",
        "loai_san": "Sân 11 người",
        "dia_chi": "8 Hùng Vương, TP Huế",
        "gia_thue_mot_gio": 1200000,
        "trang_thai": "ACTIVE",
        "ngay_tao": date(2026, 9, 1),
    },
]
