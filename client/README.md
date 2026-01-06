# MODULE CLIENT

> 📘 *Giao diện người dùng cho ứng dụng **Chat Realtime** được xây dựng bằng React + TypeScript + Vite*

---

## 🎯 MỤC TIÊU

Client chịu trách nhiệm:
- Cung cấp giao diện người dùng trực quan và thân thiện
- Xử lý xác thực (đăng nhập/đăng ký) và quản lý phiên làm việc
- Hiển thị danh sách bạn bè và lịch sử tin nhắn
- Gửi/nhận tin nhắn realtime qua WebSocket
- Quản lý thông báo và yêu cầu kết bạn
- Cập nhật trạng thái online/offline của người dùng

---

## ⚙️ CÔNG NGHỆ SỬ DỤNG

| Thành phần | Công nghệ |
|------------|-----------|
| Framework | React 18.3.1 + TypeScript 5.5.3 |
| Build Tool | Vite 5.4.2 |
| Routing | React Router DOM 7.9.5 |
| HTTP Client | Axios 1.13.1 |
| UI Styling | TailwindCSS 3.4.1 + PostCSS + Autoprefixer |
| Icons | Lucide React 0.344.0 |
| Backend Service | Supabase JS 2.57.4 |
| Giao thức | HTTP/HTTPS + WebSocket |

---

## 🚀 HƯỚNG DẪN CHẠY

### Cài đặt
```bash
# Di chuyển vào thư mục client
cd source/client

# Cài đặt các dependencies
npm install
```

### Chạy chương trình
```bash
# Chạy ở chế độ development
npm run dev

# Build cho production
npm run build

# Preview bản build
npm run preview

# Kiểm tra lỗi ESLint
npm run lint

# Kiểm tra TypeScript
npm run typecheck
```

### Cấu hình (nếu cần)
- Server URL: `http://localhost:8000` (FastAPI Backend)
- WebSocket URL: `ws://localhost:8000/ws`
- Development Port: `http://localhost:5173` (Vite default)
- Có thể thay đổi URL trong các file component khi cần

---

## 📦 CẤU TRÚC
```
client/
├── README.md                    # File tài liệu này
├── package.json                 # Dependencies và scripts
├── tsconfig.json                # TypeScript configuration
├── vite.config.cjs              # Vite configuration
├── tailwind.config.js           # TailwindCSS configuration
├── postcss.config.js            # PostCSS configuration
├── eslint.config.js             # ESLint configuration
├── index.html                   # HTML entry point
├── public/                      # Static assets
└── src/
    ├── main.tsx                 # Entry point của ứng dụng
    ├── App.tsx                  # Main App component (routing)
    ├── App.css                  # Global styles
    ├── index.css                # TailwindCSS imports
    ├── assets/                  # Images, fonts, icons
    ├── components/              # Reusable components
    │   ├── AccountSettingsModal.tsx    # Modal cài đặt tài khoản
    │   ├── AddFriendDialog.tsx         # Dialog thêm bạn bè
    │   └── NotifyDialog.tsx            # Dialog thông báo
    └── pages/                   # Page components
        ├── HomePage.tsx         # Landing page
        ├── Login.tsx            # Trang đăng nhập
        ├── Register.tsx         # Trang đăng ký
        ├── TermsAndConditions.tsx   # Điều khoản sử dụng
        └── ChatMain.tsx         # Giao diện chat chính
```

---

## 💡 SỬ DỤNG

### Chạy ứng dụng
```bash
# Khởi động development server
npm run dev

# Truy cập: http://localhost:5173
```

### Các tính năng chính:
- **Đăng nhập/Đăng ký**: Xác thực người dùng với token-based authentication
- **Chat Realtime**: Gửi/nhận tin nhắn tức thời qua WebSocket
- **Quản lý bạn bè**: Tìm kiếm, thêm bạn bè, xem trạng thái online
- **Thông báo**: Nhận thông báo yêu cầu kết bạn và tin nhắn mới
- **Đính kèm file**: Hỗ trợ gửi file trong tin nhắn
- **Tìm kiếm**: Tìm kiếm trong danh sách hội thoại

---

## 📝 GHI CHÚ

- Đảm bảo server đã chạy tại `localhost:8000` trước khi khởi động client
- Token xác thực được lưu trong `localStorage` với key `token`
- Thông tin user được lưu trong `localStorage` với key `user`
- WebSocket tự động reconnect khi bị ngắt kết nối
- CORS cần được cấu hình trên server cho origin `http://localhost:5173`
- Responsive design hỗ trợ đầy đủ trên mobile, tablet và desktop