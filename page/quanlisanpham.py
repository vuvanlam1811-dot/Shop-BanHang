import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os


class ShoeManagerApp:
    def __init__(self, root, on_logout):
        self.root = root
        self.on_logout = on_logout
        self.file_path = "products.csv"

        # Danh sách các hãng giày
        self.brand_list = ["Nike", "Adidas", "Jordan", "Bitis", "Puma", "Vans", "Converse", "New Balance"]

        self.products = self.load_data()
        self.setup_ui()
        self.refresh_table()

    def load_data(self):
        """Đọc dữ liệu từ CSV và xử lý lỗi"""
        data = []
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, mode="r", encoding="utf-8-sig") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        data.append(row)
            except Exception as e:
                print(f"Lỗi đọc file: {e}")

        # Dữ liệu mẫu nếu file trống
        if not data:
            data = [
                {"name": "Nike Air Force 1", "brand": "Nike", "price": "2200000", "size": "42", "sold": "10"},
                {"name": "Adidas Ultraboost", "brand": "Adidas", "price": "3500000", "size": "41", "sold": "5"}
            ]
        return data

    def save_data(self):
        """Lưu dữ liệu xuống CSV"""
        header = ["name", "brand", "price", "size", "sold"]
        with open(self.file_path, mode="w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            writer.writerows(self.products)
        self.update_stats()  # Cập nhật thống kê mỗi khi lưu

    def setup_ui(self):
        # --- HEADER ---
        header_frame = tk.Frame(self.root, bg="#2B323F", height=70)
        header_frame.pack(fill="x")
        tk.Label(header_frame, text="HỆ THỐNG QUẢN LÝ KHO GIÀY 4S TEAM", fg="white", bg="#2B323F",
                 font=("Arial", 18, "bold")).pack(pady=20)

        # --- PANEL TRÁI: NHẬP LIỆU ---
        input_frame = tk.LabelFrame(self.root, text="Thông tin sản phẩm", bg="white", padx=20, pady=10)
        input_frame.place(x=20, y=90, width=350, height=580)

        self.entries = {}

        # Tên giày
        tk.Label(input_frame, text="Tên giày:", bg="white", font=("Arial", 9, "bold")).pack(anchor="w", pady=(5, 0))
        self.entries['name'] = tk.Entry(input_frame, font=("Arial", 10), bd=1, relief="solid")
        self.entries['name'].pack(fill="x", pady=5, ipady=3)

        # Hãng (Combobox)
        tk.Label(input_frame, text="Hãng giày:", bg="white", font=("Arial", 9, "bold")).pack(anchor="w", pady=(5, 0))
        self.entries['brand'] = ttk.Combobox(input_frame, values=self.brand_list, font=("Arial", 10), state="readonly")
        self.entries['brand'].pack(fill="x", pady=5, ipady=3)
        self.entries['brand'].set("Nike")

        # Giá, Size, Đã bán
        for label, key in [("Giá bán (VNĐ):", "price"), ("Kích cỡ (Size):", "size"), ("Số lượng đã bán:", "sold")]:
            tk.Label(input_frame, text=label, bg="white", font=("Arial", 9, "bold")).pack(anchor="w", pady=(5, 0))
            self.entries[key] = tk.Entry(input_frame, font=("Arial", 10), bd=1, relief="solid")
            self.entries[key].pack(fill="x", pady=5, ipady=3)

        # Nhóm nút bấm
        btn_frame = tk.Frame(input_frame, bg="white")
        btn_frame.pack(fill="x", pady=10)

        tk.Button(btn_frame, text="THÊM MỚI", bg="#27ae60", fg="white", font=("Arial Bold", 9),
                  command=self.add_product).pack(fill="x", pady=2)
        tk.Button(btn_frame, text="CẬP NHẬT", bg="#f39c12", fg="white", font=("Arial Bold", 9),
                  command=self.update_product).pack(fill="x", pady=2)
        tk.Button(btn_frame, text="XÓA SẢN PHẨM", bg="#e74c3c", fg="white", font=("Arial Bold", 9),
                  command=self.delete_product).pack(fill="x", pady=2)
        tk.Button(btn_frame, text="LÀM TRỐNG", bg="#bdc3c7", command=self.clear_entries).pack(fill="x", pady=2)

        tk.Button(input_frame, text="ĐĂNG XUẤT", bg="#2B323F", fg="white", font=("Arial Bold", 10),
                  command=self.on_logout).pack(fill="x", pady=20)

        # --- PANEL PHẢI: TÌM KIẾM & BẢNG ---
        # Ô tìm kiếm
        search_frame = tk.Frame(self.root, bg="#F0F2F5")
        search_frame.place(x=390, y=85, width=580, height=40)

        tk.Label(search_frame, text="Tìm kiếm:", bg="#F0F2F5", font=("Arial Bold", 10)).pack(side="left")
        self.search_ent = tk.Entry(search_frame, font=("Arial", 10), bd=1, relief="solid")
        self.search_ent.pack(side="left", padx=10, fill="x", expand=True, ipady=2)
        self.search_ent.bind("<KeyRelease>", lambda e: self.search_product())  # Tìm ngay khi gõ

        tk.Button(search_frame, text="Làm mới bảng", command=self.refresh_table, bg="#3498db", fg="white").pack(
            side="right")

        # Bảng hiển thị (Treeview)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial Bold", 10))

        self.tree = ttk.Treeview(self.root, columns=("name", "brand", "price", "size", "sold"), show="headings")
        for col in ("name", "brand", "price", "size", "sold"):
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, width=100, anchor="center")

        self.tree.place(x=390, y=130, width=580, height=450)
        self.tree.bind("<<TreeviewSelect>>", self.load_to_entries)

        # --- KHU VỰC THỐNG KÊ (DASHBOARD) ---
        self.stats_frame = tk.LabelFrame(self.root, text="Thống kê nhanh", bg="#ecf0f1", padx=10, pady=10)
        self.stats_frame.place(x=390, y=590, width=580, height=80)

        self.lbl_stats = tk.Label(self.stats_frame, text="", bg="#ecf0f1", font=("Arial Bold", 11), fg="#2c3e50")
        self.lbl_stats.pack(fill="both")
        self.update_stats()

    def validate(self, data):
        """Kiểm tra dữ liệu nhập vào có hợp lệ không"""
        if not data["name"]:
            messagebox.showwarning("Lỗi", "Tên giày không được để trống!")
            return False
        try:
            # Kiểm tra xem Giá và Đã bán có phải là số không
            float(data["price"])
            int(data["sold"])
        except ValueError:
            messagebox.showerror("Lỗi dữ liệu", "Giá và Số lượng bán phải là số!")
            return False
        return True

    def update_stats(self):
        """Tính toán doanh thu và tổng hàng"""
        total_items = len(self.products)
        total_sold = sum(int(p['sold']) for p in self.products)
        total_revenue = sum(float(p['price']) * int(p['sold']) for p in self.products)

        self.lbl_stats.config(text=f"Tổng số loại giày: {total_items}  |  Đã bán: {total_sold} đôi\n"
                                   f"TỔNG DOANH THU: {total_revenue:,.0f} VNĐ")

    def search_product(self):
        """Lọc dữ liệu trong bảng theo từ khóa"""
        query = self.search_ent.get().lower()
        for i in self.tree.get_children():
            self.tree.delete(i)

        for p in self.products:
            if query in p['name'].lower() or query in p['brand'].lower():
                self.tree.insert("", "end", values=(p['name'], p['brand'], p['price'], p['size'], p['sold']))

    def load_to_entries(self, event):
        selected = self.tree.focus()
        if not selected: return
        values = self.tree.item(selected)['values']

        self.entries['name'].delete(0, tk.END)
        self.entries['name'].insert(0, values[0])
        self.entries['brand'].set(values[1])
        self.entries['price'].delete(0, tk.END)
        self.entries['price'].insert(0, values[2])
        self.entries['size'].delete(0, tk.END)
        self.entries['size'].insert(0, values[3])
        self.entries['sold'].delete(0, tk.END)
        self.entries['sold'].insert(0, values[4])

    def add_product(self):
        new_item = {k: v.get().strip() for k, v in self.entries.items()}
        if self.validate(new_item):
            self.products.append(new_item)
            self.save_data()
            self.refresh_table()
            self.clear_entries()
            messagebox.showinfo("Thành công", "Đã thêm sản phẩm vào kho!")

    def update_product(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Lỗi", "Chọn sản phẩm trong bảng để sửa!")
            return

        new_data = {k: v.get().strip() for k, v in self.entries.items()}
        if self.validate(new_data):
            idx = self.tree.index(selected[0])
            self.products[idx] = new_data
            self.save_data()
            self.refresh_table()
            messagebox.showinfo("Thành công", "Đã cập nhật thông tin!")

    def delete_product(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Lỗi", "Chọn sản phẩm cần xóa!")
            return

        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa sản phẩm này?"):
            idx = self.tree.index(selected[0])
            del self.products[idx]
            self.save_data()
            self.refresh_table()
            self.clear_entries()

    def clear_entries(self):
        for k, v in self.entries.items():
            if k == 'brand':
                v.set(self.brand_list[0])
            else:
                v.delete(0, tk.END)

    def refresh_table(self):
        """Làm mới dữ liệu hiển thị trên Treeview"""
        for i in self.tree.get_children(): self.tree.delete(i)
        for p in self.products:
            self.tree.insert("", "end", values=(p['name'], p['brand'], p['price'], p['size'], p['sold']))
        self.update_stats()