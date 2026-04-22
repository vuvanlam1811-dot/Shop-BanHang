import tkinter as tk
from page.dangnhap import LoginUI
from page.quanlisanpham import ShoeManagerApp
from page.quanlitaikhoan import FootballManagerApp
from page.taotk import RegisterUI

class AppManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("4S Team Management System")
        self.root.geometry("1000x700")
        self.current_app = None

    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear_root()
        self.current_app = LoginUI(
            self.root,
            on_login_success=self.handle_login_success,
            on_go_to_register=self.show_register
        )

    def show_register(self):
        self.clear_root()
        self.current_app = RegisterUI(self.root, on_back=self.show_login)

    def handle_login_success(self, role, username):
        self.clear_root()
        if role == 2:  # Admin
            self.current_app = FootballManagerApp(self.root, on_logout=self.show_login)
        else:          # User
            self.current_app = ShoeManagerApp(self.root, on_logout=self.show_login)

    def run(self):
        self.show_login()
        self.root.mainloop()