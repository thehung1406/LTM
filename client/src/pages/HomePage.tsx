import { useNavigate } from 'react-router-dom';
import { MessageCircle } from 'lucide-react';

function HomePage() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-cyan-50 flex items-center justify-center p-4">
      <div className="max-w-4xl w-full bg-white rounded-2xl shadow-xl p-12 text-center">
        <div className="flex justify-center mb-8">
          <div className="bg-blue-500 p-4 rounded-full">
            <MessageCircle className="w-16 h-16 text-white" />
          </div>
        </div>

        <h1 className="text-5xl font-bold text-gray-800 mb-4">
          Welcome to LTM Chat
        </h1>

        <p className="text-xl text-gray-600 mb-12">
          Connect with friends and family instantly
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <button
            onClick={() => navigate('/login')}
            className="w-full sm:w-auto px-8 py-3 bg-blue-500 text-white rounded-lg font-semibold hover:bg-blue-600 transition-colors shadow-md"
          >
            Đăng nhập
          </button>

          <button
            onClick={() => navigate('/register')}
            className="w-full sm:w-auto px-8 py-3 bg-white text-blue-500 border-2 border-blue-500 rounded-lg font-semibold hover:bg-blue-50 transition-colors"
          >
            Đăng ký
          </button>
        </div>
      </div>
    </div>
  );
}

export default HomePage;
