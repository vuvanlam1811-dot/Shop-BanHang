import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import customtkinter as ctk
import csv
import os
import pandas as pd # Import pandas để xử lý export nhanh chóng

# ==========================================================
# 1. SUB-WINDOW: CỬA SỔ CON ĐỂ THÊM/SỬA SẢN PHẨM
# ==========================================================
class ProductForm(ctk.CTkToplevel):
    def __init__(self, parent, title, callback, initial_data=None):
        super().__init__(parent)
        self.title(title)
        self.geometry("420x550")
        self.resizable(False, False)
        self.callback = callback
        self.initial_data = initial_data

        # Đảm bảo cửa sổ con luôn nằm trên cùng và chặn tương tác cửa sổ chính
        self.grab_set()
        self.setup_ui()

    def setup_ui(self):
        # Tiêu đề cửa sổ
        ctk.CTkLabel(self, text=self.title().upper(), font=("Arial", 16, "bold"), text_color="#2B323F").pack(pady=20)

        self.entries = {}
        # Cấu hình các trường nhập liệu
        fields = [
            ("Tên sản phẩm:", "name"),
            ("Hãng sản xuất:", "brand"),
            ("Kích cỡ (Size):", "size"),
            ("Giá bán (VNĐ):", "price"),
            ("Số lượng tồn:", "sold"),

        ]

        # Danh sách hãng để dùng OptionMenu
        self.brand_list = ["Nike", "Adidas", "Jordan", "Bitis", "Puma", "Vans"]

        for label_text, key in fields:
            frame = ctk.CTkFrame(self, fg_color="transparent")
            frame.pack(fill="x", padx=40, pady=5)

            ctk.CTkLabel(frame, text=label_text, font=("Arial", 12)).pack(anchor="w")

            if key == "brand":
                self.entries[key] = ctk.CTkOptionMenu(frame, values=self.brand_list, width=340, fg_color="#F8F9FA",
                                                      text_color="#2B323F", button_color="#E9ECEF")
                if self.initial_data: self.entries[key].set(self.initial_data[1])
            else:
                self.entries[key] = ctk.CTkEntry(frame, width=340, placeholder_text=f"Nhập {label_text.lower()}...")
                if self.initial_data:
                    # Map dữ liệu cũ vào ô nhập (initial_data là một list/tuple)
                    idx = ["name", "brand", "price", "size", "sold"].index(key)
                    self.entries[key].insert(0, str(self.initial_data[idx]))

            self.entries[key].pack(pady=2)

        # Nút xác nhận
        btn_confirm = ctk.CTkButton(
            self, text="XÁC NHẬN LƯU", font=("Arial", 13, "bold"),
            fg_color="#2B323F", hover_color="#1E242F", height=45,
            command=self.submit
        )
        btn_confirm.pack(pady=30, padx=40, fill="x")

    def submit(self):
        # 1. Thu thập dữ liệu
        data = [
            self.entries["name"].get().strip(),
            self.entries["brand"].get(),
            self.entries["price"].get().strip(),
            self.entries["size"].get().strip(),
            self.entries["sold"].get().strip()
        ]

        # 2. INPUT VALIDATION (Yêu cầu phi chức năng của GV)
        if not data[0] or not data[2] or not data[3] or not data[4]:
            messagebox.showwarning("Dữ liệu trống", "Vui lòng nhập đầy đủ tất cả các trường!")
            return

        try:
            # Kiểm tra kiểu dữ liệu số cho Giá và Số lượng
            float(data[2].replace(',', ''))
            int(data[4])
        except ValueError:
            messagebox.showerror("Sai kiểu dữ liệu", "Giá và Số lượng phải là định dạng số!")
            return

        # 3. Trả dữ liệu về cho App chính và đóng cửa sổ
        self.callback(data)
        self.destroy()


# ==========================================================
# 2. MAIN APP: PHÂN HỆ QUẢN LÝ KHO HÀNG (TAB KHO HÀNG)
# ==========================================================
class ProductManagerApp:
    def __init__(self, root):
        self.root = root
        # Đường dẫn database
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.file_path = os.path.join(base_dir, "database", "sanpham.csv")

        self.setup_styles()
        self.setup_ui()
        self.load_table()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Treeview.Heading", background="#FFFFFF", foreground="#2B323F",
                        font=("Arial", 11, "bold"))
        style.configure("Custom.Treeview", background="#FFFFFF", foreground="#2B323F", rowheight=35, font=("Arial", 10))
        style.map("Custom.Treeview", background=[("selected", "#BCD2EE")])

    def setup_ui(self):
        # Container chính
        container = ctk.CTkFrame(self.root, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=15)

        # --- THANH CÔNG CỤ (TOOLBAR) TRÊN CÙNG ---
        toolbar = ctk.CTkFrame(container, fg_color="#FFFFFF", corner_radius=12, height=60)
        toolbar.pack(fill="x", pady=(0, 15))
        toolbar.pack_propagate(False)

        # Nhóm nút chức năng
        btn_add = ctk.CTkButton(toolbar, text="+ THÊM MỚI", fg_color="#27ae60", hover_color="#219150",
                                width=110, font=("Arial", 11, "bold"), command=self.open_add_window)
        btn_add.pack(side="left", padx=10, pady=12)

        btn_edit = ctk.CTkButton(toolbar, text="📝 SỬA", fg_color="#f39c12", hover_color="#d68910",
                                 width=80, font=("Arial", 11, "bold"), command=self.open_edit_window)
        btn_edit.pack(side="left", padx=5, pady=12)

        btn_delete = ctk.CTkButton(toolbar, text="🗑 XÓA", fg_color="#e74c3c", hover_color="#c0392b",
                                   width=80, font=("Arial", 11, "bold"), command=self.delete_product)
        btn_delete.pack(side="left", padx=5, pady=12)

        # NÚT EXPORT CSV (Yêu cầu cơ bản bổ sung)
        btn_export = ctk.CTkButton(toolbar, text="📤 XUẤT CSV", fg_color="#3498DB", hover_color="#2980B9",
                                   width=100, font=("Arial", 11, "bold"), command=self.export_csv)
        btn_export.pack(side="left", padx=5, pady=12)

        # Ô tìm kiếm bên phải toolbar
        self.ent_search = ctk.CTkEntry(toolbar, placeholder_text="🔍 Tìm tên giày hoặc hãng...", width=250)
        self.ent_search.pack(side="right", padx=15, pady=12)
        self.ent_search.bind("<KeyRelease>", lambda e: self.filter_table())

        # --- BẢNG DỮ LIỆU (TREEVIEW) ---
        table_frame = ctk.CTkFrame(container, fg_color="#FFFFFF", corner_radius=12, border_color="#E2E8F0",
                                   border_width=1)
        table_frame.pack(fill="both", expand=True)

        cols = ("name", "brand", "price", "size", "sold")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", style="Custom.Treeview")

        heads = {"name": "TÊN SẢN PHẨM", "brand": "HÃNG", "price": "GIÁ (VNĐ)", "size": "SIZE", "sold": "TỒN KHO"}
        for col, head in heads.items():
            self.tree.heading(col, text=head)
            self.tree.column(col, anchor="center", width=120)

        self.tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    # ==========================================================
    # 3. LOGIC XỬ LÝ DỮ LIỆU (CONTROLLER)
    # ==========================================================

    def load_table(self):
        """Nạp toàn bộ dữ liệu từ CSV vào bảng"""

        for item in self.tree.get_children(): self.tree.delete(item)
        if not os.path.exists(self.file_path): return

        with open(self.file_path, mode="r", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            next(reader, None)  # Bỏ qua header
            for row in reader:
                if len(row) >= 5:
                    self.tree.insert("", "end", values=row)

    def open_add_window(self):
        """Mở cửa sổ con để thêm mới"""
        ProductForm(self.root, "Thêm sản phẩm mới", self.add_callback)

    def add_callback(self, data):
        """Hàm được gọi sau khi nhấn Lưu ở cửa sổ con Thêm"""
        self.tree.insert("", "end", values=data)
        self.save_to_csv()
        messagebox.showinfo("Thành công", "Đã thêm sản phẩm vào kho!")

    def open_edit_window(self):
        """Mở cửa sổ con để sửa thông tin dòng đang chọn"""
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một sản phẩm trong bảng để sửa!")
            return
        if len(sel) > 1:
            messagebox.showwarning("Cảnh báo", "Hệ thống chỉ hỗ trợ sửa từng sản phẩm một!")
            return

        # Lấy dữ liệu của dòng đang chọn
        data = self.tree.item(sel[0])['values']
        ProductForm(self.root, "Cập nhật sản phẩm", self.edit_callback, initial_data=data)

    def edit_callback(self, data):
        """Hàm được gọi sau khi nhấn Lưu ở cửa sổ con Sửa"""
        sel = self.tree.selection()[0]
        self.tree.item(sel, values=data)
        self.save_to_csv()
        messagebox.showinfo("Thành công", "Đã cập nhật thông tin sản phẩm!")

    def delete_product(self):
        """Xóa sản phẩm"""
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sản phẩm cần xóa!")
            return

        if messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc chắn muốn xóa {len(sel)} sản phẩm đã chọn?"):
            for item in sel:
                self.tree.delete(item)
            self.save_to_csv()
            messagebox.showinfo("Xóa thành công", "Sản phẩm đã được loại bỏ khỏi kho.")


    def save_to_csv(self):
        """Ghi đè dữ liệu từ bảng xuống file CSV (Model Sync)"""
        with open(self.file_path, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "brand", "price", "size", "sold","color"])
            for item in self.tree.get_children():
                writer.writerow(self.tree.item(item, "values"))

    def export_csv(self):
        """Xuất dữ liệu kho hàng ra file CSV tại vị trí người dùng chọn"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile="kho_hang_xuat_ban.csv"
        )
        if file_path:
            try:
                # Đọc dữ liệu hiện tại từ database hệ thống
                df = pd.read_csv(self.file_path)
                # Lưu ra vị trí mới với định dạng chuẩn
                df.to_csv(file_path, index=False, encoding="utf-8-sig")
                messagebox.showinfo("Thành công", f"Dữ liệu kho hàng đã được xuất ra file:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Lỗi Export", f"Không thể xuất dữ liệu: {e}")

    def filter_table(self):
        """Tìm kiếm dữ liệu thời gian thực (Real-time Search)"""
        query = self.ent_search.get().lower()
        # Nạp lại dữ liệu gốc trước khi lọc
        self.load_table()
        if query:
            for item in self.tree.get_children():
                val = self.tree.item(item, "values")
                # Tìm trong Tên (cột 0) hoặc Hãng (cột 1)
                if query not in str(val[0]).lower() and query not in str(val[1]).lower():
                    self.tree.delete(item)