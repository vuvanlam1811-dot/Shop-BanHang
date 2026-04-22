import tkinter as tk
from tkinter import messagebox
import csv
import os


class LoginUI:
    def __init__(self, root, on_login_success, on_go_to_register):
        self.root = root
        self.on_login_success = on_login_success
        self.on_go_to_register = on_go_to_register
        self.file_path = "accounts.csv"
        self.setup_ui()

    def setup_ui(self):
        # Cấu hình giao diện chính
        self.root.configure(bg="#F0F2F5")

        # Frame chính chứa 2 phần trái/phải
        main_frame = tk.Frame(self.root, bg="white")
        main_frame.place(relx=0.5, rely=0.5, anchor="center", width=850, height=550)

        # --- PHẦN BÊN TRÁI: FORM ĐĂNG NHẬP ---
        left_frame = tk.Frame(main_frame, bg="white", width=425)
        left_frame.pack(side="left", fill="both", expand=True)

        tk.Label(left_frame, text="4S TEAM LOGIN", font=("Arial Bold", 24), bg="white", fg="#2B323F").pack(
            pady=(50, 30))

        form_container = tk.Frame(left_frame, bg="white")
        form_container.pack(padx=50, fill="x")

        # Username
        tk.Label(form_container, text="Tên đăng nhập", font=("Arial Bold", 10), bg="white").pack(anchor="w")
        self.entry_username = tk.Entry(form_container, font=("Arial", 12), bd=1, relief="solid", bg="#F9F9F9")
        self.entry_username.pack(fill="x", pady=(5, 15), ipady=8)

        # Password
        tk.Label(form_container, text="Mật khẩu", font=("Arial Bold", 10), bg="white").pack(anchor="w")
        self.entry_password = tk.Entry(form_container, font=("Arial", 12), bd=1, relief="solid", bg="#F9F9F9", show="*")
        self.entry_password.pack(fill="x", pady=(5, 15), ipady=8)

        # Chọn quyền (Role)
        tk.Label(form_container, text="Bạn là:", font=("Arial Bold", 10), bg="white").pack(anchor="w")
        self.role_var = tk.IntVar(value=1)
        radio_frame = tk.Frame(form_container, bg="white")
        radio_frame.pack(fill="x", pady=5)

        tk.Radiobutton(radio_frame, text="Người dùng", variable=self.role_var, value=1, bg="white",
                       font=("Arial", 10)).pack(side="left", padx=(0, 20))
        tk.Radiobutton(radio_frame, text="Quản lý", variable=self.role_var, value=2, bg="white",
                       font=("Arial", 10)).pack(side="left")

        # Nút Đăng nhập
        tk.Button(left_frame, text="ĐĂNG NHẬP", bg="#2B323F", fg="white", font=("Arial Bold", 11),
                  cursor="hand2", command=self.handle_login).pack(pady=(20, 10), padx=50, fill="x", ipady=10)

        # Nút Đăng ký
        tk.Button(left_frame, text="Chưa có tài khoản? Đăng ký ngay", bg="white", fg="#3498db", bd=0,
                  font=("Arial", 10, "underline"), cursor="hand2", command=self.on_go_to_register).pack()

        # --- PHẦN BÊN PHẢI: TRANG TRÍ ---
        right_frame = tk.Frame(main_frame, bg="#2B323F", width=425)
        right_frame.pack(side="right", fill="both", expand=True)

        tk.Label(right_frame, text="4S TEAM\nManagement", font=("Arial Bold", 30), bg="#2B323F", fg="white",
                 justify="center").place(relx=0.5, rely=0.45, anchor="center")
        tk.Label(right_frame, text="Hệ thống quản lý chuyên nghiệp", font=("Arial", 12), bg="#2B323F",
                 fg="#bdc3c7").place(relx=0.5, rely=0.6, anchor="center")

    def handle_login(self):
        """Xử lý logic đăng nhập với file CSV"""
        u_input = self.entry_username.get().strip()
        p_input = self.entry_password.get().strip()
        r_input = str(self.role_var.get())  # "1" hoặc "2"

        if not u_input or not p_input:
            messagebox.showwarning("Thông báo", "Vui lòng nhập đầy đủ thông tin!")
            return

        if not os.path.exists(self.file_path):
            messagebox.showerror("Lỗi", f"Không tìm thấy file {self.file_path}!\nVui lòng đăng ký tài khoản trước.")
            return

        login_success = False
        try:
            with open(self.file_path, mode="r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Kiểm tra username và password
                    if row['username'] == u_input and row['password'] == p_input:
                        # Kiểm tra xem quyền có khớp không
                        if row['role'] == r_input:
                            messagebox.showinfo("Thành công", f"Đăng nhập thành công!\nChào mừng {u_input}.")
                            # Trả về quyền (int) và tên người dùng cho AppManager
                            self.on_login_success(int(row['role']), u_input)
                            login_success = True
                            break
                        else:
                            role_name = "Quản lý" if row['role'] == "2" else "Người dùng"
                            messagebox.showwarning("Lỗi quyền", f"Tài khoản này có quyền là: {role_name}")
                            return

            if not login_success:
                messagebox.showerror("Lỗi", "Sai tên đăng nhập hoặc mật khẩu!")

        except Exception as e:
            messagebox.showerror("Lỗi hệ thống", f"Không thể đọc file CSV: {e}")

# Lưu ý: Cấu trúc file accounts.csv phải có tiêu đề: username,password,email,role