Kế hoạch: Web app chia tiền ăn uống (1 file HTML)
Context
Cả nhóm đi ăn, chỉ một vài người trả tiền. Cần một app HTML siêu đơn giản: nhập ai đã trả bao nhiêu, app chia đều tổng tiền cho mọi người và cho biết từng người cần trả thêm / nhận lại bao nhiêu, kèm danh sách chuyển tiền gọn nhất.

Các lựa chọn đã chốt với người dùng:

Nhập liệu: mỗi người một dòng Tên + Đã trả (0 nếu không trả). Tổng bill = tổng số đã trả.
Kết quả: cả số dư từng người và danh sách "A chuyển cho B X đ".
Tiền tệ: VNĐ, làm tròn tới 1.000đ, hiển thị dạng 120.000đ.
Không lưu dữ liệu (tải lại trang là mất).
File tạo mới
c:\study\Vibe_Coding_Claude_Code\my_proj\chia-tien\index.html — một file duy nhất chứa HTML + CSS + JS thuần, không thư viện, mở trực tiếp bằng trình duyệt.
Giao diện
Tiêu đề "Chia tiền ăn uống".
Bảng người tham gia: mỗi dòng gồm ô Tên, ô Đã trả (đ) (type=number, min=0, step=1000), nút ✕ xóa dòng. Mặc định 3 dòng trống.
Nút + Thêm người và nút Tính tiền (có thể tính lại tự động mỗi khi nhập — input event — để khỏi cần bấm).
Khu vực tóm tắt: Tổng bill, Số người, Mỗi người phải trả.
Bảng số dư: Tên | Đã trả | Chênh lệch, màu xanh "Nhận lại X đ", màu đỏ "Cần trả X đ", xám "Đã đủ".
Danh sách chuyển tiền: "An → Bình: 50.000đ".
CSS đơn giản, responsive cho điện thoại (max-width ~480px, căn giữa).
Logic (JS)
people = các dòng có tên (dòng tên trống bị bỏ qua; tên trống mà có tiền → đặt "Người N")
total  = Σ paid
share  = total / n
balance_i = paid_i - share            // >0: nhận lại, <0: cần trả
Làm tròn 1.000đ: round1000(x) = Math.round(x / 1000) * 1000, áp dụng khi hiển thị số dư và số tiền chuyển. Tính toán nội bộ giữ số chính xác để tổng không bị lệch nhiều; nếu do làm tròn có chênh lệch nhỏ, hiển thị ghi chú nhỏ "(chênh lệch do làm tròn: X đ)".

Danh sách chuyển tiền (tham lam, tối thiểu số giao dịch gần đúng):

Tách debtors (balance < 0) và creditors (balance > 0), sắp xếp giảm dần theo độ lớn.
Lặp: lấy debtor lớn nhất và creditor lớn nhất, amt = min(|d|, c), ghi "d → c: amt", trừ hai bên; ai về ~0 (|x| < 1) thì loại khỏi danh sách.
Bỏ các giao dịch có round1000(amt) == 0.
Định dạng tiền: n.toLocaleString('vi-VN') + 'đ'.

Kiểm tra đầu vào: số âm → coi là 0; < 2 người hoặc tổng = 0 → hiện thông báo "Nhập ít nhất 2 người và số tiền đã trả".

Các bước thực hiện
Tạo thư mục chia-tien/ và index.html với khung HTML + CSS.
Viết JS: thêm/xóa dòng, đọc dữ liệu, calculate(), settle(), render().
Gắn sự kiện input / click để tự tính lại.
Kiểm tra (verification)
Mở chia-tien/index.html bằng trình duyệt và thử:

Ca 1: An 300.000, Bình 0, Chi 0 → mỗi người 100.000; An nhận lại 200.000; Bình → An 100.000, Chi → An 100.000.
Ca 2: An 200.000, Bình 100.000, Chi 0, Dũng 0 → mỗi người 75.000; An +125.000, Bình +25.000, Chi −75.000, Dũng −75.000; 3 giao dịch, tổng chuyển = 150.000.
Ca 3 (làm tròn): An 100.000, Bình 0, Chi 0 → share 33.333 → hiển thị 33.000 / nhận lại 67.000, có ghi chú chênh lệch làm tròn.
Ca biên: 1 người, tất cả 0, tên trống, xóa hết dòng → hiện thông báo, không lỗi console.
Thu nhỏ cửa sổ về cỡ điện thoại → giao diện không bị tràn ngang.