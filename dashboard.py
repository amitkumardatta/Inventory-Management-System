from tkinter import *
from tkinter import messagebox, ttk
from PIL import ImageTk
import PIL.Image
import os
import sqlite3
import time
import webbrowser

from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass
from ui_theme import apply_theme, colors


class DashboardView(Frame):
    def __init__(self, parent, palette):
        super().__init__(parent, bg=palette["bg"])
        self.palette = palette
        self.heading = None
        self.cards_frame = None
        self.card_frames = []
        self.card_title_labels = []
        self.card_value_labels = []
        self._build()

    def _build(self):
        self.heading = Label(
            self,
            text="Business Overview",
            font=("Helvetica Neue", 22, "bold"),
            bg=self.palette["bg"],
            fg=self.palette["text"],
            anchor="w",
        )
        self.heading.pack(fill=X, padx=20, pady=(20, 10))

        self.cards_frame = Frame(self, bg=self.palette["bg"])
        self.cards_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
        for i in range(3):
            self.cards_frame.columnconfigure(i, weight=1)
        self.cards_frame.rowconfigure(0, weight=1)
        self.cards_frame.rowconfigure(1, weight=1)

        self.lbl_employee = self._card(self.cards_frame, 0, 0, "Total Employee", "0", "#2563eb")
        self.lbl_supplier = self._card(self.cards_frame, 1, 0, "Total Supplier", "0", "#f97316")
        self.lbl_category = self._card(self.cards_frame, 2, 0, "Total Category", "0", "#0ea5a7")
        self.lbl_product = self._card(self.cards_frame, 0, 1, "Total Product", "0", "#64748b")
        self.lbl_sales = self._card(self.cards_frame, 1, 1, "Total Sales", "0", "#f59e0b")

    def _card(self, parent, col, row, title, value, color):
        card = Frame(parent, bg=color, bd=0)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        title_lbl = Label(
            card,
            text=title,
            font=("Helvetica Neue", 14, "bold"),
            bg=color,
            fg="white",
            anchor="w",
        )
        title_lbl.pack(fill=X, padx=14, pady=(18, 4))
        value_lbl = Label(
            card,
            text=value,
            font=("Helvetica Neue", 28, "bold"),
            bg=color,
            fg="white",
            anchor="w",
        )
        value_lbl.pack(fill=X, padx=14, pady=(0, 18))
        self.card_frames.append(card)
        self.card_title_labels.append(title_lbl)
        self.card_value_labels.append(value_lbl)
        return value_lbl

    def apply_theme(self, palette):
        self.palette = palette
        self.config(bg=self.palette["bg"])
        if self.heading:
            self.heading.config(bg=self.palette["bg"], fg=self.palette["text"])
        if self.cards_frame:
            self.cards_frame.config(bg=self.palette["bg"])

    def set_counts(self, employee, supplier, category, product, sales):
        self.lbl_employee.config(text=str(employee))
        self.lbl_supplier.config(text=str(supplier))
        self.lbl_category.config(text=str(category))
        self.lbl_product.config(text=str(product))
        self.lbl_sales.config(text=str(sales))


class IMS:
    def __init__(self, root):
        self.root = root
        self.theme_mode = "light"
        self.palette = apply_theme(self.root, self.theme_mode)
        self.root.geometry("1400x820+0+0")
        self.root.minsize(1100, 700)
        self.root.title("IMS | Developed by Amit")
        self.root.config(bg=self.palette["bg"])
        photo = PhotoImage(file=os.path.join("images", "i1.png"))
        self.root.iconphoto(False, photo)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(2, weight=1)

        self._build_header()
        self._build_clock()
        self._build_main()
        self._build_footer()
        self._build_views()
        self.show_view("dashboard")
        self.refresh_counts()
        self.update_clock()

    def _build_header(self):
        self.header = Frame(self.root, bg=self.palette["sidebar"], height=70)
        self.header.grid(row=0, column=0, sticky="nsew")
        self.header.grid_propagate(False)
        self.header.columnconfigure(0, weight=1)

        self.icon_title = PhotoImage(file=os.path.join("images", "icon1.png"))
        self.title_label = Label(
            self.header,
            text="Inventory Management System",
            image=self.icon_title,
            compound=LEFT,
            font=("Helvetica Neue", 24, "bold"),
            bg=self.palette["sidebar"],
            fg=self.palette["sidebar_text"],
            anchor="w",
            padx=20,
        )
        self.title_label.grid(row=0, column=0, sticky="w")

        self.btn_theme = ttk.Button(
            self.header,
            text="Dark",
            command=self.toggle_theme,
            style="Accent.TButton",
        )
        self.btn_theme.grid(row=0, column=1, padx=(0, 10), pady=14)

        self.btn_logout = ttk.Button(
            self.header,
            text="Logout",
            command=self.logout,
            style="Danger.TButton",
        )
        self.btn_logout.grid(row=0, column=2, padx=20, pady=12)

    def _build_clock(self):
        self.clock_bar = Frame(self.root, bg="#1e293b", height=34)
        self.clock_bar.grid(row=1, column=0, sticky="nsew")
        self.clock_bar.grid_propagate(False)
        self.lbl_clock = Label(
            self.clock_bar,
            text="",
            font=("Helvetica Neue", 11),
            bg="#1e293b",
            fg=self.palette["sidebar_text"],
        )
        self.lbl_clock.pack(fill=BOTH, padx=20)

    def _build_main(self):
        self.main_frame = Frame(self.root, bg=self.palette["bg"])
        self.main_frame.grid(row=2, column=0, sticky="nsew")
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

        self.sidebar = Frame(self.main_frame, bg=self.palette["sidebar"], width=220)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        self.content_frame = Frame(self.main_frame, bg=self.palette["bg"])
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        self.content_frame.rowconfigure(0, weight=1)
        self.content_frame.columnconfigure(0, weight=1)

        self.MenuLogo = PIL.Image.open(os.path.join("images", "l1.png"))
        self.MenuLogo = self.MenuLogo.resize((170, 170), PIL.Image.Resampling.LANCZOS)
        self.MenuLogo = ImageTk.PhotoImage(self.MenuLogo)
        lbl_menuLogo = Label(self.sidebar, image=self.MenuLogo, bg=self.palette["sidebar"])
        lbl_menuLogo.pack(side=TOP, fill=X, pady=(15, 5))

        self.lbl_menu = Label(
            self.sidebar,
            text="Menu",
            font=("Helvetica Neue", 16, "bold"),
            bg=self.palette["sidebar"],
            fg=self.palette["sidebar_text"],
        )
        self.lbl_menu.pack(side=TOP, fill=X, pady=(0, 8))


        self.sidebar_buttons = []
        self._sidebar_button("Dashboard", lambda: self.show_view("dashboard"), text_only=True)
        self._sidebar_button("Employee", lambda: self.show_view("employee"), text_only=True)
        self._sidebar_button("Supplier", lambda: self.show_view("supplier"), text_only=True)
        self._sidebar_button("Category", lambda: self.show_view("category"), text_only=True)
        self._sidebar_button("Products", lambda: self.show_view("product"), text_only=True)
        self._sidebar_button("Sales", lambda: self.show_view("sales"), text_only=True)
        self._sidebar_button("Exit", self.exit, text_only=True)

    def _sidebar_button(self, text, command, text_only=False):
        btn = ttk.Button(
            self.sidebar,
            text=f"> {text}" if text_only else text,
            command=command,
            style="Sidebar.TButton",
            padding=(16, 6),
        )
        btn.pack(side=TOP, fill=X, pady=2)
        self.sidebar_buttons.append(btn)

    def _build_footer(self):
        self.footer = Frame(self.root, bg="#1e293b")
        self.footer.grid(row=3, column=0, sticky="nsew")
        self.lbl_footer = Label(
            self.footer,
            text="IMS - Inventory Management System | Developed by Amit",
            font=("Helvetica Neue", 10),
            bg="#1e293b",
            fg=self.palette["sidebar_text"],
        )
        self.lbl_footer.pack(side=LEFT, padx=10, pady=6)

        self.footer_image = PhotoImage(file=os.path.join("images", "footer1.png"))
        self.btn_footer = Button(
            self.footer,
            command=self.test1,
            image=self.footer_image,
            compound=RIGHT,
            cursor="hand2",
            bd=0,
            bg="#1e293b",
            activebackground="#1e293b",
        )
        self.btn_footer.pack(side=RIGHT, padx=10)

    def _build_views(self):
        self.view_frames = {}
        for name in ("dashboard", "employee", "supplier", "category", "product", "sales"):
            frame = Frame(self.content_frame, bg=self.palette["bg"])
            frame.grid(row=0, column=0, sticky="nsew")
            self.view_frames[name] = frame

        self.dashboard_view = DashboardView(self.view_frames["dashboard"], self.palette)
        self.views = {
            "dashboard": self.dashboard_view,
            "employee": employeeClass(self.view_frames["employee"], show_menu=self.toggle_sidebar),
            "supplier": supplierClass(self.view_frames["supplier"], show_menu=self.toggle_sidebar),
            "category": categoryClass(self.view_frames["category"], show_menu=self.toggle_sidebar),
            "product": productClass(self.view_frames["product"], show_menu=self.toggle_sidebar),
            "sales": salesClass(self.view_frames["sales"], show_menu=self.toggle_sidebar),
        }
        for view in self.views.values():
            if isinstance(view, Frame):
                view.pack(fill=BOTH, expand=True)

    def show_view(self, name):
        frame = self.view_frames.get(name)
        if frame:
            frame.tkraise()
        if name == "dashboard":
            self.refresh_counts()

    def refresh_counts(self):
        employee_count = 0
        supplier_count = 0
        category_count = 0
        product_count = 0
        sales_count = 0
        try:
            con = sqlite3.connect(database=r"ims.db")
            cur = con.cursor()
            cur.execute("SELECT COUNT(*) FROM employee")
            employee_count = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM supplier")
            supplier_count = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM category")
            category_count = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM product")
            product_count = cur.fetchone()[0]
            con.close()
        except Exception:
            pass

        try:
            sales_count = len([
                name
                for name in os.listdir("bill/")
                if name.lower().endswith(".txt")
            ])
        except Exception:
            sales_count = 0

        if self.dashboard_view:
            self.dashboard_view.set_counts(
                employee_count,
                supplier_count,
                category_count,
                product_count,
                sales_count,
            )

    def toggle_sidebar(self):
        if self.sidebar.winfo_ismapped():
            self.sidebar.grid_remove()
        else:
            self.sidebar.grid()

    def toggle_theme(self):
        self.theme_mode = "dark" if self.theme_mode == "light" else "light"
        self.palette = apply_theme(self.root, self.theme_mode)
        self.apply_theme_to_widgets()
        self.btn_theme.config(text="Light" if self.theme_mode == "dark" else "Dark")

    def apply_theme_to_widgets(self):
        self.root.config(bg=self.palette["bg"])
        self.header.config(bg=self.palette["sidebar"])
        self.title_label.config(bg=self.palette["sidebar"], fg=self.palette["sidebar_text"])
        self.btn_theme.config(style="Accent.TButton")
        self.btn_logout.config(style="Danger.TButton")
        self.clock_bar.config(bg=self.palette["sidebar"])
        self.lbl_clock.config(bg=self.palette["sidebar"], fg=self.palette["sidebar_text"])
        self.main_frame.config(bg=self.palette["bg"])
        self.sidebar.config(bg=self.palette["sidebar"])
        self.lbl_menu.config(bg=self.palette["sidebar"], fg=self.palette["sidebar_text"])
        for btn in self.sidebar_buttons:
            btn.config(style="Sidebar.TButton")
        self.content_frame.config(bg=self.palette["bg"])
        for frame in self.view_frames.values():
            frame.config(bg=self.palette["bg"])
        if self.dashboard_view:
            self.dashboard_view.apply_theme(self.palette)
        self.footer.config(bg=self.palette["sidebar"])
        self.lbl_footer.config(bg=self.palette["sidebar"], fg=self.palette["sidebar_text"])
        self.btn_footer.config(bg=self.palette["sidebar"], activebackground=self.palette["sidebar"])

    def update_clock(self):
        date_str = time.strftime("%d-%m-%Y")
        time_str = time.strftime("%H:%M:%S")
        self.lbl_clock.config(
            text=f"Welcome to Inventory Management System    Date: {date_str}    Time: {time_str}"
        )
        self.lbl_clock.after(1000, self.update_clock)

    def test1(self):
        webbrowser.open("https://amitkumardatta2005.wixsite.com/website-1/about-1")

    def logout(self):
        self.root.destroy()
        from login import LoginWindow
        root = Tk()
        LoginWindow(root)
        root.mainloop()

    def exit(self):
        exit_ok = messagebox.askyesno("Exit", "Do you really want exit?", parent=self.root)
        if exit_ok:
            self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    obj = IMS(root)
    root.mainloop()