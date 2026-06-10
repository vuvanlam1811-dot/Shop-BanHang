import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import os
import pandas as pd


class SearchManagerApp:
    def __init__(self, master, db_orders):
        self.master = master
        self.db_orders = db_orders
        self.brand_list = ["Tất cả", "Nike", "Adidas", "Jordan", "Bitis", "Puma", "Vans"]

        self.setup_styles()
        self.setup_ui()
        self.search_data()  # Tự động tải toàn bộ dữ liệu khi vừa mở tab

    def setup_styles(self):
        """Cấu hình phong cách bảng tra cứu phẳng và đổ sọc sành điệu"""
        style = ttk.Style()
        style.theme_use("clam")

        # Tiêu đề bảng trắng sáng, chữ đậm nét
        style.configure(
            "Search.Treeview.Heading",
            background="#FFFFFF",
            foreground="#2B323F",
            font=("Arial", 11, "bold"),
            relief="flat",
            borderwidth=0
        )
        style.map("Search.Treeview.Heading", background=[("active", "#E9ECEF")])

        # Hàng dữ liệu cao ráo, thoáng mát
        style.configure(
            "Search.Treeview",
            background="#FFFFFF",
            foreground="#2B323F",
            fieldbackground="#FFFFFF",
            font=("Arial", 10),
            rowheight=35,
            relief="flat",
            borderwidth=0
        )
        style.map("Search.Treeview", background=[("selected", "#BCD2EE")], foreground=[("selected", "#000000")])

    def setup_ui(self):
        # Thiết lập nền tổng thể cho tab tra cứu
        if hasattr(self.master, 'configure'):
            self.master.configure(fg_color="#F8F9FA")

        # Container chính bọc toàn bộ giao diện
        main_container = ctk.CTkFrame(self.master, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=25, pady=20)

        # ==========================================
        # --- THANH BỘ LỌC TÌM KIẾM (FILTER CONTROL) ---
        # ==========================================
        filter_frame = ctk.CTkFrame(main_container, fg_color="#FFFFFF", corner_radius=12, border_color="#E2E8F0",
                                    border_width=1)
        filter_frame.pack(fill="x", pady=(0, 15))

        # Cấu hình các cột trong Grid để căn đều khoảng cách
        filter_frame.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)

        # 1. Bộ lọc Tháng
        lbl_month = ctk.CTkLabel(filter_frame, text="Tháng:", text_color="#2B323F", font=("Arial", 11, "bold"))
        lbl_month.grid(row=0, column=0, padx=(20, 5), pady=15, sticky="e")
        self.cb_month = ctk.CTkOptionMenu(
            filter_frame, values=["Tất cả"] + [f"Tháng {i}" for i in range(1, 13)], height=35, corner_radius=8,
            fg_color="#FFFFFF", button_color="#E9ECEF", text_color="#2B323F", dropdown_fg_color="#FFFFFF",
            dropdown_text_color="#2B323F"
        )
        self.cb_month.set("Tất cả")
        self.cb_month.grid(row=0, column=1, padx=5, pady=15, sticky="w")

        # 2. Bộ lọc Hãng
        lbl_brand = ctk.CTkLabel(filter_frame, text="Hãng:", text_color="#2B323F", font=("Arial", 11, "bold"))
        lbl_brand.grid(row=0, column=2, padx=(15, 5), pady=15, sticky="e")
        self.cb_brand = ctk.CTkOptionMenu(
            filter_frame, values=self.brand_list, height=35, corner_radius=8,
            fg_color="#FFFFFF", button_color="#E9ECEF", text_color="#2B323F", dropdown_fg_color="#FFFFFF",
            dropdown_text_color="#2B323F"
        )
        self.cb_brand.set("Tất cả")
        self.cb_brand.grid(row=0, column=3, padx=5, pady=15, sticky="w")

        # 3. Tìm theo Tên Khách Hàng
        lbl_name = ctk.CTkLabel(filter_frame, text="Tên khách:", text_color="#2B323F", font=("Arial", 11, "bold"))
        lbl_name.grid(row=0, column=4, padx=(15, 5), pady=15, sticky="e")
        self.ent_name = ctk.CTkEntry(
            filter_frame, placeholder_text="Nhập tên cần tìm...", height=35, corner_radius=8,
            fg_color="#FFFFFF", border_color="#CED4DA", text_color="#2B323F"
        )
        self.ent_name.grid(row=0, column=5, padx=5, pady=15, sticky="we")

        # 4. Nút bấm tìm kiếm phẳng màu xanh đen
        btn_search = ctk.CTkButton(
            filter_frame, text="🔍 TÌM KIẾM", fg_color="#2B323F", hover_color="#1E242F",
            text_color="white", font=("Arial", 11, "bold"), height=35, corner_radius=8,
            command=self.search_data
        )
        btn_search.grid(row=0, column=6, padx=(20, 20), pady=15, sticky="e")

        # ==========================================
        # --- BẢNG HIỂN THỊ KẾT QUẢ ĐỔ SỌC PASTEL ---
        # ==========================================
        table_border_frame = ctk.CTkFrame(main_container, fg_color="#FFFFFF", corner_radius=12, border_color="#E2E8F0",
                                          border_width=1)
        table_border_frame.pack(fill="both", expand=True)

        table_inner_frame = tk.Frame(table_border_frame, bg="#FFFFFF")
        table_inner_frame.pack(fill="both", expand=True, padx=2, pady=2)

        columns = ("id", "date", "kh", "brand", "sp", "v", "st")
        self.tree = ttk.Treeview(table_inner_frame, columns=columns, show="headings", style="Search.Treeview")

        heads = {
            "id": "MÃ ĐƠN", "date": "NGÀY", "kh": "KHÁCH HÀNG",
            "brand": "HÃNG", "sp": "SẢN PHẨM", "v": "SỐ TIỀN (VNĐ)", "st": "TRẠNG THÁI"
        }

        for col, head in heads.items():
            self.tree.heading(col, text=head, anchor="center")
            self.tree.column(col, anchor="center", width=100)

        # Căn chỉnh riêng độ rộng một số cột quan trọng cho thoáng chữ
        self.tree.column("id", width=130)
        self.tree.column("kh", width=140)
        self.tree.column("sp", width=140)

        scrollbar = ttk.Scrollbar(table_inner_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # ==========================================
        # --- THANH TỔNG HỢP (SUMMARY FOOTER) ---
        # ==========================================
        self.lbl_summary = ctk.CTkLabel(
            main_container, text="Tìm thấy: 0 đơn | Tổng cộng: 0 VNĐ",
            font=("Arial", 12, "bold"), text_color="#2B323F"
        )
        self.lbl_summary.pack(pady=(10, 0), anchor="e", padx=5)

    def search_data(self):
        """Thực hiện lọc thông minh bằng bộ lọc đa điều kiện của Pandas"""
        month_val = self.cb_month.get()
        brand_val = self.cb_brand.get()
        name_val = self.ent_name.get().strip().lower()

        # Xóa sạch các hàng cũ trước khi nạp kết quả mới
        for i in self.tree.get_children():
            self.tree.delete(i)

        if not os.path.exists(self.db_orders) or os.stat(self.db_orders).st_size == 0:
            self.lbl_summary.configure(text="Tìm thấy: 0 đơn | Tổng cộng: 0 VNĐ")
            return

        try:
            # 1. Đọc dữ liệu từ file database
            df = pd.read_csv(self.db_orders)
            df['tong_tien'] = pd.to_numeric(df['tong_tien'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)

            # 2. Tạo mặt nạ lọc đa điều kiện
            mask = pd.Series([True] * len(df))

            if month_val != "Tất cả":
                mask &= (df['thang'] == month_val)
            if brand_val != "Tất cả":
                mask &= (df['hang'] == brand_val)
            if name_val:
                mask &= (df['khach_hang'].str.lower().str.contains(name_val, na=False))

            filtered_df = df[mask]

            # 3. Đổ dữ liệu lên lưới đồ họa kèm thẻ sọc màu Pastel
            for index, (_, r) in enumerate(filtered_df.iterrows()):
                tag = "evenrow" if index % 2 == 0 else "oddrow"
                self.tree.insert("", "end", values=(
                    r['id'], r['ngay'], r['khach_hang'],
                    r.get('hang', 'N/A'), r['san_pham'], f"{int(r['tong_tien']):,}", r['trang_thai']
                ), tags=(tag,))

            # Cấu hình màu nền xen kẽ dịu mắt
            self.tree.tag_configure("evenrow", background="#FFFFFF")
            self.tree.tag_configure("oddrow", background="#F4F7FC")

            # Cập nhật thanh trạng thái tổng hợp dưới chân trang
            total_money = int(filtered_df['tong_tien'].sum())
            self.lbl_summary.configure(
                text=f"Tìm thấy: {len(filtered_df)} đơn | Tổng cộng: {total_money:,} VNĐ"
            )
        except Exception as e:
            print(f"Lỗi tra cứu dữ liệu: {e}")