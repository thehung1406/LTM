import { useState, useEffect } from "react";
import axios from "axios";
import { Settings } from "lucide-react";

interface User {
  username: string;
  fullname: string;
}

interface AccountSettingsModalProps {
  open: boolean;
  onClose: () => void;
  onLogout: () => void;
  onChangePassword: (
    oldPassword: string,
    newPassword: string,
    confirmPassword: string
  ) => void;
}

export default function AccountSettingsModal({
  open,
  onClose,
  onLogout,

}: AccountSettingsModalProps) {
  const [oldPassword, setOldPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState<string>("");
  const [user, setUser] = useState<User>({ username: "", fullname: "" });

  useEffect(() => {
    if (open) {
      const localUser = localStorage.getItem("user");
      if (localUser) {
        setUser(JSON.parse(localUser));
      }
    }
  }, [open]);

  if (!open) return null;

  const handleChangePassword = async () => {
    setError(""); // reset lỗi

    if (newPassword !== confirmPassword) {
      setError("Mật khẩu mới và xác nhận mật khẩu không khớp");
      return;
    }

    if (!oldPassword || !newPassword || !confirmPassword) {
      setError("Vui lòng nhập đầy đủ các trường mật khẩu");
      return;
    }

    try {
      await axios.patch(
        "http://127.0.0.1:8000/auth/change-password",
        {
          old_password: oldPassword,
          new_password: newPassword,
          confirm_password: confirmPassword,
        },
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        }
      );

      setError("");
      alert("Đổi mật khẩu thành công!");
      onClose();
    } catch (err: any) {
      if (err.response && err.response.data && err.response.data.detail) {
        const detail = err.response.data.detail;
        if (typeof detail === "string") {
          setError(detail);
        } else if (Array.isArray(detail)) {
          setError(detail.map((d: any) => d.msg || JSON.stringify(d)).join(", "));
        } else if (typeof detail === "object") {
          setError(JSON.stringify(detail));
        } else {
          setError("Đổi mật khẩu thất bại");
        }
      } else {
        setError("Đổi mật khẩu thất bại");
      }
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl shadow-lg p-6 w-full max-w-md relative">
        <h2 className="text-xl font-bold mb-4 flex items-center">
          <Settings className="w-6 h-6 mr-2" /> Cài đặt tài khoản
        </h2>
        <p className="font-medium mb-1">Tên đăng nhập: {user.username}</p>
        <p className="font-medium mb-4">Họ và tên: {user.fullname}</p>

        <div className="mb-4">
          <label className="block font-medium mb-2">Mật khẩu hiện tại</label>
          <input
            type="password"
            placeholder="Mật khẩu hiện tại"
            value={oldPassword}
            onChange={(e) => setOldPassword(e.target.value)}
            className="w-full border rounded-lg px-3 py-2 mb-2"
          />
          <label className="block font-medium mb-2">Mật khẩu mới</label>
          <input
            type="password"
            placeholder="Mật khẩu mới"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            className="w-full border rounded-lg px-3 py-2 mb-2"
          />
          <label className="block font-medium mb-2">Xác nhận mật khẩu mới</label>
          <input
            type="password"
            placeholder="Xác nhận mật khẩu mới"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            className="w-full border rounded-lg px-3 py-2 mb-2"
          />
          {error && (
            <p className="text-red-600 mt-2 text-center">{error}</p>
          )}
          <button
            className="mt-2 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            onClick={handleChangePassword}
          >
            Đổi mật khẩu
          </button>
        </div>

        <button
          onClick={onLogout}
          className="w-full mt-2 py-2 bg-red-500 text-white rounded-lg font-bold hover:bg-red-600 transition"
        >
          Đăng xuất
        </button>

        <button
          onClick={onClose}
          className="absolute top-3 right-3 text-gray-400 hover:text-gray-600"
        >
          Đóng
        </button>
      </div>
    </div>
  );
}
