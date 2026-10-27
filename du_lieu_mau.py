# SPDX-FileCopyrightText: 2026 Nguyễn Văn Quân
# SPDX-License-Identifier: MIT
"""Dữ liệu sân lưu tạm trong list. Chương 6 sẽ thay bằng cơ sở dữ liệu."""

# Mỗi sân là một dict. Tiền là số nguyên, đơn vị VND.
# trang_thai lấy theo SRS: ACTIVE = đang khai thác, INACTIVE = ngừng khai thác.
DANH_SACH_SAN = [
    {
        "ma_san": 1,
        "ten_san": "Sân A1",
        "loai_san": "Sân 5 người",
        "gia_thue_mot_gio": 300000,
        "trang_thai": "ACTIVE",
    },
    {
        "ma_san": 2,
        "ten_san": "Sân A2",
        "loai_san": "Sân 5 người",
        "gia_thue_mot_gio": 300000,
        "trang_thai": "INACTIVE",
    },
    {
        "ma_san": 3,
        "ten_san": "Sân B1",
        "loai_san": "Sân 7 người",
        "gia_thue_mot_gio": 500000,
        "trang_thai": "ACTIVE",
    },
    {
        "ma_san": 4,
        "ten_san": "Sân B2",
        "loai_san": "Sân 7 người",
        "gia_thue_mot_gio": 500000,
        "trang_thai": "ACTIVE",
    },
    {
        "ma_san": 5,
        "ten_san": "Sân C1",
        "loai_san": "Sân 11 người",
        "gia_thue_mot_gio": 1200000,
        "trang_thai": "ACTIVE",
    },
]
