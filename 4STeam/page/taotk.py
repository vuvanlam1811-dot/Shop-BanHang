import tkinter as tk
from tkinter import messagebox
import csv
import os
import customtkinter as ctk


class RegisterUI:
    def __init__(self, root, on_back):
        self.root = root
        self.on_back = on_back

        # Thiết lập đường dẫn tuyệt đối ổn định đến database/taikhoan.csv
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        db_dir = os.path.join(os.path.dirname(curr_dir), "database")
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
        self.file_path = os.path.join(db_dir, "taikhoan.csv")

        self.setup_ui()

    def setup_ui(self):
        # Thiết lập màu nền hệ thống sáng sủa, nhã nhặn
        if hasattr(self.root, 'configure'):
            self.root.configure(fg_color="#F8F9FA")
        else:
            self.root.configure(bg="#F8F9FA")

        # Thẻ Card trắng trung tâm bo tròn góc 16px, đổ viền mỏng cao cấp
        frame = ctk.CTkFrame(
            self.root, fg_color="#FFFFFF", border_color="#E2E8F0",
            border_width=1, corner_radius=16, width=420, height=640
        )
        frame.place(relx=0.5, rely=0.5, anchor="center")
        frame.pack_propagate(False)

        # Tiêu đề chữ đậm màu xanh đen chủ đạo của 4S Team
        lbl_title = ctk.CTkLabel(
            frame, text="TẠO TÀI KHOẢN MỚI",
            font=("Arial", 18, "bold"), text_color="#2B323F"
        )
        lbl_title.pack(pady=(30, 15))

        # --- CÁC TRƯỜNG NHẬP LIỆU PHẲNG ---
        self.entries = {}
        fields = [
            ("Tên đăng nhập", "username", ""),
            ("Email", "email", ""),
            ("Mật khẩu", "password", "*"),
            ("Xác nhận mật khẩu", "confirm", "*")
        ]

        for label_text, key, show_char in fields:
            lbl = ctk.CTkLabel(
                frame, text=label_text, text_color="#2B323F",
                font=("Arial", 11, "bold")
            )
            lbl.pack(anchor="w", padx=40, pady=(4, 2))

            if show_char:
                ent = ctk.CTkEntry(
                    frame, font=("Arial", 12), height=38, corner_radius=8,
                    fg_color="#FFFFFF", border_color="#CED4DA", text_color="#2B323F",
                    show=show_char
                )
            else:
                ent = ctk.CTkEntry(
                    frame, font=("Arial", 12), height=38, corner_radius=8,
                    fg_color="#FFFFFF", border_color="#CED4DA", text_color="#2B323F"
                )
            ent.pack(fill="x", padx=40, pady=(0, 4))
            self.entries[key] = ent

        # --- PHẦN CHỌN QUYỀN (ROLE) ĐỔI SANG CTkRadioButton ---
        lbl_role = ctk.CTkLabel(
            frame, text="Đăng ký với quyền:", text_color="#2B323F",
            font=("Arial", 11, "bold")
        )
        lbl_role.pack(anchor="w", padx=40, pady=(10, 4))

        self.role_var = tk.IntVar(value=1)  # Mặc định là Người dùng (1)
        radio_frame = ctk.CTkFrame(frame, fg_color="transparent")
        radio_frame.pack(fill="x", padx=40, pady=(2, 10))

        # Cấu hình RadioButton phẳng, đổi tone vòng chọn sang màu xanh đen thương hiệu
        rb_user = ctk.CTkRadioButton(
            radio_frame, text="Người dùng", variable=self.role_var, value=1,
            font=("Arial", 12), text_color="#2B323F",
            fg_color="#2B323F", hover_color="#1E242F"
        )
        rb_user.pack(side="left", padx=(0, 30))

        rb_manager = ctk.CTkRadioButton(
            radio_frame, text="Quản lý", variable=self.role_var, value=2,
            font=("Arial", 12), text_color="#2B323F",
            fg_color="#2B323F", hover_color="#1E242F"
        )
        rb_manager.pack(side="left")

        # --- CỤM NÚT HÀNH ĐỘNG PHẲNG ---
        # Nút ĐĂNG KÝ chuyển hẳn sang màu xanh đen chủ đạo khỏe khoắn
        btn_register = ctk.CTkButton(
            frame, text="ĐĂNG KÝ NGAY", fg_color="#2B323F", hover_color="#1E242F",
            text_color="#FFFFFF", font=("Arial", 12, "bold"), height=42, corner_radius=8,
            command=self.validate_registration
        )
        btn_register.pack(fill="x", padx=40, pady=(20, 10))

        # Nút điều hướng phụ dạng Text Link phẳng hiện đại, chuyển sang màu nền xám mờ khi hover
        btn_back = ctk.CTkButton(
            frame, text="Đã có tài khoản? Đăng nhập", fg_color="transparent", hover_color="#F1F3F5",
            text_color="#3498DB", font=("Arial", 12), height=32, corner_radius=6,
            command=self.on_back
        )
        btn_back.pack(pady=(0, 15))

    def validate_registration(self):
        """Xử lý nghiệp vụ kiểm tra form và lưu tài khoản mới xuống CSV"""
        u = self.entries["username"].get().strip()
        e = self.entries["email"].get().strip()
        p = self.entries["password"].get().strip()
        c = self.entries["confirm"].get().strip()
        r = str(self.role_var.get())

        # 1. Kiểm tra trường rỗng
        if not all([u, e, p, c]):
            messagebox.showwarning("Thông báo", "Vui lòng điền đầy đủ các thông tin đăng ký!")
            return

        # 2. Kiểm tra khớp mật khẩu
        if p != c:
            messagebox.showerror("Lỗi dữ liệu", "Mật khẩu xác nhận không trùng khớp!")
            return

        # 3. Kiểm tra cấu trúc Email đơn giản
        if "@" not in e:
            messagebox.showerror("Lỗi Email", "Định dạng tài khoản Email không hợp lệ!")
            return

        # 4. Kiểm tra trùng lặp tên đăng nhập trong CSV
        header = ["username", "password", "email", "role"]
        file_exists = os.path.exists(self.file_path)

        if file_exists:
            try:
                with open(self.file_path, mode="r", encoding="utf-8-sig") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if row['username'] == u:
                            messagebox.showerror("Lỗi tài khoản", "Tên đăng nhập này đã tồn tại trên hệ thống!")
                            return
            except Exception as ex:
                print(f"Lỗi đọc file kiểm tra trùng: {ex}")

        # 5. Thực hiện ghi tài khoản mới vào file dữ liệu cứng CSV
        try:
            file_is_empty = not file_exists or os.stat(self.file_path).st_size == 0

            with open(self.file_path, mode="a", encoding="utf-8-sig", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=header)
                if file_is_empty:
                    writer.writeheader()

                writer.writerow({
                    "username": u,
                    "password": p,
                    "email": e,
                    "role": r
                })

            messagebox.showinfo("Thành công",
                                f"Tài khoản {u} đã được khởi tạo thành công với quyền {'Quản lý' if r == '2' else 'Người dùng'}!")
            self.on_back()  # Quay ngược lại màn hình đăng nhập chính

        except Exception as ex:
            messagebox.showerror("Lỗi hệ thống", f"Không thể đồng bộ ghi file tài khoản: {ex}")