import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import os
import pandas as pd
import numpy as np  # BẮT BUỘC: Thư viện tính toán lõi theo yêu cầu GV


class StatManagerApp:
    def __init__(self, master, db_orders, db_products):
        self.master = master
        self.db_orders = db_orders
        self.db_products = db_products

        self.setup_styles()
        self.setup_ui()
        self.update_stats()

    def setup_styles(self):
        """Cấu hình phong cách bảng Treeview sọc hiện đại"""
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Stat.Treeview.Heading",
            background="#FFFFFF",
            foreground="#2B323F",
            font=("Arial", 11, "bold"),
            relief="flat"
        )
        style.configure(
            "Stat.Treeview",
            background="#FFFFFF",
            foreground="#2B323F",
            fieldbackground="#FFFFFF",
            font=("Arial", 10),
            rowheight=35
        )
        style.map("Stat.Treeview", background=[("selected", "#BCD2EE")])

    def setup_ui(self):
        # Thiết lập nền tổng thể
        self.master.configure(fg_color="#F8F9FA")

        # Khung chính
        main_frame = ctk.CTkFrame(self.master, fg_color="#FFFFFF", corner_radius=16, border_color="#E2E8F0",
                                  border_width=1)
        main_frame.pack(expand=True, fill="both", padx=30, pady=20)

        # Tiêu đề lớn
        ctk.CTkLabel(main_frame, text="BÁO CÁO KẾT QUẢ KINH DOANH (NUMPY ENGINE)",
                     font=("Arial", 18, "bold"), text_color="#2B323F").pack(pady=(20, 10))

        # ==========================================
        # --- KHỐI CHỈ SỐ KPI (SỬ DỤNG CARD) ---
        # ==========================================
        metric_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        metric_frame.pack(fill="x", padx=30, pady=10)
        metric_frame.columnconfigure((0, 1, 2), weight=1)

        # Card 1: Tổng Doanh Thu
        self.lbl_revenue = self.create_kpi_card(metric_frame, "TỔNG DOANH THU", "0 VNĐ", 0, "#E8F1F5", "#2A6F97")
        # Card 2: Giá trị Trung Bình (Dùng Numpy tính)
        self.lbl_avg = self.create_kpi_card(metric_frame, "GIÁ TRỊ TB ĐƠN", "0 VNĐ", 1, "#E8F8F5", "#1E8449")
        # Card 3: Tổng Tồn Kho
        self.lbl_inventory = self.create_kpi_card(metric_frame, "TỒN KHO HỆ THỐNG", "0 Đôi", 2, "#FEF5E7", "#B35416")

        # ==========================================
        # --- BẢNG CHI TIẾT DOANH THU THEO THÁNG ---
        # ==========================================
        table_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        table_frame.pack(expand=True, fill="both", padx=30, pady=15)

        self.tree_stat = ttk.Treeview(
            table_frame,
            columns=("month", "status", "total"),
            show="headings",
            style="Stat.Treeview"
        )
        self.tree_stat.heading("month", text="THỜI GIAN")
        self.tree_stat.heading("status", text="TRẠNG THÁI")
        self.tree_stat.heading("total", text="DOANH THU (VNĐ)")

        for col in ("month", "status", "total"):
            self.tree_stat.column(col, anchor="center", width=150)

        self.tree_stat.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree_stat.yview)
        self.tree_stat.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Nút cập nhật
        btn_update = ctk.CTkButton(
            main_frame, text="🔄 CẬP NHẬT DỮ LIỆU HỆ THỐNG", fg_color="#2B323F", hover_color="#1E242F",
            text_color="white", font=("Arial", 11, "bold"), height=40, corner_radius=8,
            command=self.update_stats
        )
        btn_update.pack(pady=(0, 20))

    def create_kpi_card(self, parent, title, value, col, bg_color, txt_color):
        card = ctk.CTkFrame(parent, fg_color=bg_color, corner_radius=12, height=100)
        card.grid(row=0, column=col, padx=10, sticky="nsew")
        card.pack_propagate(False)

        ctk.CTkLabel(card, text=title, font=("Arial", 11, "bold"), text_color="#7F8C8D").pack(pady=(15, 2))
        lbl = ctk.CTkLabel(card, text=value, font=("Arial", 18, "bold"), text_color=txt_color)
        lbl.pack(pady=2)
        return lbl

    def update_stats(self):
        """Hàm xử lý dữ liệu chính: Kết hợp Pandas lọc và Numpy tính toán"""
        # Xóa bảng cũ
        for i in self.tree_stat.get_children(): self.tree_stat.delete(i)

        if not os.path.exists(self.db_orders) or os.stat(self.db_orders).st_size == 0:
            return

        try:
            # 1. Đọc dữ liệu bằng Pandas
            df = pd.read_csv(self.db_orders)

            # Tiền xử lý dữ liệu (Xóa dấu phẩy, chuyển về số)
            df['tong_tien'] = pd.to_numeric(df['tong_tien'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)

            # --- SỬ DỤNG THƯ VIỆN NUMPY ĐỂ TÍNH TOÁN (Yêu cầu GV) ---
            # Chuyển cột dữ liệu thành mảng Numpy để tính toán hiệu năng cao
            revenue_array = df['tong_tien'].to_numpy()

            total_rev = np.sum(revenue_array)  # Tính tổng bằng Numpy
            avg_order = np.mean(revenue_array) if len(revenue_array) > 0 else 0  # Tính trung bình bằng Numpy
            # -------------------------------------------------------

            # Hiển thị lên KPI Cards
            self.lbl_revenue.configure(text=f"{int(total_rev):,} VNĐ")
            self.lbl_avg.configure(text=f"{int(avg_order):,} VNĐ")

            # 2. Cập nhật bảng doanh thu hàng tháng bằng Pandas Groupby
            monthly_rev = df.groupby('thang')['tong_tien'].sum().to_dict()
            for i in range(1, 13):
                m_name = f"Tháng {i}"
                val = monthly_rev.get(m_name, 0)
                tag = "even" if i % 2 == 0 else "odd"
                self.tree_stat.insert("", "end", values=(m_name, "Ổn định", f"{int(val):,}"), tags=(tag,))

            self.tree_stat.tag_configure("odd", background="#F4F7FC")

            # 3. Tính tồn kho từ file sản phẩm bằng Numpy
            if os.path.exists(self.db_products):
                dfp = pd.read_csv(self.db_products)
                stock_data = pd.to_numeric(dfp['sold'], errors='coerce').fillna(0).to_numpy()
                total_stock = np.sum(stock_data)  # Tính tổng tồn bằng Numpy
                self.lbl_inventory.configure(text=f"{int(total_stock)} Đôi")

        except Exception as e:
            print(f"Lỗi phân tích dữ liệu: {e}")
            messagebox.showerror("Lỗi Model", f"Không thể tính toán thống kê: {str(e)}")