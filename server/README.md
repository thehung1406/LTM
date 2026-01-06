# MODULE SERVER

> 📘 *Sinh viên mô tả phần **server** tại đây. Điền đầy đủ theo framework và bài toán của nhóm.*

---

## 🎯 MỤC TIÊU

Server chịu trách nhiệm:
- Xử lý logic nghiệp vụ, xác thực người dùng, quản lý dữ liệu tin nhắn
- Quản lý kết nối WebSocket Realtime
- Trả kết quả cho client

---

## ⚙️ CÔNG NGHỆ SỬ DỤNG

| Thành phần | Công nghệ |
|------------|-----------|
| Ngôn ngữ | Python |
| Framework | Fast API|
| Database | MongoDB |

---

## 🚀 HƯỚNG DẪN CHẠY

### Cài đặt
```bash

# Cài đặt uv
pip install uv
# Chạy máy ảo
.\.venv\Scripts\Activate.ps1
Sau khi chạy, bạn sẽ thấy đầu dòng terminal đổi như sau:
'(.venv) PS C:\Users\admin\PycharmProjects\<project>'
Nghĩa là bạn đang “bật” máy ảo thành công.
# Cài thư viện từ pyproject.toml
uv sync
```

### Khởi động server
```bash
uvicorn main:app --reload

Server chạy tại: `http://localhost:8080`
---
```
## 🔗 API

| Endpoint | Method | Input | Output |
|----------|--------|-------|--------|
| /health | GET | — | {"status":"ok"} |
|/api/register| POST | { "username", "password", "fullname" } | trả về thông tin user vừa tạo (không có mật khẩu). |


> **Lưu ý:** Bổ sung các endpoint của nhóm vào bảng trên.

---

## 📦 CẤU TRÚC
```
server/
├── core/
│   ├── __init__.py
│   ├── config.py
│   └── database.py
├── models/
│   ├── __init__.py
│   └── user.py
├── routers/
│   ├── __init__.py
│   └── auth.py
├── schemas/
│   ├── __init__.py
│   ├── token.py
│   └── user.py
├── services/
│   ├── __init__.py
│   └── user_service.py
├── utils/
│   ├── __init__.py
│   ├── dependencies.py
│   ├── jwt.py
│   └── security.py
├── .gitignore
├── .python-version
├── main.py
├── pyproject.toml
├── README.md
└── uv.lock
```

## 🧪 TEST
```bash
# Test API bằng curl
curl http://localhost:8080/health
```

---

## 📝 GHI CHÚ

- Port mặc định: **8080**
- Có thể thay đổi trong file `.env` hoặc config
