import tkinter as tk
from tkinter import messagebox
import csv
import os


class ForgotPasswordUI:
    def __init__(self, root, on_back):
        self.root = root
        self.on_back = on_back
        self.file_path = "accounts.csv"
        self.setup_ui()

    def setup_ui(self):
        self.root.configure(bg="#F0F2F5")

        frame = tk.Frame(self.root, bg="white", padx=40, pady=30, bd=1, relief="solid")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=420, height=550)

        tk.Label(frame, text="KHÔI PHỤC MẬT KHẨU", font=("Arial Bold", 18), bg="white", fg="#e67e22").pack(pady=(0, 20))

        self.entries = {}
        fields = [
            ("Tên đăng nhập", "username", ""),
            ("Email đã đăng ký", "email", ""),
            ("Mật khẩu mới", "new_password", "*"),
            ("Xác nhận mật khẩu mới", "confirm_password", "*")
        ]

        for label_text, key, show_char in fields:
            tk.Label(frame, text=label_text, bg="white", font=("Arial Bold", 9)).pack(anchor="w", pady=(5, 0))
            ent = tk.Entry(frame, font=("Arial", 11), bd=1, relief="solid", show=show_char)
            ent.pack(fill="x", pady=5, ipady=5)
            self.entries[key] = ent

        tk.Button(frame, text="ĐỔI MẬT KHẨU", bg="#e67e22", fg="white", font=("Arial Bold", 11),
                  cursor="hand2", command=self.handle_reset).pack(fill="x", pady=(25, 10), ipady=7)

        tk.Button(frame, text="Quay lại đăng nhập", bg="white", fg="#3498db", bd=0,
                  font=("Arial", 10, "underline"), cursor="hand2", command=self.on_back).pack()

    def handle_reset(self):
        u = self.entries["username"].get().strip()
        e = self.entries["email"].get().strip()
        p1 = self.entries["new_password"].get().strip()
        p2 = self.entries["confirm_password"].get().strip()

        if not all([u, e, p1, p2]):
            messagebox.showwarning("Thông báo", "Vui lòng nhập đầy đủ thông tin!")
            return

        if p1 != p2:
            messagebox.showerror("Lỗi", "Mật khẩu xác nhận không khớp!")
            return

        if not os.path.exists(self.file_path):
            messagebox.showerror("Lỗi", "Hệ thống chưa có dữ liệu tài khoản!")
            return

        updated_data = []
        found = False

        try:
            with open(self.file_path, mode="r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                fieldnames = reader.fieldnames
                for row in reader:
                    if row['username'] == u and row['email'] == e:
                        row['password'] = p1
                        found = True
                    updated_data.append(row)

            if found:
                with open(self.file_path, mode="w", encoding="utf-8-sig", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(updated_data)

                messagebox.showinfo("Thành công", "Mật khẩu đã được thay đổi thành công!")
                self.on_back()
            else:
                messagebox.showerror("Lỗi", "Thông tin Tên đăng nhập hoặc Email không chính xác!")

        except Exception as ex:
            messagebox.showerror("Lỗi", f"Không thể xử lý: {ex}")