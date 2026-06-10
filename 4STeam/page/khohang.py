import os
import csv
import threading
import webbrowser
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import customtkinter as ctk
import pandas as pd

# Import các phân hệ con
from .quanlisanpham import ProductManagerApp
from .thongke import StatManagerApp
from .donhang import OrderManagerApp
from .tracuu import SearchManagerApp
from .baocao import ReportManagerApp
from .quanlitaikhoan import AccountManagerApp


class MainShell:
    def __init__(self, root, username, role, on_back, start_tab=0):
        self.root = root
        self.username = username
        self.role = role
        self.on_back = on_back
        self.start_tab = start_tab

        # Đường dẫn cơ sở dữ liệu
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(curr_dir)
        self.db_orders = os.path.join(root_dir, "database", "donhang.csv")
        self.db_products = os.path.join(root_dir, "database", "sanpham.csv")

        self.fieldnames = ["id", "thang", "khach_hang", "ngay", "hang", "san_pham", "size", "so_luong", "tong_tien",
                           "trang_thai"]

        self.init_database()
        self.setup_ui()

    def init_database(self):
        os.makedirs(os.path.dirname(self.db_orders), exist_ok=True)
        if not os.path.exists(self.db_orders) or os.stat(self.db_orders).st_size == 0:
            with open(self.db_orders, "w", encoding="utf-8-sig", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()

    def setup_ui(self):
        # Thiết lập nền tổng thể (Hỗ trợ Auto-resize)
        self.root.configure(fg_color="#F8F9FA")

        # =================================================================
        # --- HEADER BANNER NGHỆ THUẬT (CÓ THÊM TOOLBAR NÂNG CAO) ---
        # =================================================================
        header = ctk.CTkFrame(self.root, fg_color="#2B323F", height=90, corner_radius=0)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        # Họa tiết trang trí (giữ nguyên phong cách của bạn)
        circle_top_right = ctk.CTkFrame(header, fg_color="#343A40", width=130, height=130, corner_radius=65)
        circle_top_right.place(relx=0.88, rely=-0.3, anchor="center")

        brand_dot = ctk.CTkFrame(header, fg_color="#E67E22", width=10, height=10, corner_radius=5)
        brand_dot.place(relx=0.025, rely=0.5, anchor="center")

        title_label = ctk.CTkLabel(header, text="4S TEAM SYSTEM", text_color="#FFFFFF", font=("Arial", 20, "bold"))
        title_label.place(relx=0.04, rely=0.5, anchor="w")

        # --- NHÓM NÚT ĐIỀU HƯỚNG VÀ CÔNG CỤ (BÊN PHẢI) ---
        btn_txt = "QUAY LẠI" if str(self.role) == "2" else "ĐĂNG XUẤT"

        # Nút Quay lại / Đăng xuất
        btn_back = ctk.CTkButton(header, text=f"➔ {btn_txt}", fg_color="#F38B7F", hover_color="#E07A6E",
                                 text_color="#FFFFFF", font=("Arial", 11, "bold"), corner_radius=18,
                                 height=36, width=110, command=self.on_back)
        btn_back.pack(side="right", padx=20, pady=27)

        # Nút Hướng dẫn (Mở file PDF) - YÊU CẦU NÂNG CAO
        btn_manual = ctk.CTkButton(header, text="📖 Hướng dẫn", fg_color="#5D6D7E", hover_color="#46515E",
                                   text_color="#FFFFFF", font=("Arial", 11, "bold"), corner_radius=18,
                                   height=36, width=110, command=self.open_pdf)
        btn_manual.pack(side="right", padx=10, pady=27)

        # Nút About - YÊU CẦU CƠ BẢN
        btn_about = ctk.CTkButton(header, text="ℹ About", fg_color="#5D6D7E", hover_color="#46515E",
                                  text_color="#FFFFFF", font=("Arial", 11, "bold"), corner_radius=18,
                                  height=36, width=90, command=self.show_about)
        btn_about.pack(side="right", padx=10, pady=27)

        # Nút Import CSV - YÊU CẦU CƠ BẢN (Xử lý Threading nâng cao)
        btn_import = ctk.CTkButton(header, text="📥 Import Kho", fg_color="#27ae60", hover_color="#219150",
                                   text_color="#FFFFFF", font=("Arial", 11, "bold"), corner_radius=18,
                                   height=36, width=110, command=self.import_data)
        btn_import.pack(side="right", padx=10, pady=27)

        # =================================================================
        # --- KHU VỰC TAB CONTROL (QUẢN LÝ CHỨC NĂNG) ---
        # =================================================================
        self.tab_control = ctk.CTkTabview(
            self.root, fg_color="#F8F9FA", segmented_button_fg_color="#E9ECEF",
            segmented_button_selected_color="#BCD2EE", text_color="#2B323F"
        )
        self.tab_control.pack(fill="both", expand=True, padx=20, pady=(10, 15))

        # Định nghĩa các trang chức năng
        names = ["Kho hàng", "Thống kê", "Đơn hàng", "Tra cứu", "Báo cáo"]
        for name in names:
            self.tab_control.add(name)

        self.tabs = [self.tab_control.tab(name) for name in names]

        # Khởi tạo các module con (Controller kết nối View và Model)
        self.app1 = ProductManagerApp(self.tabs[0])
        self.app2 = StatManagerApp(self.tabs[1], self.db_orders, self.db_products)
        self.app3 = OrderManagerApp(self.tabs[2], self.db_orders, self.app2.update_stats)
        self.app4 = SearchManagerApp(self.tabs[3], self.db_orders)
        self.app5 = ReportManagerApp(self.tabs[4], self.db_orders, self.db_products, self.username)

        if str(self.role) == "2":
            self.tab_control.add("Tài khoản")
            AccountManagerApp(self.tab_control.tab("Tài khoản"))

        # Tự động cập nhật thống kê khi chuyển tab
        self.tab_control.configure(command=lambda: self.app2.update_stats())

        # Mở tab mặc định
        try:
            if self.start_tab < len(names):
                self.tab_control.set(names[start_tab])
            elif str(self.role) == "2" and self.start_tab == 5:
                self.tab_control.set("Tài khoản")
        except:
            pass

    # --- CÁC HÀM XỬ LÝ (CONTROLLER) ---

    def show_about(self):
        """Hiển thị thông tin tác giả và phiên bản"""
        messagebox.showinfo("About 4S Team",
                            "Hệ thống Quản lý Shop Giày 4STeam\n"
                            "Phiên bản: 2.0 (Bản nâng cao)\n"
                            "Tác giả: Nhóm 4S Team\n"
                            "Ngày phát hành: 31/05/2026\n"
                            "Công nghệ: Python, CustomTkinter, Pandas, Numpy")

    def open_pdf(self):
        """Mở file hướng dẫn sử dụng (Yêu cầu nâng cao)"""
        pdf_path = "HuongDanSuDung.pdf"
        if os.path.exists(pdf_path):
            webbrowser.open_new(pdf_path)
        else:
            messagebox.showerror("Lỗi", "Không tìm thấy file HuongDanSuDung.pdf trong thư mục gốc!")

    def import_data(self):
        """Import dữ liệu từ file CSV bên ngoài vào kho hàng (Xử lý Threading)"""
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        # Tạo một luồng (Thread) xử lý riêng để không làm GUI bị treo (Yêu cầu nâng cao)
        def process_import():
            try:
                # Đọc dữ liệu bằng Pandas (Model)
                new_data = pd.read_csv(file_path)

                # Giả lập xử lý nặng để thấy hiệu quả của Threading (có thể bỏ qua khi chạy thật)
                import time;
                time.sleep(1.5)

                # Lưu vào database hệ thống
                new_data.to_csv(self.db_products, index=False, encoding="utf-8-sig")

                # Sau khi xong, dùng .after để cập nhật giao diện an toàn
                self.root.after(0, lambda: messagebox.showinfo("Thành công", "Đã nạp dữ liệu kho hàng thành công!"))
                self.root.after(0, self.app1.load_table)  # Refresh bảng ở tab Kho hàng
                self.root.after(0, self.app2.update_stats)  # Cập nhật lại số liệu thống kê
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Lỗi Import", f"Dữ liệu không đúng định dạng:\n{e}"))

        # Chạy task ngầm
        threading.Thread(target=process_import, daemon=True).start()