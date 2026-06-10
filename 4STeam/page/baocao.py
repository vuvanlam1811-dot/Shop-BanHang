import tkinter as tk
from tkinter import messagebox, filedialog
import customtkinter as ctk
from datetime import datetime
import os
import pandas as pd

class ReportManagerApp:
    def __init__(self, master, db_orders, db_products, username):
        self.master = master
        self.db_orders = db_orders
        self.db_products = db_products
        self.username = username
        self.setup_ui()

    def setup_ui(self):
        if hasattr(self.master, 'configure'):
            self.master.configure(fg_color="#F8F9FA")

        main_container = ctk.CTkFrame(self.master, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=30, pady=20)

        # --- CONTROL PANEL ---
        ctrl_frame = ctk.CTkFrame(main_container, fg_color="#FFFFFF", corner_radius=12, border_color="#E2E8F0", border_width=1)
        ctrl_frame.pack(fill="x", pady=(0, 15), ipady=5)

        lbl_title = ctk.CTkLabel(ctrl_frame, text="XUẤT PHIẾU BÁO CÁO HỆ THỐNG", font=("Arial", 13, "bold"), text_color="#2B323F")
        lbl_title.pack(side="left", padx=20, pady=15)

        btn_save = ctk.CTkButton(ctrl_frame, text="💾 LƯU FILE (.txt)", fg_color="#27ae60", hover_color="#219653",
                                 text_color="white", font=("Arial", 11, "bold"), height=36, corner_radius=8,
                                 command=self.save_to_file)
        btn_save.pack(side="right", padx=(5, 20), pady=15)

        btn_generate = ctk.CTkButton(ctrl_frame, text="🔄 TẠO BÁO CÁO MỚI", fg_color="#2B323F", hover_color="#1E242F",
                                     text_color="white", font=("Arial", 11, "bold"), height=36, corner_radius=8,
                                     command=self.generate_report)
        btn_generate.pack(side="right", padx=5, pady=15)

        # --- REPORT VIEW (ĐÃ SỬA LỖI TẠI ĐÂY) ---
        self.txt_display = ctk.CTkTextbox(
            main_container,
            font=("Courier New", 12),
            fg_color="#FFFFFF",
            text_color="#2B323F",
            border_color="#E2E8F0",
            border_width=1,
            corner_radius=12
            # ĐÃ XÓA: text_pad=(30, 30) <- Đây là nguyên nhân gây lỗi
        )
        self.txt_display.pack(fill="both", expand=True)

        self.generate_report()

    def generate_report(self):
        self.txt_display.delete("1.0", tk.END)
        total_rev, total_ord, total_stock = 0, 0, 0
        order_details = ""

        if os.path.exists(self.db_orders) and os.stat(self.db_orders).st_size > 0:
            try:
                df_ord = pd.read_csv(self.db_orders)
                df_ord['tong_tien'] = pd.to_numeric(df_ord['tong_tien'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
                total_rev = df_ord['tong_tien'].sum()
                total_ord = len(df_ord)
                recent_orders = df_ord.tail(10)
                for _, r in recent_orders.iterrows():
                    order_details += f" {str(r['ngay']):<10} | {str(r['khach_hang']):<18} | {str(r.get('hang', 'N/A')):<10} | {int(r['tong_tien']):>12,}\n"
            except Exception as e:
                print(f"Lỗi: {e}")

        if os.path.exists(self.db_products) and os.stat(self.db_products).st_size > 0:
            try:
                df_prod = pd.read_csv(self.db_products)
                total_stock = pd.to_numeric(df_prod['sold'], errors='coerce').fillna(0).sum()
            except: pass

        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report_content = f"""
============================================================
              CỬA HÀNG GIÀY THỂ THAO 4S TEAM
============================================================
Ngày lập: {now} | Người lập: {self.username.upper()}

I. TỔNG KẾT:
- DOANH THU:      {int(total_rev):,} VNĐ
- ĐƠN HÀNG:       {total_ord} đơn
- TỒN KHO:        {int(total_stock)} đôi

II. CHI TIẾT 10 GIAO DỊCH GẦN NHẤT:
 {"Ngày":<10} | {"Khách hàng":<18} | {"Hãng":<10} | {"Tiền (VNĐ)":>12}
 {"-"*55}
{order_details}
============================================================
"""
        self.txt_display.insert("1.0", report_content.strip())

    def save_to_file(self):
        content = self.txt_display.get("1.0", tk.END).strip()
        if not content: return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("Thành công", "Đã lưu báo cáo!")