import tkinter as tk
from page.dangnhap import LoginUI
from page.quanlisanpham import ShoeManagerApp
from page.quanlitaikhoan import FootballManagerApp
from page.taotk import RegisterUI
from page.trangchu import HomeUI
from page.quenmatkhau import ForgotPasswordUI


class AppManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("4S Team Management System")
        self.root.geometry("1000x700")

        # Lưu trữ thông tin phiên đăng nhập
        self.current_user = None
        self.current_role = None
        self.current_app = None

    def clear_root(self):
        """Xóa tất cả widget trên màn hình trước khi chuyển trang"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login(self):
        """Hiển thị màn hình Đăng nhập"""
        self.clear_root()
        self.current_app = LoginUI(
            self.root,
            on_login_success=self.handle_login_success,
            on_go_to_register=self.show_register,
            on_forgot_password=self.show_forgot_password
        )

    def show_register(self):
        """Hiển thị màn hình Đăng ký"""
        self.clear_root()
        self.current_app = RegisterUI(self.root, on_back=self.show_login)

    def show_forgot_password(self):
        """Hiển thị màn hình Quên mật khẩu"""
        self.clear_root()
        self.current_app = ForgotPasswordUI(self.root, on_back=self.show_login)

    def handle_login_success(self, role, username):
        """Xử lý sau khi đăng nhập thành công"""
        self.current_user = username
        self.current_role = role
        self.show_home()

    def show_home(self):
        """Hiển thị màn hình Trang chủ (Dashboard)"""
        self.clear_root()
        self.current_app = HomeUI(
            self.root,
            username=self.current_user,
            role=self.current_role,
            on_logout=self.show_login,
            on_go_to_products=self.show_products,
            on_go_to_accounts=self.show_accounts
        )

    def show_products(self):
        """Chuyển đến màn hình Quản lý sản phẩm"""
        self.clear_root()
        # Khi nhấn "Đăng xuất" (hoặc Quay lại) trong kho hàng, trả về Trang chủ
        self.current_app = ShoeManagerApp(self.root, on_logout=self.show_home)

    def show_accounts(self):
        """Chuyển đến màn hình Quản lý tài khoản (Chỉ dành cho Admin)"""
        if self.current_role == 2:
            self.clear_root()
            # Khi nhấn "Đăng xuất" trong quản lý tài khoản, trả về Trang chủ
            self.current_app = FootballManagerApp(self.root, on_logout=self.show_home)

    def run(self):
        """Khởi chạy ứng dụng"""
        self.show_login()
        self.root.mainloop()