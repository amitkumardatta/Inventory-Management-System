import os
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk

from dashboard import IMS
from billing import BillClass
from ui_theme import apply_theme


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.palette = apply_theme(self.root, "light")
        self.root.title("IMS Login")
        self.root.geometry("900x520+300+160")
        self.root.minsize(820, 480)
        self.root.config(bg=self.palette["bg"])

        self.var_email = tk.StringVar()
        self.var_pass = tk.StringVar()

        self.hero_image = None

        self._build_ui()

    def _build_ui(self):
        container = tk.Frame(self.root, bg=self.palette["bg"], bd=0)
        container.place(relx=0.5, rely=0.5, anchor="center", width=820, height=440)
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)

        left_panel = tk.Frame(container, bg=self.palette["sidebar"], bd=0)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 16))

        right_panel = tk.Frame(container, bg=self.palette["panel"], bd=0)
        right_panel.grid(row=0, column=1, sticky="nsew")

        image_path = os.path.join("images", "cat3.png")
        try:
            image = Image.open(image_path)
            image = image.resize((360, 360), Image.Resampling.LANCZOS)
            self.hero_image = ImageTk.PhotoImage(image)
            image_label = tk.Label(left_panel, image=self.hero_image, bg=self.palette["sidebar"])
            image_label.pack(expand=True)
        except Exception:
            fallback = tk.Label(
                left_panel,
                text="Inventory\nManagement\nSystem",
                font=("Helvetica Neue", 20, "bold"),
                bg=self.palette["sidebar"],
                fg=self.palette["sidebar_text"],
                justify="left",
            )
            fallback.pack(expand=True)

        brand = tk.Label(
            left_panel,
            text="IMS",
            font=("Helvetica Neue", 26, "bold"),
            bg=self.palette["sidebar"],
            fg=self.palette["sidebar_text"],
        )
        brand.pack(pady=(0, 20))

        title = tk.Label(
            right_panel,
            text="Welcome back",
            font=("Helvetica Neue", 22, "bold"),
            bg=self.palette["panel"],
            fg=self.palette["text"],
        )
        title.pack(pady=(36, 8))

        subtitle = tk.Label(
            right_panel,
            text="Sign in to continue",
            font=("Helvetica Neue", 12),
            bg=self.palette["panel"],
            fg=self.palette["muted"],
        )
        subtitle.pack(pady=(0, 24))

        form = tk.Frame(right_panel, bg=self.palette["panel"], bd=0)
        form.pack(fill="x", padx=60)

        tk.Label(
            form,
            text="Email",
            font=("Helvetica Neue", 11),
            bg=self.palette["panel"],
            fg=self.palette["muted"],
            anchor="w",
        ).pack(fill="x")
        tk.Entry(
            form,
            textvariable=self.var_email,
            font=("Helvetica Neue", 12),
            bg="white",
            fg=self.palette["text"],
            bd=1,
            relief="solid",
        ).pack(fill="x", pady=(6, 16), ipady=6)

        tk.Label(
            form,
            text="Password",
            font=("Helvetica Neue", 11),
            bg=self.palette["panel"],
            fg=self.palette["muted"],
            anchor="w",
        ).pack(fill="x")
        tk.Entry(
            form,
            textvariable=self.var_pass,
            show="*",
            font=("Helvetica Neue", 12),
            bg="white",
            fg=self.palette["text"],
            bd=1,
            relief="solid",
        ).pack(fill="x", pady=(6, 20), ipady=6)

        ttk.Button(
            right_panel,
            text="Login",
            command=self.login,
            style="Accent.TButton",
        ).pack(padx=60, fill="x", ipady=8)

        self.root.bind("<Return>", lambda event: self.login())

    def login(self):
        email = self.var_email.get().strip()
        password = self.var_pass.get().strip()
        if not email or not password:
            messagebox.showerror("Error", "Email and password are required", parent=self.root)
            return

        con = sqlite3.connect(database=r"ims.db")
        cur = con.cursor()
        try:
            cur.execute(
                "SELECT utype FROM employee WHERE email=? AND pass=?",
                (email, password),
            )
            row = cur.fetchone()
            if row is None:
                messagebox.showerror("Error", "Invalid credentials", parent=self.root)
                return

            user_type = row[0]
            self.root.destroy()
            if user_type == "Admin":
                root = tk.Tk()
                IMS(root)
                root.mainloop()
            else:
                root = tk.Tk()
                BillClass(root)
                root.mainloop()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()


if __name__ == "__main__":
    os.system("python start.py")
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()
