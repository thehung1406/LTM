import { X } from 'lucide-react';

interface Notification {
  id: number;
  title: string;
  message: string;
  time: string;
  isRead: boolean;
}

interface NotifyDialogProps {
  onClose: () => void;
}

function NotifyDialog({ onClose }: NotifyDialogProps) {
  const notifications: Notification[] = [
    {
      id: 1,
      title: 'Lời mời kết bạn',
      message: 'Phạm Văn D đã gửi lời mời kết bạn cho bạn',
      time: '5 phút trước',
      isRead: false,
    },
    {
      id: 2,
      title: 'Tin nhắn mới',
      message: 'Bạn có 3 tin nhắn mới từ Nguyễn Văn A',
      time: '1 giờ trước',
      isRead: false,
    },
    {
      id: 3,
      title: 'Cập nhật hệ thống',
      message: 'LTM Chat đã cập nhật phiên bản mới',
      time: 'Hôm qua',
      isRead: true,
    },
  ];

  const handleBackdropClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  return (
    <div
      className="fixed inset-0 bg-black bg-opacity-50 flex items-start justify-center pt-20 z-50"
      onClick={handleBackdropClick}
    >
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md mx-4 max-h-[80vh] flex flex-col">
        <div className="p-4 border-b border-gray-200 flex items-center justify-between">
          <h2 className="text-xl font-bold text-gray-800">Thông báo</h2>
          <button
            onClick={onClose}
            className="p-1 hover:bg-gray-100 rounded-full transition-colors"
          >
            <X className="w-6 h-6 text-gray-600" />
          </button>
        </div>

        <div className="flex-1 overflow-y-auto">
          {notifications.map((notification) => (
            <div
              key={notification.id}
              className={`p-4 border-b border-gray-100 hover:bg-gray-50 transition-colors cursor-pointer ${
                !notification.isRead ? 'bg-blue-50' : ''
              }`}
            >
              <div className="flex items-start justify-between mb-1">
                <h3 className="font-semibold text-gray-800">
                  {notification.title}
                </h3>
                {!notification.isRead && (
                  <span className="w-2 h-2 bg-blue-500 rounded-full mt-1"></span>
                )}
              </div>
              <p className="text-sm text-gray-600 mb-2">{notification.message}</p>
              <p className="text-xs text-gray-500">{notification.time}</p>
            </div>
          ))}
        </div>

        <div className="p-4 border-t border-gray-200">
          <button className="w-full text-center text-blue-500 font-semibold hover:text-blue-600 transition-colors">
            Đánh dấu tất cả đã đọc
          </button>
        </div>
      </div>
    </div>
  );
}

export default NotifyDialog;
