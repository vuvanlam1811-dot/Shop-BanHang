import tkinter as tk
import customtkinter as ctk
import os
import csv
from page.dangnhap import LoginUI
from page.taotk import RegisterUI
from page.quenmatkhau import ForgotPasswordUI
from page.khohang import MainShell
from page.trangchu import HomeUI

class AppManager:
    def __init__(self):
        self.init_database()
        self.root = ctk.CTk()
        self.root.title("4S Team Management System")
        self.root.geometry("1150x800")
        self.root.resizable(True, True)
        ctk.set_appearance_mode("Light")

        self.current_user = None
        self.current_role = None

    def init_database(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_dir = os.path.join(base_dir, "database")
        if not os.path.exists(db_dir): os.makedirs(db_dir)

        files = {
            "taikhoan.csv": ["username", "password", "email", "role"],
            "sanpham.csv": ["name", "brand", "price", "size", "sold"],
            "donhang.csv": ["id", "thang", "khach_hang", "ngay", "hang", "san_pham", "size", "so_luong", "tong_tien", "trang_thai"]
        }
        for file, header in files.items():
            path = os.path.join(db_dir, file)
            if not os.path.exists(path) or os.stat(path).st_size == 0:
                with open(path, "w", encoding="utf-8-sig", newline="") as f:
                    csv.writer(f).writerow(header)

    def clear_root(self):
        for widget in self.root.winfo_children(): widget.destroy()

    def show_login(self):
        self.clear_root()
        LoginUI(self.root, self.handle_login_success, self.show_register, self.show_forgot_password)

    def handle_login_success(self, role, username):
        self.current_user = username
        self.current_role = str(role)
        if self.current_role == "2":
            self.show_home()
        else:
            self.show_main_system(0)

    def show_home(self):
        self.clear_root()
        HomeUI(self.root, self.current_user, self.current_role,
               on_logout=self.show_login,
               on_go_to_products=lambda: self.show_main_system(0),
               on_go_to_accounts=lambda: self.show_main_system(5))

    def show_main_system(self, tab_index=0):
        self.clear_root()
        back_action = self.show_home if self.current_role == "2" else self.show_login
        MainShell(self.root, self.current_user, self.current_role, back_action, tab_index)

    def show_register(self):
        self.clear_root()
        RegisterUI(self.root, self.show_login)

    def show_forgot_password(self):
        self.clear_root()
        ForgotPasswordUI(self.root, self.show_login)

    def run(self):
        self.show_login()
        self.root.mainloop()