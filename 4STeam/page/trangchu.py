import tkinter as tk
from tkinter import ttk
import customtkinter as ctk


class HomeUI:
    def __init__(self, root, username, role, on_logout, on_go_to_products, on_go_to_accounts):
        self.root = root
        self.username = username
        self.role = role
        self.on_logout = on_logout
        self.on_go_to_products = on_go_to_products
        self.on_go_to_accounts = on_go_to_accounts
        self.setup_ui()

    def setup_ui(self):
        # Thiết lập nền tổng thể cho trang chủ sáng sủa, mượt mà
        if hasattr(self.root, 'configure'):
            self.root.configure(fg_color="#F8F9FA")
        else:
            self.root.configure(bg="#F8F9FA")

        # =================================================================
        # --- HEADER BANNER NÂNG CẤP NGHỆ THUẬT (THEO MẪU IMAGE_D1E7CC) ---
        # =================================================================
        # Khung viền bọc bên ngoài tạo khoảng cách lề thụt vào cân đối
        header_container = ctk.CTkFrame(self.root, fg_color="transparent")
        header_container.pack(fill="x", padx=30, pady=(20, 10))

        # Khung Header chính màu xanh đen, bo tròn góc 16px cực mượt
        header = ctk.CTkFrame(
            header_container, fg_color="#2B323F", height=100, corner_radius=16
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        # -----------------------------------------------------------------
        # HOẠ TIẾT HÌNH KHỐI CHẠY NGẦM (Tạo hiệu ứng chiều sâu như ảnh mẫu)
        # -----------------------------------------------------------------
        # 1. Khối tròn lớn mờ ở góc trên bên phải thanh Banner
        circle_top_right = ctk.CTkFrame(header, fg_color="#343A40", width=120, height=120, corner_radius=60)
        circle_top_right.place(relx=0.75, rely=-0.3, anchor="center")

        # 2. Khối tròn lớn mờ ẩn dưới góc dưới bên trái thanh Banner
        circle_bottom_left = ctk.CTkFrame(header, fg_color="#212529", width=100, height=100, corner_radius=50)
        circle_bottom_left.place(relx=0.05, rely=1.1, anchor="center")

        # 3. Chấm cam thương hiệu nhỏ nhắn làm điểm nhấn nghệ thuật phía trước chữ
        brand_dot = ctk.CTkFrame(header, fg_color="#E67E22", width=10, height=10, corner_radius=5)
        brand_dot.place(relx=0.03, rely=0.5, anchor="center")

        # -----------------------------------------------------------------
        # CÁC THÀNH PHẦN NỘI DUNG CHÍNH (Hiển thị nổi trên nền họa tiết)
        # -----------------------------------------------------------------
        # Lời chào người dùng (Đẩy dịch sang phải một chút để không đè vào chấm cam)
        lbl_welcome = ctk.CTkLabel(
            header, text=f"XIN CHÀO, {self.username.upper()}",
            text_color="#FFFFFF", font=("Arial", 22, "bold"), bg_color="transparent"
        )
        lbl_welcome.pack(side="left", padx=(50, 35), pady=25)

        # Nút ĐĂNG XUẤT thiết kế phẳng, bo góc mềm mại đồng bộ
        btn_logout = ctk.CTkButton(
            header, text="ĐĂNG XUẤT", fg_color="#E74C3C", hover_color="#C0392B",
            text_color="#FFFFFF", font=("Arial", 11, "bold"), height=38, width=120,
            corner_radius=8, command=self.on_logout
        )
        btn_logout.pack(side="right", padx=40, pady=25)

        # ==========================================
        # --- THÂN TRANG (BODY CONTAINER) ---
        # ==========================================
        container = ctk.CTkFrame(self.root, fg_color="transparent")
        container.pack(expand=True, fill="both", padx=50, pady=40)

        # Tiêu đề bảng điều khiển trung tâm
        title_label = ctk.CTkLabel(
            container, text="BẢNG ĐIỀU KHIỂN HỆ THỐNG",
            font=("Arial", 24, "bold"), text_color="#2B323F"
        )
        title_label.pack(pady=(10, 40))

        # Khung chứa các thẻ Menu
        card_frame = ctk.CTkFrame(container, fg_color="transparent")
        card_frame.pack(expand=True)

        # Tông màu xanh đen chủ đạo thống nhất của hệ thống
        main_color = "#2B323F"

        # --- Card 1: Phân hệ Kho Hàng ---
        self.create_menu_card(
            card_frame,
            "QUẢN LÝ KHO HÀNG",
            "Hệ thống quản lý xuất nhập tồn,\ntối ưu hóa kho hàng giày 4S.",
            "👟",  # Icon đại diện cho Giày thể thao
            main_color,
            self.on_go_to_products
        )

        # --- Card 2: Phân hệ Quản Lý Tài Khoản (Đặc quyền của Admin - Quyền "2") ---
        if str(self.role) == "2":
            self.create_menu_card(
                card_frame,
                "QUẢN LÝ TÀI KHOẢN",
                "Quản lý nhân viên, phân quyền\nvà bảo mật hệ thống toàn diện.",
                "👥",  # Icon đại diện cho Nhân viên/Tài khoản
                main_color,
                self.on_go_to_accounts
            )

    def create_menu_card(self, parent, title, desc, icon, color, command):
        """Khởi tạo một thẻ menu (Card) bo góc kèm họa tiết hình khối phẳng nghệ thuật"""
        card = ctk.CTkFrame(
            parent, fg_color="#FFFFFF", border_color="#E2E8F0",
            border_width=1, width=320, height=390, corner_radius=16
        )
        card.pack(side="left", padx=25)
        card.pack_propagate(False)

        # Khối tròn mờ ở góc dưới bên trái của thẻ để tạo chiều sâu UX
        bg_shape = ctk.CTkFrame(card, fg_color="#F8F9FA", width=140, height=140, corner_radius=70)
        bg_shape.place(relx=-0.1, rely=0.9, anchor="center")

        # Chấm cam Pastel làm điểm nhấn thương hiệu nhỏ nhắn
        bg_dot = ctk.CTkFrame(card, fg_color="#E67E22", width=8, height=8, corner_radius=4)
        brand_dot = ctk.CTkFrame(card, fg_color="#E67E22", width=8, height=8, corner_radius=4)
        bg_dot.place(relx=0.85, rely=0.15, anchor="center")

        # Thanh màu sắc nét trang trí trên đỉnh đầu thẻ
        top_stripe = ctk.CTkFrame(card, fg_color=color, height=8, corner_radius=0)
        top_stripe.pack(fill="x", side="top")

        # Tiêu đề của thẻ tính năng
        lbl_card_title = ctk.CTkLabel(
            card, text=title, font=("Arial", 16, "bold"), text_color=color, bg_color="transparent"
        )
        lbl_card_title.pack(pady=(35, 10))

        # Khối Icon lớn trực quan nằm ở trung tâm Card giúp giao diện bớt trống trải
        lbl_icon = ctk.CTkLabel(
            card, text=icon, font=("Arial", 48), text_color=color, bg_color="transparent"
        )
        lbl_icon.pack(pady=(10, 10))

        # Dòng văn bản mô tả ngắn gọn nhiệm vụ phân hệ
        lbl_card_desc = ctk.CTkLabel(
            card, text=desc, font=("Arial", 12), text_color="#7F8C8D",
            justify="center", bg_color="transparent"
        )
        lbl_card_desc.pack(pady=(10, 20), padx=20)

        # Nút hành động "TRUY CẬP NGAY" bo góc và đổi hiệu ứng hover cực mượt
        btn_action = ctk.CTkButton(
            card, text="TRUY CẬP NGAY", fg_color=color, hover_color="#1E242F",
            text_color="#FFFFFF", font=("Arial", 12, "bold"), width=180, height=42,
            corner_radius=10, command=command
        )
        btn_action.pack(side="bottom", pady=30)