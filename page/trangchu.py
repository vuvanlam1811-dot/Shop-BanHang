import tkinter as tk
from tkinter import ttk


class HomeUI:
    def __init__(self, root, username, role, on_logout, on_go_to_products, on_go_to_accounts):
        self.root = root
        self.username = username
        self.role = role
        self.on_logout = on_logout
        self.on_go_to_products = on_go_to_products
        self.on_go_to_accounts = on_go_to_accounts
        self.setup_ui()

    def setup_ui(self):
        self.root.configure(bg="#F0F2F5")

        # --- HEADER ---
        header = tk.Frame(self.root, bg="#2B323F", height=100)
        header.pack(fill="x")

        tk.Label(header, text=f"XIN CHÀO, {self.username.upper()}", fg="white", bg="#2B323F",
                 font=("Arial Bold", 18)).pack(side="left", padx=30, pady=20)

        tk.Button(header, text="ĐĂNG XUẤT", bg="#e74c3c", fg="white", font=("Arial Bold", 10),
                  command=self.on_logout, padx=15).pack(side="right", padx=30)

        # --- BODY ---
        container = tk.Frame(self.root, bg="#F0F2F5")
        container.pack(expand=True, fill="both", padx=50, pady=50)

        title_label = tk.Label(container, text="BẢNG ĐIỀU KHIỂN HỆ THỐNG 4S TEAM",
                               font=("Arial Bold", 22), bg="#F0F2F5", fg="#2c3e50")
        title_label.pack(pady=(0, 40))

        card_frame = tk.Frame(container, bg="#F0F2F5")
        card_frame.pack()

        # Card: Quản lý sản phẩm (Dành cho cả User và Admin)
        self.create_menu_card(card_frame, "QUẢN LÝ KHO HÀNG", "Xem, thêm, sửa, xóa \nvà thống kê giày.",
                              "#3498db", self.on_go_to_products)

        # Card: Quản lý tài khoản (Chỉ dành cho Admin - Role 2)
        if self.role == 2:
            self.create_menu_card(card_frame, "QUẢN LÝ TÀI KHOẢN", "Quản lý quyền truy cập \nvà người dùng hệ thống.",
                                  "#27ae60", self.on_go_to_accounts)

    def create_menu_card(self, parent, title, desc, color, command):
        card = tk.Frame(parent, bg="white", highlightbackground="#dcdde1",
                        highlightthickness=1, width=300, height=350)
        card.pack(side="left", padx=20)
        card.pack_propagate(False)

        # Thanh màu phía trên
        tk.Frame(card, bg=color, height=10).pack(fill="x")

        tk.Label(card, text=title, font=("Arial Bold", 14), bg="white", fg=color).pack(pady=(30, 10))
        tk.Label(card, text=desc, font=("Arial", 11), bg="white", fg="#7f8c8d", justify="center").pack(pady=20)

        btn = tk.Button(card, text="TRUY CẬP", bg=color, fg="white", font=("Arial Bold", 11),
                        cursor="hand2", command=command, width=15, pady=8)
        btn.pack(side="bottom", pady=30)