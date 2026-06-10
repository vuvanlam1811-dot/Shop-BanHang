import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import csv
import os


class LoginUI:
    def __init__(self, root, on_login_success, on_go_to_register, on_forgot_password):
        self.root = root
        self.on_login_success = on_login_success
        self.on_go_to_register = on_go_to_register
        self.on_forgot_password = on_forgot_password

        # Đường dẫn database
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.file_path = os.path.join(base_dir, "database", "taikhoan.csv")
        self.setup_ui()

    def setup_ui(self):
        self.root.configure(fg_color="#F2F4F7")

        main_frame = ctk.CTkFrame(self.root, fg_color="#FFFFFF", corner_radius=15, width=850, height=550)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        main_frame.pack_propagate(False)

        # --- BÊN TRÁI: FORM ĐĂNG NHẬP ---
        left_frame = ctk.CTkFrame(main_frame, fg_color="#FFFFFF", corner_radius=0)
        left_frame.pack(side="left", fill="both", expand=True)

        ctk.CTkLabel(
            left_frame,
            text="4S TEAM LOGIN",
            font=("Arial", 28, "bold"),
            text_color="#2B323F"
        ).pack(pady=(60, 10))

        ctk.CTkLabel(
            left_frame,
            text="Hệ thống tự động nhận diện quyền truy cập",
            font=("Arial", 12),
            text_color="#7F8C8D"
        ).pack(pady=(0, 30))

        # --- Ô NHẬP LIỆU ---
        input_width = 300
        self.entry_username = ctk.CTkEntry(
            left_frame,
            placeholder_text="Tên đăng nhập...",
            width=input_width,
            height=45,
            corner_radius=8,
            fg_color="#F8F9FA",
            border_color="#CED4DA",
            text_color="#2B323F"
        )
        self.entry_username.pack(pady=12)

        self.entry_password = ctk.CTkEntry(
            left_frame,
            placeholder_text="Mật khẩu...",
            show="*",
            width=input_width,
            height=45,
            corner_radius=8,
            fg_color="#F8F9FA",
            border_color="#CED4DA",
            text_color="#2B323F"
        )
        self.entry_password.pack(pady=12)

        # --- NÚT ĐĂNG NHẬP ---
        btn_login = ctk.CTkButton(
            left_frame,
            text="ĐĂNG NHẬP",
            font=("Arial", 14, "bold"),
            fg_color="#2B323F",
            hover_color="#1E242F",
            text_color="#FFFFFF",
            width=input_width,
            height=45,
            corner_radius=8,
            command=self.handle_login
        )
        btn_login.pack(pady=(30, 10))

        # --- LIÊN KẾT PHỤ ---
        links_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        links_frame.pack(pady=10)

        ctk.CTkButton(links_frame, text="Đăng ký tài khoản", font=("Arial", 11, "underline"),
                      fg_color="transparent", text_color="#7F8C8D", hover=False, width=120,
                      command=self.on_go_to_register).pack(side="left", padx=5)

        ctk.CTkButton(links_frame, text="Quên mật khẩu?", font=("Arial", 11, "underline"),
                      fg_color="transparent", text_color="#7F8C8D", hover=False, width=110,
                      command=self.on_forgot_password).pack(side="right", padx=5)

        # --- BÊN PHẢI: BANNER ---
        right_frame = ctk.CTkFrame(main_frame, fg_color="#2B323F", corner_radius=15, width=400)
        right_frame.pack(side="right", fill="both", expand=True)
        right_frame.pack_propagate(False)

        # 1. Thêm các khối hình học làm họa tiết nền nghệ thuật (Pastel / Abstract)
        bg_circle1 = ctk.CTkFrame(right_frame, fg_color="#34495E", width=180, height=180, corner_radius=90)
        bg_circle1.place(relx=0.9, rely=0.1, anchor="center")

        bg_circle2 = ctk.CTkFrame(right_frame, fg_color="#1F2A38", width=240, height=240, corner_radius=120)
        bg_circle2.place(relx=0.1, rely=0.8, anchor="center")

        # Khối màu cam nhạt làm điểm nhấn nhỏ đồng bộ tone màu hệ thống cũ
        bg_dot = ctk.CTkFrame(right_frame, fg_color="#E67E22", width=12, height=12, corner_radius=6)
        bg_dot.place(relx=0.25, rely=0.35, anchor="center")

        # 2. Dòng text thương hiệu chính đặt nổi lên trên các họa tiết
        lbl_main_title = ctk.CTkLabel(
            right_frame,
            text="4S TEAM\nManagement",
            font=("Arial", 36, "bold"),
            text_color="#FFFFFF",
            justify="center",
            bg_color="transparent"
        )
        lbl_main_title.place(relx=0.5, rely=0.46, anchor="center")

        # 3. Thêm một câu Slogan nhỏ phía dưới cho đỡ trống trải
        lbl_slogan = ctk.CTkLabel(
            right_frame,
            text="Hệ thống quản lý kho giày thể thao chuyên nghiệp",
            font=("Arial", 12, "italic"),
            text_color="#BDC3C7",
            bg_color="transparent"
        )
        lbl_slogan.place(relx=0.5, rely=0.62, anchor="center")

    def handle_login(self):
        u = self.entry_username.get().strip()
        p = self.entry_password.get().strip()

        if not u or not p:
            messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu!")
            return

        if not os.path.exists(self.file_path):
            messagebox.showerror("Lỗi", "Cơ sở dữ liệu tài khoản không tồn tại!")
            return

        try:
            with open(self.file_path, mode="r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Kiểm tra tên đăng nhập và mật khẩu
                    if row['username'] == u and row['password'] == p:
                        # LẤY QUYỀN TRỰC TIẾP TỪ FILE
                        user_role = row['role']
                        # Thành công: Trả về quyền và tên đăng nhập cho AppManager
                        self.on_login_success(user_role, u)
                        return

                # Nếu chạy hết vòng lặp mà không thấy
                messagebox.showerror("Thất bại", "Tên đăng nhập hoặc mật khẩu không chính xác!")
        except Exception as e:
            messagebox.showerror("Lỗi hệ thống", f"Không thể xử lý dữ liệu:\n{str(e)}")