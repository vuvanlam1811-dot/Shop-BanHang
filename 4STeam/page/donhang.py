import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import csv
import os
from datetime import datetime


class OrderManagerApp:
    def __init__(self, master, db_orders, on_update_callback):
        self.master = master
        self.db_orders = db_orders
        self.on_update_callback = on_update_callback
        self.selected_id = None
        self.brand_list = ["Nike", "Adidas", "Jordan", "Bitis", "Puma", "Vans"]
        self.csv_headers = ["id", "thang", "khach_hang", "ngay", "hang", "san_pham", "size", "so_luong", "tong_tien",
                            "trang_thai"]

        self.setup_styles()
        self.setup_ui()
        self.load_data()

    def setup_styles(self):
        """Cấu hình nâng cao cho Treeview Đơn hàng phẳng và đổ sọc màu Pastel"""
        style = ttk.Style()
        style.theme_use("clam")

        # Tiêu đề bảng (Header) trắng sáng, chữ đậm nét, không viền 3D
        style.configure(
            "Order.Treeview.Heading",
            background="#FFFFFF",
            foreground="#2B323F",
            font=("Arial", 11, "bold"),
            relief="flat",
            borderwidth=0
        )
        style.map("Order.Treeview.Heading", background=[("active", "#E9ECEF")])

        # Các hàng dữ liệu cao ráo, chữ căn giữa gọn gàng
        style.configure(
            "Order.Treeview",
            background="#FFFFFF",
            foreground="#2B323F",
            fieldbackground="#FFFFFF",
            font=("Arial", 10),
            rowheight=35,
            relief="flat",
            borderwidth=0
        )
        style.map("Order.Treeview", background=[("selected", "#BCD2EE")], foreground=[("selected", "#000000")])

    def setup_ui(self):
        # Đặt nền tổng thể của tab đơn hàng sang màu xám sáng
        if hasattr(self.master, 'configure'):
            self.master.configure(fg_color="#F8F9FA")

        # Container chính chia không gian chuẩn tỉ lệ, không lo bị đè chữ
        container = ctk.CTkFrame(self.master, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=15)

        # ==========================================
        # --- SIDEBAR TRÁI: FORM ĐƠN HÀNG BO GÓC ---
        # ==========================================
        left = ctk.CTkFrame(container, fg_color="transparent", width=280)
        left.pack(side="left", fill="y", padx=(0, 20))
        left.pack_propagate(False)

        self.in_f = {}

        # 1. Chọn Tháng
        ctk.CTkLabel(left, text="Chọn Tháng:", text_color="#2B323F", font=("Arial", 11, "bold")).pack(anchor="w")
        self.in_f['t'] = ctk.CTkOptionMenu(
            left, values=[f"Tháng {i}" for i in range(1, 13)], height=35, corner_radius=8,
            fg_color="#FFFFFF", button_color="#E9ECEF", text_color="#2B323F", dropdown_fg_color="#FFFFFF",
            dropdown_text_color="#2B323F"
        )
        self.in_f['t'].pack(fill="x", pady=(2, 8))

        # 2. Tên khách hàng
        ctk.CTkLabel(left, text="Tên Khách hàng:", text_color="#2B323F", font=("Arial", 11)).pack(anchor="w")
        self.in_f['kh'] = ctk.CTkEntry(left, height=35, corner_radius=8, fg_color="#FFFFFF", border_color="#CED4DA",
                                       text_color="#2B323F")
        self.in_f['kh'].pack(fill="x", pady=(2, 8))

        # 3. Hãng sản xuất
        ctk.CTkLabel(left, text="Hãng sản xuất:", text_color="#2B323F", font=("Arial", 11)).pack(anchor="w")
        self.in_f['brand'] = ctk.CTkOptionMenu(
            left, values=self.brand_list, height=35, corner_radius=8,
            fg_color="#FFFFFF", button_color="#E9ECEF", text_color="#2B323F", dropdown_fg_color="#FFFFFF",
            dropdown_text_color="#2B323F"
        )
        self.in_f['brand'].pack(fill="x", pady=(2, 8))

        # 4. Tên sản phẩm
        ctk.CTkLabel(left, text="Tên Sản phẩm:", text_color="#2B323F", font=("Arial", 11)).pack(anchor="w")
        self.in_f['sp'] = ctk.CTkEntry(left, height=35, corner_radius=8, fg_color="#FFFFFF", border_color="#CED4DA",
                                       text_color="#2B323F")
        self.in_f['sp'].pack(fill="x", pady=(2, 8))

        # 5. Số lượng & Size giày (Chia đôi dòng nằm song song cho gọn gàng)
        size_qty_frame = ctk.CTkFrame(left, fg_color="transparent")
        size_qty_frame.pack(fill="x", pady=4)

        # Ô nhập Size
        sub_left = ctk.CTkFrame(size_qty_frame, fg_color="transparent")
        sub_left.pack(side="left", fill="x", expand=True, padx=(0, 5))
        ctk.CTkLabel(sub_left, text="Size:", text_color="#2B323F", font=("Arial", 11)).pack(anchor="w")
        self.in_f['size'] = ctk.CTkEntry(sub_left, height=35, corner_radius=8, fg_color="#FFFFFF",
                                         border_color="#CED4DA", text_color="#2B323F")
        self.in_f['size'].pack(fill="x")
        self.in_f['size'].insert(0, "38")  # Giá trị mặc định như code cũ

        # Ô nhập Số lượng
        sub_right = ctk.CTkFrame(size_qty_frame, fg_color="transparent")
        sub_right.pack(side="right", fill="x", expand=True, padx=(5, 0))
        ctk.CTkLabel(sub_right, text="Số lượng:", text_color="#2B323F", font=("Arial", 11)).pack(anchor="w")
        self.in_f['sl'] = ctk.CTkEntry(sub_right, height=35, corner_radius=8, fg_color="#FFFFFF",
                                       border_color="#CED4DA", text_color="#2B323F")
        self.in_f['sl'].pack(fill="x")

        # 6. Thành tiền (VNĐ)
        ctk.CTkLabel(left, text="Thành tiền (VNĐ):", text_color="#2B323F", font=("Arial", 11)).pack(anchor="w",
                                                                                                    pady=(4, 0))
        self.in_f['v'] = ctk.CTkEntry(left, height=35, corner_radius=8, fg_color="#FFFFFF", border_color="#CED4DA",
                                      text_color="#2B323F")
        self.in_f['v'].pack(fill="x", pady=(2, 8))

        # 7. Trạng thái đơn hàng
        ctk.CTkLabel(left, text="Trạng thái:", text_color="#2B323F", font=("Arial", 11)).pack(anchor="w")
        self.in_f['st'] = ctk.CTkOptionMenu(
            left, values=["Chờ xử lý", "Đã thanh toán", "Đã hủy"], height=35, corner_radius=8,
            fg_color="#FFFFFF", button_color="#E9ECEF", text_color="#2B323F", dropdown_fg_color="#FFFFFF",
            dropdown_text_color="#2B323F"
        )
        self.in_f['st'].pack(fill="x", pady=(2, 15))

        # --- NÚT BẤM CHỨC NĂNG PHẲNG MÀU PASTEL DỊU MẮT ---
        btn_frame = ctk.CTkFrame(left, fg_color="transparent")
        btn_frame.pack(fill="x", side="bottom", pady=5)

        btn_add = ctk.CTkButton(
            btn_frame, text="THÊM", fg_color="#81C784", hover_color="#71B774",
            text_color="white", font=("Arial", 11, "bold"), height=38, corner_radius=6,
            width=80, command=self.add
        )
        btn_add.pack(side="left", padx=(0, 4), expand=True, fill="x")

        btn_edit = ctk.CTkButton(
            btn_frame, text="SỬA", fg_color="#4EA8DE", hover_color="#3A96CD",
            text_color="white", font=("Arial", 11, "bold"), height=38, corner_radius=6,
            width=80, command=self.edit
        )
        btn_edit.pack(side="left", padx=2, expand=True, fill="x")

        btn_del = ctk.CTkButton(
            btn_frame, text="XÓA", fg_color="#FF8787", hover_color="#FA5252",
            text_color="white", font=("Arial", 11, "bold"), height=38, corner_radius=6,
            width=80, command=self.delete
        )
        btn_del.pack(side="right", padx=(4, 0), expand=True, fill="x")

        # ==========================================
        # --- BÊN PHẢI: BẢNG LƯỚI ĐƠN HÀNG SỌC ---
        # ==========================================
        right_frame = ctk.CTkFrame(container, fg_color="#FFFFFF", corner_radius=12, border_color="#E2E8F0",
                                   border_width=1)
        right_frame.pack(side="right", fill="both", expand=True)

        table_inner_frame = tk.Frame(right_frame, bg="#FFFFFF")
        table_inner_frame.pack(fill="both", expand=True, padx=2, pady=2)

        # Đồng bộ cấu trúc cột hiển thị
        cols = ("id", "t", "kh", "b", "sp", "sl", "v", "st")
        self.tree = ttk.Treeview(table_inner_frame, columns=cols, show="headings", style="Order.Treeview")

        heads = {
            "id": "ID ĐƠN", "t": "THÁNG", "kh": "KHÁCH HÀNG", "b": "HÃNG",
            "sp": "SẢN PHẨM", "sl": "SL", "v": "TIỀN (VNĐ)", "st": "TRẠNG THÁI"
        }
        for c, h in heads.items():
            self.tree.heading(c, text=h, anchor="center")
            self.tree.column(c, width=80, anchor="center")

        self.tree.column("id", width=130, anchor="center")
        self.tree.column("kh", width=120, anchor="center")
        self.tree.column("sp", width=120, anchor="center")

        scrollbar = ttk.Scrollbar(table_inner_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def load_data(self):
        """Đọc dữ liệu và đổ màu nền xen kẽ sọc Pastel"""
        for i in self.tree.get_children():
            self.tree.delete(i)
        if not os.path.exists(self.db_orders):
            return

        with open(self.db_orders, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for index, r in enumerate(reader):
                tag = "evenrow" if index % 2 == 0 else "oddrow"
                self.tree.insert("", "end", values=(
                    r.get('id', ''),
                    r.get('thang', ''),
                    r.get('khach_hang', ''),
                    r.get('hang', ''),
                    r.get('san_pham', ''),
                    r.get('so_luong', ''),
                    r.get('tong_tien', ''),
                    r.get('trang_thai', '')
                ), tags=(tag,))

        # Thiết lập đổ sọc màu dịu mắt
        self.tree.tag_configure("evenrow", background="#FFFFFF")
        self.tree.tag_configure("oddrow", background="#F4F7FC")

    def on_select(self, e):
        """Khi chọn dòng, điền ngược dữ liệu vào Form nhập chính xác"""
        sel = self.tree.focus()
        if not sel:
            return
        v = self.tree.item(sel)['values']
        if not v:
            return
        self.selected_id = str(v[0])

        self.in_f['t'].set(v[1])

        self.in_f['kh'].delete(0, tk.END)
        self.in_f['kh'].insert(0, v[2])

        self.in_f['brand'].set(v[3])

        self.in_f['sp'].delete(0, tk.END)
        self.in_f['sp'].insert(0, v[4])

        self.in_f['sl'].delete(0, tk.END)
        self.in_f['sl'].insert(0, v[5])

        self.in_f['v'].delete(0, tk.END)
        self.in_f['v'].insert(0, v[6])

        self.in_f['st'].set(v[7])

        # Đọc bổ sung cột Size ẩn từ database nếu có để điền lên Form
        with open(self.db_orders, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for r in reader:
                if str(r['id']) == self.selected_id:
                    self.in_f['size'].delete(0, tk.END)
                    self.in_f['size'].insert(0, r.get('size', '38'))
                    break

    def add(self):
        kh = self.in_f['kh'].get().strip()
        thang = self.in_f['t'].get()
        if not thang or not kh:
            return messagebox.showwarning("Lỗi", "Vui lòng nhập Tháng và Tên khách!")

        row = {
            "id": datetime.now().strftime("%Y%m%d%H%M%S"),
            "thang": thang,
            "khach_hang": kh,
            "ngay": datetime.now().strftime("%d/%m/%Y"),
            "hang": self.in_f['brand'].get(),
            "san_pham": self.in_f['sp'].get().strip(),
            "size": self.in_f['size'].get().strip(),
            "so_luong": self.in_f['sl'].get().strip(),
            "tong_tien": self.in_f['v'].get().strip(),
            "trang_thai": self.in_f['st'].get()
        }

        f_exists = os.path.exists(self.db_orders)
        with open(self.db_orders, "a", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=self.csv_headers)
            if not f_exists or os.stat(self.db_orders).st_size == 0:
                w.writeheader()
            w.writerow(row)

        self.refresh()
        messagebox.showinfo("Thành công", "Đã thêm đơn hàng mới!")

    def edit(self):
        if not self.selected_id:
            return messagebox.showwarning("Lỗi", "Vui lòng chọn đơn hàng cần sửa!")

        rows = []
        with open(self.db_orders, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for r in reader:
                if str(r['id']) == self.selected_id:
                    r.update({
                        "thang": self.in_f['t'].get(),
                        "khach_hang": self.in_f['kh'].get().strip(),
                        "hang": self.in_f['brand'].get(),
                        "san_pham": self.in_f['sp'].get().strip(),
                        "size": self.in_f['size'].get().strip(),
                        "so_luong": self.in_f['sl'].get().strip(),
                        "tong_tien": self.in_f['v'].get().strip(),
                        "trang_thai": self.in_f['st'].get()
                    })
                rows.append(r)

        with open(self.db_orders, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=self.csv_headers)
            w.writeheader()
            w.writerows(rows)

        self.refresh()
        messagebox.showinfo("Thành công", "Đã cập nhật thông tin đơn hàng!")

    def delete(self):
        if not self.selected_id:
            return messagebox.showwarning("Lỗi", "Vui lòng chọn đơn hàng cần xóa!")
        if not messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa đơn hàng này?"):
            return

        rows = []
        with open(self.db_orders, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            rows = [r for r in reader if str(r['id']) != self.selected_id]

        with open(self.db_orders, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=self.csv_headers)
            w.writeheader()
            w.writerows(rows)

        self.selected_id = None
        self.refresh()
        messagebox.showinfo("Thành công", "Đã xóa đơn hàng thành công!")

    def refresh(self):
        self.load_data()
        self.on_update_callback()