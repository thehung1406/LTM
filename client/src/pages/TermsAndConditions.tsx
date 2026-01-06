import { useNavigate } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';

function TermsAndConditions() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-cyan-50 p-4">
      <div className="max-w-3xl mx-auto bg-white rounded-2xl shadow-xl p-8 my-8">
        <button
          onClick={() => navigate(-1)}
          className="flex items-center text-blue-500 hover:text-blue-600 mb-6"
        >
          <ArrowLeft className="w-5 h-5 mr-2" />
          Quay lại
        </button>

        <h1 className="text-3xl font-bold text-gray-800 mb-6">
          Điều khoản và Điều kiện
        </h1>

        <div className="space-y-6 text-gray-700">
          <section>
            <h2 className="text-xl font-semibold mb-3">1. Chấp nhận Điều khoản</h2>
            <p className="leading-relaxed">
              Bằng cách truy cập và sử dụng ứng dụng Chat App, bạn đồng ý tuân thủ và bị ràng buộc bởi các điều khoản và điều kiện sau đây. Nếu bạn không đồng ý với bất kỳ phần nào của các điều khoản này, vui lòng không sử dụng dịch vụ của chúng tôi.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold mb-3">2. Sử dụng Dịch vụ</h2>
            <p className="leading-relaxed mb-2">
              Bạn đồng ý sử dụng Chat App chỉ cho các mục đích hợp pháp và theo cách không vi phạm quyền của người khác hoặc hạn chế hoặc ngăn cản việc sử dụng và tận hưởng dịch vụ của họ.
            </p>
            <ul className="list-disc list-inside space-y-1 ml-4">
              <li>Không spam hoặc gửi nội dung quấy rối</li>
              <li>Không chia sẻ nội dung bất hợp pháp hoặc gây hại</li>
              <li>Tôn trọng quyền riêng tư của người dùng khác</li>
              <li>Không mạo danh người khác</li>
            </ul>
          </section>

          <section>
            <h2 className="text-xl font-semibold mb-3">3. Tài khoản Người dùng</h2>
            <p className="leading-relaxed">
              Bạn chịu trách nhiệm duy trì tính bảo mật của tài khoản và mật khẩu của mình. Bạn đồng ý chấp nhận trách nhiệm cho tất cả các hoạt động xảy ra dưới tài khoản của bạn.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold mb-3">4. Quyền riêng tư</h2>
            <p className="leading-relaxed">
              Chúng tôi cam kết bảo vệ quyền riêng tư của bạn. Thông tin cá nhân của bạn sẽ được xử lý theo Chính sách Quyền riêng tư của chúng tôi. Chúng tôi không bán hoặc chia sẻ thông tin cá nhân của bạn với bên thứ ba mà không có sự đồng ý của bạn.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold mb-3">5. Nội dung</h2>
            <p className="leading-relaxed">
              Bạn giữ quyền sở hữu đối với bất kỳ nội dung nào bạn gửi hoặc chia sẻ qua Chat App. Tuy nhiên, bằng cách gửi nội dung, bạn cấp cho chúng tôi quyền sử dụng, lưu trữ và hiển thị nội dung đó nhằm cung cấp dịch vụ.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold mb-3">6. Chấm dứt</h2>
            <p className="leading-relaxed">
              Chúng tôi có quyền chấm dứt hoặc tạm ngưng quyền truy cập của bạn vào dịch vụ ngay lập tức, mà không cần thông báo trước hoặc chịu trách nhiệm pháp lý, vì bất kỳ lý do gì, bao gồm cả việc vi phạm các Điều khoản này.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold mb-3">7. Thay đổi Điều khoản</h2>
            <p className="leading-relaxed">
              Chúng tôi có quyền sửa đổi hoặc thay thế các Điều khoản này bất cứ lúc nào. Chúng tôi sẽ thông báo cho bạn về bất kỳ thay đổi quan trọng nào bằng cách đăng các điều khoản mới trên trang này.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold mb-3">8. Liên hệ</h2>
            <p className="leading-relaxed">
              Nếu bạn có bất kỳ câu hỏi nào về các Điều khoản này, vui lòng liên hệ với chúng tôi qua email: support@gmail.com
            </p>
          </section>
        </div>

        <div className="mt-8 pt-6 border-t border-gray-200">
          <p className="text-sm text-gray-500 text-center">
            Cập nhật lần cuối: {new Date().toLocaleDateString('vi-VN')}
          </p>
        </div>
      </div>
    </div>
  );
}

export default TermsAndConditions;
