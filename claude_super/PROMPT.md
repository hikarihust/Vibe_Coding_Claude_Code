Tôi muốn tạo một giao diện chatbot với phần LLM tôi sẽ sử dụng từ Ollama (model là "gemma4:31b-cloud")

- Có phần khung chat thể hiện conversation giữa user và chatbot
- Ở bên dưới có phần nhập text nhiều dòng, có nút "Send" đẻ user có thể gửi text đi
- Bên tay trái tôi muốn có phần lịch sử các session đã được lưu
- Tên của session sẽ lấy dựa trên tên của prompt đầu tiên của user trong session đấy (giới hạn 20 kí tự)
- Các sessions sẽ được lưu vào trong database (sqlite cho đơn giản). Mục tiêu của tôi là khi user click vào session nào đó thì conversation history của session được load trở lại và hiển thị để có thể tiếp tục chat
- Bên cạnh tên của session sẽ có dấu "..." hiển thị cho phép user có thể đổi tên session và có thể xoá session. Chỉ hiển thị khi user hover qua
- Tôi muốn có một tiêu đề chung là "AI Coding's Chatbot"
- Bên trên sidebar của lịch sử session sẽ có phần "New Chat" cho phép user tạo ra đoạn hội thoại mới
- Tạm thời chưa cần thiết kế user
- Frontend sử dụng react + typescript với vite. CSS thì dùng Tailwind CSS
- Backend sẽ sử dụng fastapi
- Database sử dụng sqlite
