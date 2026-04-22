import tkinter as tk
from tkinter import messagebox
import csv
import os


class RegisterUI:
    def __init__(self, root, on_back):
        self.root = root
        self.on_back = on_back
        self.file_path = "accounts.csv"  # Sử dụng chung file với hệ thống
        self.setup_ui()

    def setup_ui(self):
        self.root.configure(bg="#F0F2F5")

        # Frame chính
        frame = tk.Frame(self.root, bg="white", padx=40, pady=30, bd=1, relief="solid")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=420, height=600)

        tk.Label(frame, text="TẠO TÀI KHOẢN MỚI", font=("Arial Bold", 18), bg="white", fg="#2c3e50").pack(pady=(0, 20))

        # --- CÁC TRƯỜNG NHẬP LIỆU ---
        self.entries = {}

        fields = [
            ("Tên đăng nhập", "username", ""),
            ("Email", "email", ""),
            ("Mật khẩu", "password", "*"),
            ("Xác nhận mật khẩu", "confirm", "*")
        ]

        for label_text, key, show_char in fields:
            tk.Label(frame, text=label_text, bg="white", font=("Arial Bold", 9)).pack(anchor="w", pady=(5, 0))
            if show_char:
                ent = tk.Entry(frame, font=("Arial", 11), bd=1, relief="solid", show=show_char)
            else:
                ent = tk.Entry(frame, font=("Arial", 11), bd=1, relief="solid")
            ent.pack(fill="x", pady=5, ipady=5)
            self.entries[key] = ent

        # --- NÚT BẤM ---
        tk.Button(frame, text="ĐĂNG KÝ NGAY", bg="#27ae60", fg="white", font=("Arial Bold", 11),
                  cursor="hand2", command=self.validate_registration).pack(fill="x", pady=(25, 10), ipady=7)

        tk.Button(frame, text="Đã có tài khoản? Đăng nhập", bg="white", fg="#3498db", bd=0,
                  font=("Arial", 10, "underline"), cursor="hand2", command=self.on_back).pack()

    def validate_registration(self):
        # Lấy dữ liệu và xóa khoảng trắng thừa
        u = self.entries["username"].get().strip()
        e = self.entries["email"].get().strip()
        p = self.entries["password"].get().strip()
        c = self.entries["confirm"].get().strip()

        # 1. Kiểm tra để trống
        if not all([u, e, p, c]):
            messagebox.showwarning("Thông báo", "Vui lòng điền đầy đủ các trường!")
            return

        # 2. Kiểm tra định dạng Email đơn giản
        if "@" not in e or "." not in e:
            messagebox.showerror("Lỗi Email", "Email không đúng định dạng (ví dụ: abc@gmail.com)")
            return

        # 3. Kiểm tra khớp mật khẩu
        if p != c:
            messagebox.showerror("Lỗi", "Mật khẩu xác nhận không khớp!")
            return

        # 4. Kiểm tra độ dài mật khẩu (tùy chọn nhưng nên có)
        if len(p) < 6:
            messagebox.showwarning("Bảo mật", "Mật khẩu nên có ít nhất 6 ký tự!")
            return

        # 5. Kiểm tra trùng tên đăng nhập trong file CSV
        header = ["username", "password", "email", "role"]
        if os.path.exists(self.file_path):
            with open(self.file_path, mode="r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['username'] == u:
                        messagebox.showerror("Lỗi", "Tên đăng nhập này đã có người sử dụng!")
                        return

        # 6. Ghi vào file CSV
        # Kiểm tra file có nội dung chưa để ghi header
        file_is_empty = not os.path.exists(self.file_path) or os.stat(self.file_path).st_size == 0

        try:
            with open(self.file_path, mode="a", encoding="utf-8-sig", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=header)
                if file_is_empty:
                    writer.writeheader()

                # Role mặc định khi đăng ký là "1" (Người dùng)
                writer.writerow({
                    "username": u,
                    "password": p,
                    "email": e,
                    "role": "1"
                })

            messagebox.showinfo("Thành công", f"Chúc mừng {u}!\nTài khoản của bạn đã được tạo.")
            self.on_back()  # Quay lại màn hình đăng nhập

        except Exception as ex:
            messagebox.showerror("Lỗi hệ thống", f"Không thể lưu tài khoản: {ex}")