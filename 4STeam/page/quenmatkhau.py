import tkinter as tk
from tkinter import messagebox
import csv
import os
import customtkinter as ctk


class ForgotPasswordUI:
    def __init__(self, root, on_back):
        self.root = root
        self.on_back = on_back

        # Đồng bộ cấu trúc lấy đường dẫn database chuẩn của hệ thống
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(os.path.dirname(curr_dir), "database", "taikhoan.csv")

        self.setup_ui()

    def setup_ui(self):
        # Nền tổng thể đồng bộ màu xám sáng nhã nhặn của hệ thống
        if hasattr(self.root, 'configure'):
            self.root.configure(fg_color="#F8F9FA")
        else:
            self.root.configure(bg="#F8F9FA")

        # Thẻ Card trắng trung tâm bo tròn góc, đổ viền phẳng hiện đại
        frame = ctk.CTkFrame(
            self.root, fg_color="#FFFFFF", border_color="#E2E8F0",
            border_width=1, corner_radius=16, width=420, height=560
        )
        frame.place(relx=0.5, rely=0.5, anchor="center")
        frame.pack_propagate(False)

        # Tiêu đề đổi sang màu xanh đen thương hiệu của 4S Team
        lbl_title = ctk.CTkLabel(
            frame, text="KHÔI PHỤC MẬT KHẨU",
            font=("Arial", 18, "bold"), text_color="#2B323F"
        )
        lbl_title.pack(pady=(35, 20))

        self.entries = {}
        fields = [
            ("Tên đăng nhập", "username", ""),
            ("Email đã đăng ký", "email", ""),
            ("Mật khẩu mới", "new_password", "*"),
            ("Xác nhận mật khẩu mới", "confirm_password", "*")
        ]

        # Khởi tạo các trường nhập liệu phẳng, bo góc 8px đồng bộ
        for label_text, key, show_char in fields:
            lbl = ctk.CTkLabel(
                frame, text=label_text, text_color="#2B323F",
                font=("Arial", 11, "bold")
            )
            lbl.pack(anchor="w", padx=40, pady=(6, 2))

            # Nếu là trường mật khẩu thì bật chế độ ẩn ký tự bằng tham số show
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

        # Nút hành động ĐỔI MẬT KHẨU màu xanh đen, hover chuyển tone xám đậm cực nhạy
        btn_reset = ctk.CTkButton(
            frame, text="ĐỔI MẬT KHẨU", fg_color="#2B323F", hover_color="#1E242F",
            text_color="#FFFFFF", font=("Arial", 12, "bold"), height=42, corner_radius=8,
            command=self.handle_reset
        )
        btn_reset.pack(fill="x", padx=40, pady=(25, 12))

        # Nút "Quay lại đăng nhập" dạng Text Link phẳng hiện đại (loại bỏ gạch chân thô sơ)
        btn_back = ctk.CTkButton(
            frame, text="← Quay lại đăng nhập", fg_color="transparent", hover_color="#F1F3F5",
            text_color="#3498DB", font=("Arial", 12), height=32, corner_radius=6,
            command=self.on_back
        )
        btn_back.pack(pady=(0, 20))

    def handle_reset(self):
        """Xử lý nghiệp vụ kiểm tra thông tin và ghi đè mật khẩu mới vào CSV"""
        u = self.entries["username"].get().strip()
        e = self.entries["email"].get().strip()
        p1 = self.entries["new_password"].get().strip()
        p2 = self.entries["confirm_password"].get().strip()

        if not all([u, e, p1, p2]):
            messagebox.showwarning("Thông báo", "Vui lòng nhập đầy đủ thông tin hệ thống yêu cầu!")
            return

        if p1 != p2:
            messagebox.showerror("Lỗi dữ liệu", "Mật khẩu mới và mật khẩu xác nhận không trùng khớp!")
            return

        if not os.path.exists(self.file_path):
            messagebox.showerror("Lỗi hệ thống", "Tập tin cơ sở dữ liệu tài khoản không tồn tại!")
            return

        updated_data = []
        found = False

        try:
            with open(self.file_path, mode="r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                fieldnames = reader.fieldnames
                for row in reader:
                    # Kiểm tra khớp đồng thời cả tên đăng nhập và email
                    if row['username'] == u and row['email'] == e:
                        row['password'] = p1
                        found = True
                    updated_data.append(row)

            if found:
                with open(self.file_path, mode="w", encoding="utf-8-sig", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(updated_data)

                messagebox.showinfo("Thành công", "Mật khẩu tài khoản của bạn đã được cập nhật!")
                self.on_back()
            else:
                messagebox.showerror("Lỗi xác thực", "Tên đăng nhập hoặc Email không chính xác trên hệ thống!")

        except Exception as ex:
            messagebox.showerror("Lỗi xử lý", f"Không thể đồng bộ dữ liệu: {ex}")