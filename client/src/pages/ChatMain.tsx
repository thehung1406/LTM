import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Send, Plus, Bell, LogOut, Search, MoreVertical, Paperclip, Settings } from 'lucide-react';
import NotifyDialog from '../components/NotifyDialog';
import AddFriendDialog from '../components/AddFriendDialog';
import AccountSettingsModal from '../components/AccountSettingsModal';

interface Contact {
  id: number;
  name: string;
  lastMessage: string;
  time: string;
  avatar: string;
  unread?: number;
  isOnline: boolean;
}

interface Message {
  id: number;
  text: string;
  sender: 'me' | 'other';
  time: string;
  file?: File;
}

function ChatMain() {
  const navigate = useNavigate();
  const [showNotify, setShowNotify] = useState(false);
  const [showAddFriend, setShowAddFriend] = useState(false);
  const [selectedContact, setSelectedContact] = useState<Contact | null>(null);
  const [messageInput, setMessageInput] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [showSettings, setShowSettings] = useState(false);
  const [infoOpen, setInfoOpen] = useState(true);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const userString = localStorage.getItem("user")



  const contacts: Contact[] = [
    {
      id: 1,
      name: 'Nguyễn Văn A',
      lastMessage: 'Chào bạn!',
      time: '10:30',
      avatar: '👤',
      unread: 2,
      isOnline: true,
    },
    {
      id: 2,
      name: 'Trần Thị B',
      lastMessage: 'Hẹn gặp lại nhé',
      time: '09:15',
      avatar: '👤',
      isOnline: false,
    },
    {
      id: 3,
      name: 'Lê Văn C',
      lastMessage: 'Cảm ơn bạn nhiều',
      time: 'Hôm qua',
      avatar: '👤',
      isOnline: true,
    },
  ];

const [user, setUser] = useState({ username: "", fullName: "" });

useEffect(() => {
  const userStr = localStorage.getItem("user");
  if (userStr) {
    setUser(JSON.parse(userStr));
  }
}, []);

  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      text: 'Chào bạn! Bạn khỏe không?',
      sender: 'other',
      time: '10:25',
    },
    {
      id: 2,
      text: 'Mình khỏe, cảm ơn bạn!',
      sender: 'me',
      time: '10:26',
    },
    {
      id: 3,
      text: 'Tuyệt vời! Hôm nay bạn có rảnh không?',
      sender: 'other',
      time: '10:30',
    },
  ]);

  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (selectedFile) {
      // Thêm file vào chat như một tin nhắn đặc biệt
      setMessages([...messages, {
        id: messages.length + 1,
        text: '', // hoặc messageInput nếu muốn gửi cả text
        file: selectedFile, // thêm trường file
        sender: 'me',
        time: new Date().toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' }),
      }]);
      setSelectedFile(null);
      setMessageInput('');
    } else if (messageInput.trim() && selectedContact) {
      const newMessage: Message = {
        id: messages.length + 1,
        text: messageInput,
        sender: 'me',
        time: new Date().toLocaleTimeString('vi-VN', {
          hour: '2-digit',
          minute: '2-digit',
        }),
      };
      setMessages([...messages, newMessage]);
      setMessageInput('');
    }
  };
  const handleChangeAvatar = (file: File | null) => {
    if (file) {
      console.log('Avatar mới:', file);
      // Xử lý update avatar ở đây
    }
  };

  const handleChangePassword = (newPassword: string, confirmPassword: string) => {
    if (newPassword === confirmPassword) {
      console.log('Đổi mật khẩu:', newPassword);
      // Gọi API đổi mật khẩu
    } else {
      alert('Mật khẩu xác nhận không khớp');
    }
  };

  const handleLogout = () => {
    navigate('/');
  };

  const filteredContacts = contacts.filter((contact) =>
    contact.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="h-screen flex bg-gray-50 relative">
      <div className="w-80 bg-white border-r border-gray-200 flex flex-col">
        <div className="p-4 border-b border-gray-200">
          <div className="flex items-center justify-between mb-4">
            <h1 className="text-2xl font-bold text-gray-800">Chat App</h1>
            <div className="flex items-center gap-2">
              <button
                onClick={() => setShowNotify(true)}
                className="p-2 hover:bg-gray-100 rounded-full transition-colors relative"
              >
                <Bell className="w-5 h-5 text-gray-600" />
                <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
              </button>
              <button
                onClick={() => setShowAddFriend(true)}
                className="p-2 hover:bg-gray-100 rounded-full transition-colors"
              >
                <Plus className="w-5 h-5 text-gray-600" />
              </button>
              <button
                onClick={() => setShowSettings(true)}
                className="p-2 hover:bg-gray-100 rounded-full transition-colors"
              >
                <Settings className="w-5 h-5 text-gray-600" />
              </button>

            </div>
          </div>

          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Tìm kiếm..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>

        <div className="flex-1 overflow-y-auto">
          {filteredContacts.map((contact) => (
            <button
              key={contact.id}
              onClick={() => setSelectedContact(contact)}
              className={`w-full p-4 flex items-center gap-3 hover:bg-gray-50 transition-colors border-b border-gray-100 ${selectedContact?.id === contact.id ? 'bg-blue-50' : ''
                }`}
            >
              <div className="relative flex-shrink-0">
                <div className="w-12 h-12 bg-blue-500 rounded-full flex items-center justify-center text-2xl">
                  {contact.avatar}
                </div>
                <div
                  className={`absolute bottom-0 right-0 w-3 h-3 rounded-full border-2 border-white ${contact.isOnline ? 'bg-green-500' : 'bg-gray-400'
                    }`}
                ></div>
              </div>
              <div className="flex-1 min-w-0 text-left">
                <div className="flex items-center justify-between mb-1">
                  <h3 className="font-semibold text-gray-800 truncate">
                    {contact.name}
                  </h3>
                  <span className="text-xs text-gray-500">{contact.time}</span>
                </div>
                <div className="flex items-center justify-between">
                  <p className="text-sm text-gray-600 truncate">
                    {contact.lastMessage}
                  </p>
                  {contact.unread && (
                    <span className="ml-2 bg-blue-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center flex-shrink-0">
                      {contact.unread}
                    </span>
                  )}
                </div>
              </div>
            </button>
          ))}
        </div>
      </div>

      <div className="flex-1 flex flex-col">
        {selectedContact ? (
          <>
            <div className="bg-white border-b border-gray-200 p-4 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="relative">
                  <div className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center text-xl">
                    {selectedContact.avatar}
                  </div>
                  <div
                    className={`absolute bottom-0 right-0 w-2.5 h-2.5 rounded-full border-2 border-white ${selectedContact.isOnline ? 'bg-green-500' : 'bg-gray-400'
                      }`}
                  ></div>
                </div>
                <div>
                  <h2 className="font-semibold text-gray-800">
                    {selectedContact.name}
                  </h2>
                  <p
                    className={`text-sm ${selectedContact.isOnline ? 'text-green-500' : 'text-gray-500'
                      }`}
                  >
                    {selectedContact.isOnline ? 'Đang hoạt động' : 'Ngoại tuyến'}
                  </p>
                </div>
              </div>
              <button
                onClick={() => setInfoOpen(!infoOpen)}
                className="p-2 hover:bg-gray-100 rounded-full transition-colors"
              >
                <MoreVertical className="w-5 h-5 text-gray-600" />
              </button>
            </div>

            <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.sender === 'me' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-md px-4 py-2 rounded-2xl ${message.sender === 'me'
                        ? 'bg-blue-500 text-white'
                        : 'bg-white text-gray-800 border border-gray-200'
                      }`}
                  >
                    {message.file ? (
                      <div className="flex items-center gap-2">
                        <span className="font-medium">{message.file.name}</span>
                        <span className="text-xs">{(message.file.size / 1024).toFixed(1)} KB</span>
                      </div>
                    ) : (
                      <p>{message.text}</p>
                    )}
                    <p
                      className={`text-xs mt-1 ${message.sender === 'me'
                          ? 'text-blue-100'
                          : 'text-gray-500'
                        }`}
                    >
                      {message.time}
                    </p>
                  </div>
                </div>
              ))}
            </div>


            <div className="bg-white border-t border-gray-200 p-4">
              {selectedFile && (
                <div className="mb-2 px-4 py-2 bg-gray-100 rounded-lg w-full flex flex-col">
                  <div className="flex items-center gap-2 mb-1">
                    <Paperclip className="w-5 h-5 text-blue-500" />
                    <span className="font-medium">{selectedFile.name}</span>
                    <span className="text-xs text-gray-500">{(selectedFile.size / 1024).toFixed(1)} KB</span>
                    <button
                      className="ml-auto px-2 py-1 rounded text-red-500 hover:bg-red-100"
                      onClick={() => setSelectedFile(null)}
                    >
                      X
                    </button>
                  </div>
                </div>
              )}

              <form onSubmit={handleSendMessage} className="flex items-center gap-2">
                <button
                  type="button"
                  className="p-2 hover:bg-gray-100 rounded-full transition-colors"
                  onClick={() => document.getElementById('fileInput')?.click()}
                >
                  <Paperclip className="w-6 h-6 text-gray-600" />
                  <input
                    type="file"
                    id="fileInput"
                    className="hidden"
                    onChange={(e) => {
                      const file = e.target.files ? e.target.files[0] : null;
                      if (file) {
                        setSelectedFile(file);
                      }
                    }}
                  />
                </button>

                <input
                  type="text"
                  value={messageInput}
                  onChange={(e) => setMessageInput(e.target.value)}
                  placeholder="Nhập tin nhắn..."
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button
                  type="submit"
                  className="p-2 bg-blue-500 hover:bg-blue-600 rounded-full transition-colors"
                >
                  <Send className="w-6 h-6 text-white" />
                </button>
              </form>
            </div>
          </>
        ) : null}
      </div>

      <div className={`${infoOpen ? 'w-80' : 'w-0'} bg-white border-l border-gray-200 transition-all duration-300 overflow-hidden flex flex-col`}>
        {selectedContact && (
          <>
            <div className="p-4 border-b border-gray-200">
              <h3 className="font-bold text-gray-800 text-lg">Thông tin</h3>
            </div>

            <div className="flex-1 overflow-y-auto p-4 space-y-6">
              <div className="flex flex-col items-center py-4">
                <div className="relative mb-4">
                  <div className="w-24 h-24 bg-blue-500 rounded-full flex items-center justify-center text-5xl">
                    {selectedContact.avatar}
                  </div>
                  <div
                    className={`absolute bottom-2 right-2 w-4 h-4 rounded-full border-2 border-white ${selectedContact.isOnline ? 'bg-green-500' : 'bg-gray-400'
                      }`}
                  ></div>
                </div>
                <h2 className="text-xl font-bold text-gray-800">
                  {selectedContact.name}
                </h2>
                <p
                  className={`text-sm mt-1 ${selectedContact.isOnline ? 'text-green-500' : 'text-gray-500'
                    }`}
                >
                  {selectedContact.isOnline ? 'Đang hoạt động' : 'Ngoại tuyến'}
                </p>
              </div>

              <div className="border-t border-gray-200 pt-4">
                <p className="text-sm text-gray-500 mb-2">LIÊN HỆ</p>
                <div className="space-y-3">
                  <div>
                    <p className="text-xs text-gray-500 font-semibold">TÊN ĐĂNG NHẬP</p>
                    <p className="text-sm text-gray-800 mt-1">user_{selectedContact.id}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500 font-semibold">TRẠNG THÁI</p>
                    <p className="text-sm text-gray-800 mt-1">
                      {selectedContact.isOnline ? 'Online' : 'Offline'}
                    </p>
                  </div>
                </div>
              </div>

              <div className="border-t border-gray-200 pt-4">
                <p className="text-sm text-gray-500 mb-2">HÀNH ĐỘNG</p>
                <div className="space-y-2">
                  <button className="w-full text-left px-3 py-2 rounded-lg hover:bg-gray-100 text-gray-700 transition-colors text-sm">
                    Xem tất cả tin nhắn
                  </button>
                  <button className="w-full text-left px-3 py-2 rounded-lg hover:bg-red-50 text-red-600 transition-colors text-sm">
                    Xóa cuộc hội thoại
                  </button>
                </div>
              </div>
            </div>
          </>
        )}
      </div>

      {!selectedContact && (
        <div className="absolute inset-0 left-80 right-0 flex items-center justify-center bg-gray-50">
          <div className="text-center">
            <div className="w-24 h-24 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Plus className="w-12 h-12 text-blue-500" />
            </div>
            <h2 className="text-2xl font-semibold text-gray-800 mb-2">
              Chọn một cuộc trò chuyện
            </h2>
            <p className="text-gray-600">
              Chọn một người bạn để bắt đầu trò chuyện
            </p>
          </div>
        </div>
      )}

      {showNotify && <NotifyDialog onClose={() => setShowNotify(false)} />}
      {showAddFriend && <AddFriendDialog onClose={() => setShowAddFriend(false)} />}
      {showSettings && (
        <AccountSettingsModal
          open={showSettings}
          onClose={() => setShowSettings(false)}
          onLogout={handleLogout}
          onChangePassword={handleChangePassword} />
      )}

    </div>
  );
}

export default ChatMain;
