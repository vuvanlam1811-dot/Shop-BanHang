import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os


class FootballManagerApp:
    def __init__(self, root, on_logout):
        self.root = root
        self.on_logout = on_logout
        self.file_path = "accounts.csv"
        self.accounts = self.load_data()
        self.setup_ui()
        self.refresh_table()

    def load_data(self):
        """Đọc danh sách tài khoản từ CSV"""
        data = []
        if os.path.exists(self.file_path):
            with open(self.file_path, mode="r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
        return data

    def save_data(self):
        """Lưu danh sách tài khoản vào CSV"""
        header = ["username", "password", "email", "role"]
        with open(self.file_path, mode="w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            writer.writerows(self.accounts)
        self.update_stats()

    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg="#1a252f", height=70)
        header_frame.pack(fill="x")
        tk.Label(header_frame, text="QUẢN TRỊ VIÊN - HỆ THỐNG TÀI KHOẢN", fg="white", bg="#1a252f",
                 font=("Arial", 16, "bold")).pack(pady=20)

        # --- CỘT TRÁI: NHẬP LIỆU ---
        left_frame = tk.LabelFrame(self.root, text="Chi tiết tài khoản", bg="white", padx=20, pady=10)
        left_frame.place(x=20, y=90, width=350, height=580)

        self.entries = {}
        fields = [("Tên đăng nhập:", "username"), ("Mật khẩu:", "password"), ("Email:", "email")]

        for label_text, attr in fields:
            tk.Label(left_frame, text=label_text, bg="white", font=("Arial Bold", 9)).pack(anchor="w", pady=(5, 0))
            # Nếu là mật khẩu, cho phép ẩn/hiện (tùy chọn đơn giản ở đây dùng show)
            show_char = "" if attr != "password" else "*"
            ent = tk.Entry(left_frame, font=("Arial", 10), bd=1, relief="solid", show=show_char)
            ent.pack(fill="x", pady=5, ipady=3)
            self.entries[attr] = ent

        tk.Label(left_frame, text="Quyền truy cập:", bg="white", font=("Arial Bold", 9)).pack(anchor="w", pady=(5, 0))
        self.role_combo = ttk.Combobox(left_frame, values=["1", "2"], state="readonly")
        self.role_combo.set("1")
        self.role_combo.pack(fill="x", pady=5, ipady=3)
        tk.Label(left_frame, text="(1: Người dùng | 2: Quản lý)", font=("Arial Italic", 8), bg="white", fg="grey").pack(
            anchor="w")

        # Nút chức năng
        tk.Button(left_frame, text="THÊM TÀI KHOẢN", bg="#27ae60", fg="white", font=("Arial Bold", 10),
                  command=self.add_account).pack(fill="x", pady=(20, 5))
        tk.Button(left_frame, text="CẬP NHẬT", bg="#f39c12", fg="white", font=("Arial Bold", 10),
                  command=self.update_account).pack(fill="x", pady=5)
        tk.Button(left_frame, text="XÓA TÀI KHOẢN", bg="#e74c3c", fg="white", font=("Arial Bold", 10),
                  command=self.delete_account).pack(fill="x", pady=5)
        tk.Button(left_frame, text="LÀM TRỐNG", bg="#bdc3c7", command=self.clear_entries).pack(fill="x", pady=5)
        tk.Button(left_frame, text="ĐĂNG XUẤT", bg="#1a252f", fg="white", font=("Arial Bold", 10),
                  command=self.on_logout).pack(fill="x", pady=30)

        # --- PANEL PHẢI: TÌM KIẾM & BẢNG ---
        # Tìm kiếm tài khoản
        search_frame = tk.Frame(self.root)
        search_frame.place(x=390, y=90, width=580, height=35)
        tk.Label(search_frame, text="Tìm kiếm:").pack(side="left")
        self.search_ent = tk.Entry(search_frame, font=("Arial", 10), bd=1, relief="solid")
        self.search_ent.pack(side="left", padx=10, fill="x", expand=True, ipady=2)
        self.search_ent.bind("<KeyRelease>", lambda e: self.search_account())

        # Bảng hiển thị
        columns = ("username", "password", "email", "role")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        self.tree.heading("username", text="USERNAME")
        self.tree.heading("password", text="PASSWORD")
        self.tree.heading("email", text="EMAIL")
        self.tree.heading("role", text="ROLE")

        self.tree.column("username", width=120)
        self.tree.column("password", width=100)
        self.tree.column("email", width=180)
        self.tree.column("role", width=60, anchor="center")

        self.tree.place(x=390, y=130, width=580, height=440)
        self.tree.bind("<<TreeviewSelect>>", self.load_to_entries)

        # Thống kê
        self.stats_frame = tk.LabelFrame(self.root, text="Thống kê hệ thống", bg="#f9f9f9")
        self.stats_frame.place(x=390, y=580, width=580, height=90)
        self.lbl_stats = tk.Label(self.stats_frame, text="", bg="#f9f9f9", font=("Arial Bold", 11))
        self.lbl_stats.pack(expand=True)
        self.update_stats()

    def update_stats(self):
        u_count = sum(1 for a in self.accounts if a['role'] == '1')
        a_count = sum(1 for a in self.accounts if a['role'] == '2')
        self.lbl_stats.config(text=f"Tổng số tài khoản: {len(self.accounts)}\n"
                                   f"Người dùng (Role 1): {u_count}  |  Quản lý (Role 2): {a_count}")

    def search_account(self):
        query = self.search_ent.get().lower()
        for i in self.tree.get_children(): self.tree.delete(i)
        for acc in self.accounts:
            if query in acc['username'].lower() or query in acc['email'].lower():
                self.tree.insert("", "end", values=(acc['username'], acc['password'], acc['email'], acc['role']))

    def load_to_entries(self, event):
        selected = self.tree.focus()
        if not selected: return
        values = self.tree.item(selected)['values']

        self.entries["username"].delete(0, tk.END)
        self.entries["username"].insert(0, values[0])
        self.entries["password"].delete(0, tk.END)
        self.entries["password"].insert(0, values[1])
        self.entries["email"].delete(0, tk.END)
        self.entries["email"].insert(0, values[2])
        self.role_combo.set(values[3])

    def validate_data(self, u, p, e):
        if not u or not p or not e:
            messagebox.showwarning("Thông báo", "Vui lòng nhập đầy đủ thông tin!")
            return False
        if "@" not in e:
            messagebox.showwarning("Lỗi email", "Email không hợp lệ!")
            return False
        return True

    def add_account(self):
        u = self.entries["username"].get().strip()
        p = self.entries["password"].get().strip()
        e = self.entries["email"].get().strip()
        r = self.role_combo.get()

        if not self.validate_data(u, p, e): return

        if any(acc['username'] == u for acc in self.accounts):
            messagebox.showerror("Lỗi", "Tên đăng nhập đã tồn tại!")
            return

        self.accounts.append({"username": u, "password": p, "email": e, "role": r})
        self.save_data()
        self.refresh_table()
        self.clear_entries()
        messagebox.showinfo("Thành công", "Đã tạo tài khoản mới!")

    def update_account(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Lỗi", "Hãy chọn tài khoản cần sửa!")
            return

        u = self.entries["username"].get().strip()
        p = self.entries["password"].get().strip()
        e = self.entries["email"].get().strip()
        r = self.role_combo.get()

        if not self.validate_data(u, p, e): return

        idx = self.tree.index(selected[0])
        self.accounts[idx] = {"username": u, "password": p, "email": e, "role": r}
        self.save_data()
        self.refresh_table()
        messagebox.showinfo("Thành công", "Cập nhật thành công!")

    def delete_account(self):
        selected = self.tree.selection()
        if not selected: return

        idx = self.tree.index(selected[0])
        target_user = self.accounts[idx]['username']

        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa tài khoản '{target_user}'?"):
            del self.accounts[idx]
            self.save_data()
            self.refresh_table()
            self.clear_entries()

    def clear_entries(self):
        for ent in self.entries.values(): ent.delete(0, tk.END)
        self.role_combo.set("1")

    def refresh_table(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for acc in self.accounts:
            self.tree.insert("", "end", values=(acc['username'], acc['password'], acc['email'], acc['role']))
        self.update_stats()