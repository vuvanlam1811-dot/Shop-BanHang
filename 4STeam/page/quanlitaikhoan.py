import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import csv, os


class AccountManagerApp:
    def __init__(self, root):
        self.root = root
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.file_path = os.path.join(base_dir, "database", "taikhoan.csv")
        self.setup_ui()
        self.load_table()

    def setup_ui(self):
        container = ctk.CTkFrame(self.root, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # Form nhập liệu
        lf = ctk.CTkFrame(container, width=280, corner_radius=10)
        lf.pack(side="left", fill="y", padx=(0, 20))

        ctk.CTkLabel(lf, text="QUẢN TRỊ USER", font=("Arial", 14, "bold")).pack(pady=10)

        self.ents = {}
        for lbl, k in [("Username:", "u"), ("Password:", "p"), ("Email:", "e")]:
            ctk.CTkLabel(lf, text=lbl).pack(anchor="w", padx=10)
            self.ents[k] = ctk.CTkEntry(lf)
            self.ents[k].pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(lf, text="Quyền (1:User, 2:Admin):").pack(anchor="w", padx=10)
        self.ents['r'] = ctk.CTkOptionMenu(lf, values=["1", "2"])
        self.ents['r'].pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(lf, text="THÊM", fg_color="#27ae60", command=self.add_acc).pack(fill="x", padx=10, pady=10)
        ctk.CTkButton(lf, text="SỬA", fg_color="#f39c12", command=self.update_acc).pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(lf, text="XÓA", fg_color="#e74c3c", command=self.delete_acc).pack(fill="x", padx=10, pady=5)

        # Table
        self.tree = ttk.Treeview(container, columns=("u", "p", "e", "r"), show="headings")
        for c, h in zip(("u", "p", "e", "r"), ["USERNAME", "PASSWORD", "EMAIL", "ROLE"]):
            self.tree.heading(c, text=h)
            self.tree.column(c, width=100, anchor="center")
        self.tree.pack(side="right", fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def on_select(self, event):
        sel = self.tree.focus()
        if not sel: return
        v = self.tree.item(sel)['values']
        for i, k in enumerate(['u', 'p', 'e', 'r']):
            if k == 'r':
                self.ents[k].set(str(v[i]))
            else:
                self.ents[k].delete(0, tk.END)
                self.ents[k].insert(0, v[i])

    def add_acc(self):
        d = [self.ents[k].get() for k in ['u', 'p', 'e', 'r']]
        if not d[0]: return
        self.tree.insert("", "end", values=d)
        self.save_csv()

    def update_acc(self):
        sel = self.tree.focus()
        if not sel: return
        d = [self.ents[k].get() for k in ['u', 'p', 'e', 'r']]
        self.tree.item(sel, values=d)
        self.save_csv()

    def delete_acc(self):
        sel = self.tree.focus()
        if not sel: return
        self.tree.delete(sel)
        self.save_csv()

    def save_csv(self):
        with open(self.file_path, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["username", "password", "email", "role"])
            for r in self.tree.get_children():
                writer.writerow(self.tree.item(r)['values'])

    def load_table(self):
        if not os.path.exists(self.file_path): return
        with open(self.file_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for r in reader:
                self.tree.insert("", "end", values=(r['username'], r['password'], r['email'], r['role']))