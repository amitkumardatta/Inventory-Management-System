import os, sys, time, sqlite3
from tkinter import *
from tkinter import ttk, messagebox
import os
import platform
import subprocess

try:
    from PIL import ImageTk, Image as PILImage
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# ══════════════════════════════════════════════════════════════════
#  COLOUR PALETTES
# ══════════════════════════════════════════════════════════════════
THEMES = {
    "dark": {
        "win_bg":        "#0e1117",
        "sidebar_bg":    "#13181f",
        "panel_bg":      "#1a2130",
        "panel_border":  "#252f40",
        "header_bg":     "#141b26",
        "hdr_accent":    "#0ea5e9",   # sky-500
        "hdr_text":      "#f1f5f9",
        "hdr_sub":       "#64748b",
        "text":          "#e2e8f0",
        "text_muted":    "#64748b",
        "text_dim":      "#475569",
        "input_bg":      "#0e1117",
        "input_border":  "#2d3a4e",
        "input_focus":   "#0ea5e9",
        "tbl_head_bg":   "#0e1117",
        "tbl_row_a":     "#1a2130",
        "tbl_row_b":     "#1f2840",
        "tbl_sel":       "#0c3251",
        "tbl_sel_fg":    "#7dd3fc",
        "accent":        "#0ea5e9",
        "accent_dark":   "#0284c7",
        "accent_fg":     "#ffffff",
        "green":         "#22c55e",
        "green_dark":    "#16a34a",
        "green_bg":      "#14271e",
        "amber":         "#f59e0b",
        "amber_dark":    "#d97706",
        "red":           "#ef4444",
        "red_dark":      "#dc2626",
        "red_bg":        "#2a1515",
        "divider":       "#1e2d3e",
        "receipt_bg":    "#0e1117",
        "receipt_fg":    "#94a3b8",
        "receipt_hl":    "#e2e8f0",
        "tile1_bg":      "#0c2a3e",
        "tile1_fg":      "#7dd3fc",
        "tile2_bg":      "#0f2a1a",
        "tile2_fg":      "#86efac",
        "tile3_bg":      "#1e1a0e",
        "tile3_fg":      "#fde68a",
    },
    "light": {
        "win_bg":        "#f1f5f9",
        "sidebar_bg":    "#ffffff",
        "panel_bg":      "#ffffff",
        "panel_border":  "#e2e8f0",
        "header_bg":     "#1e2d45",
        "hdr_accent":    "#38bdf8",
        "hdr_text":      "#ffffff",
        "hdr_sub":       "#93c5fd",
        "text":          "#1e293b",
        "text_muted":    "#64748b",
        "text_dim":      "#94a3b8",
        "input_bg":      "#f8fafc",
        "input_border":  "#cbd5e1",
        "input_focus":   "#3b82f6",
        "tbl_head_bg":   "#1e2d45",
        "tbl_row_a":     "#f8fafc",
        "tbl_row_b":     "#ffffff",
        "tbl_sel":       "#dbeafe",
        "tbl_sel_fg":    "#1d4ed8",
        "accent":        "#2563eb",
        "accent_dark":   "#1d4ed8",
        "accent_fg":     "#ffffff",
        "green":         "#16a34a",
        "green_dark":    "#15803d",
        "green_bg":      "#f0fdf4",
        "amber":         "#d97706",
        "amber_dark":    "#b45309",
        "red":           "#dc2626",
        "red_dark":      "#b91c1c",
        "red_bg":        "#fef2f2",
        "divider":       "#e2e8f0",
        "receipt_bg":    "#fffdf7",
        "receipt_fg":    "#475569",
        "receipt_hl":    "#1e293b",
        "tile1_bg":      "#eff6ff",
        "tile1_fg":      "#1d4ed8",
        "tile2_bg":      "#f0fdf4",
        "tile2_fg":      "#15803d",
        "tile3_bg":      "#fffbeb",
        "tile3_fg":      "#92400e",
    },
}


# ══════════════════════════════════════════════════════════════════
#  STYLE BUILDER
# ══════════════════════════════════════════════════════════════════
def build_styles(p):
    s = ttk.Style()
    s.theme_use("clam")

    s.configure(".", background=p["panel_bg"], foreground=p["text"],
                font=("Segoe UI", 10), borderwidth=0, relief="flat")

    # ── Treeview ──────────────────────────────────────────────────
    s.configure("T.Treeview",
                background=p["tbl_row_a"], foreground=p["text"],
                fieldbackground=p["tbl_row_a"],
                rowheight=30, borderwidth=0, relief="flat",
                font=("Segoe UI", 10))
    s.configure("T.Treeview.Heading",
                background=p["tbl_head_bg"], foreground=p["hdr_text"],
                font=("Segoe UI", 10, "bold"),
                relief="flat", padding=(8, 8))
    s.map("T.Treeview",
          background=[("selected", p["tbl_sel"])],
          foreground=[("selected", p["tbl_sel_fg"])])

    # ── Buttons ───────────────────────────────────────────────────
    defs = {
        "Primary":  (p["accent"],  p["accent_dark"],  p["accent_fg"]),
        "Success":  (p["green"],   p["green_dark"],   "#ffffff"),
        "Warning":  (p["amber"],   p["amber_dark"],   "#ffffff"),
        "Danger":   (p["red"],     p["red_dark"],     "#ffffff"),
        "Ghost":    (p["panel_bg"], p["panel_border"],p["text_muted"]),
    }
    for name, (bg, hbg, fg) in defs.items():
        s.configure(f"{name}.TButton",
                    background=bg, foreground=fg,
                    font=("Segoe UI", 10, "bold"),
                    padding=(12, 7), relief="flat", borderwidth=0)
        s.map(f"{name}.TButton",
              background=[("active", hbg), ("pressed", hbg)],
              foreground=[("active", fg)])

    # Calc variants
    for name, bg, hbg, fg in [
        ("Num",  p["panel_border"], p["text_dim"],    p["text"]),
        ("Op",   p["accent"],       p["accent_dark"], "#ffffff"),
        ("Eq",   p["green"],        p["green_dark"],  "#ffffff"),
        ("Clr",  p["red"],          p["red_dark"],    "#ffffff"),
    ]:
        s.configure(f"C{name}.TButton",
                    background=bg, foreground=fg,
                    font=("Segoe UI", 14, "bold"),
                    padding=(4, 8), relief="flat", borderwidth=0)
        s.map(f"C{name}.TButton",
              background=[("active", hbg)],
              foreground=[("active", fg)])

    # Scrollbar
    s.configure("Slim.Vertical.TScrollbar",
                background=p["panel_border"], troughcolor=p["panel_bg"],
                borderwidth=0, arrowsize=12, width=8)
    s.configure("Slim.Horizontal.TScrollbar",
                background=p["panel_border"], troughcolor=p["panel_bg"],
                borderwidth=0, arrowsize=12, width=8)


# ══════════════════════════════════════════════════════════════════
#  WIDGET HELPERS
# ══════════════════════════════════════════════════════════════════
# ══════════════════════════════════════════════════════════════════
#  FIXED PANEL + SECTIONBAR
# ══════════════════════════════════════════════════════════════════

def Panel(parent, p, **kw):
    """
    Safe panel system.
    OUTER uses grid with parent.
    INNER should use ONLY pack internally.
    """

    outer = Frame(parent, bg=p["panel_border"])
    outer.grid(**kw)

    inner = Frame(outer, bg=p["panel_bg"])
    inner.pack(fill=BOTH, expand=True, padx=1, pady=1)

    return inner


def SectionBar(parent, p, title, icon=""):
    """
    Header bar using pack ONLY.
    """

    bar = Frame(parent, bg=p["header_bg"], height=38)
    bar.pack(fill=X)

    bar.pack_propagate(False)

    full = f"  {icon}  {title}" if icon else f"  {title}"

    # Accent line
    Frame(bar, bg=p["hdr_accent"], width=4).pack(
        side=LEFT,
        fill=Y
    )

    Label(
        bar,
        text=full,
        font=("Segoe UI", 10, "bold"),
        bg=p["header_bg"],
        fg=p["hdr_text"],
        anchor=W
    ).pack(
        side=LEFT,
        fill=BOTH,
        expand=True,
        padx=8
    )

    return bar

def StyledEntry(parent, p, textvariable, readonly=False, width=None):
    kw = dict(
        textvariable=textvariable,
        font=("Segoe UI", 11),
        bg=p["input_bg"], fg=p["text"],
        insertbackground=p["text"],
        relief="flat",
        highlightthickness=1,
        highlightbackground=p["input_border"],
        highlightcolor=p["input_focus"],
        bd=0,
    )
    if width:
        kw["width"] = width
    if readonly:
        kw["state"] = "readonly"
        kw["readonlybackground"] = p["panel_border"]
    return Entry(parent, **kw)


# ══════════════════════════════════════════════════════════════════
#  MAIN CLASS
# ══════════════════════════════════════════════════════════════════
class BillClass:
    def __init__(self, root, theme="dark"):
        self.root = root
        self.theme_mode = theme
        self.p = THEMES[theme]
        self.cart_list   = []
        self.bill_amnt   = 0.0
        self.discount    = 0.0
        self.net_pay     = 0.0

        # StringVars
        self.var_search  = StringVar()
        self.var_cname   = StringVar()
        self.var_contact = StringVar()
        self.var_pid     = StringVar()
        self.var_pname   = StringVar()
        self.var_price   = StringVar()
        self.var_qty     = StringVar()
        self.var_stock   = StringVar()
        self.var_cal     = StringVar()

        self._setup_root()
        build_styles(self.p)
        self._build_header()
        self._build_body()
        self.show()
        self.update_clock()
    def toggle_theme(self):

        new = "light" if self.theme_mode == "dark" else "dark"

        self.root.destroy()

        import subprocess
        import sys

        subprocess.Popen([
            sys.executable,
            __file__,
            "--theme",
            new
        ])
    # ── Root ─────────────────────────────────────────────────────
    def _setup_root(self):
        self.root.title("IMS  ·  Point of Sale")
        self.root.geometry("1480x880+0+0")
        self.root.minsize(1280, 760)
        self.root.config(bg=self.p["win_bg"])
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        try:
            img = PhotoImage(file=os.path.join("images", "i1.png"))
            self.root.iconphoto(False, img)
        except Exception:
            pass

    # ── Header ───────────────────────────────────────────────────
    def _build_header(self):
        p = self.p
        hdr = Frame(self.root, bg=p["header_bg"], height=62)
        hdr.grid(row=0, column=0, sticky="ew")
        hdr.grid_propagate(False)
        hdr.columnconfigure(1, weight=1)

        # Left – logo
        logo = Frame(hdr, bg=p["header_bg"])
        logo.grid(row=0, column=0, sticky="ns", padx=(20, 30))

        dot = Frame(logo, bg=p["hdr_accent"], width=5)
        dot.pack(side=LEFT, fill=Y, pady=14, padx=(0, 10))

        txt = Frame(logo, bg=p["header_bg"])
        txt.pack(side=LEFT, pady=10)
        Label(txt, text="Inventory Management System",
              font=("Segoe UI", 15, "bold"),
              bg=p["header_bg"], fg=p["hdr_text"]).pack(anchor=W)
        Label(txt, text="Point of Sale  ·  Developed by Amit",
              font=("Segoe UI", 8),
              bg=p["header_bg"], fg=p["hdr_sub"]).pack(anchor=W)

        # Centre – clock
        self.lbl_clock = Label(hdr, text="",
                               font=("Segoe UI", 10),
                               bg=p["header_bg"], fg=p["hdr_sub"])
        self.lbl_clock.grid(row=0, column=1)

        # Right – buttons
        btns = Frame(hdr, bg=p["header_bg"])
        btns.grid(row=0, column=2, padx=20, sticky="ns", pady=12)

        self.btn_theme = ttk.Button(btns,
            text="☾  Dark" if self.theme_mode == "light" else "☀  Light",
            command=self.toggle_theme, style="Ghost.TButton", width=10)
        self.btn_theme.pack(side=LEFT, padx=(0, 8))

        ttk.Button(btns, text="⏻  Logout",
                   command=self.logout,
                   style="Danger.TButton", width=9).pack(side=LEFT)

    # ── Body (3 columns) ─────────────────────────────────────────
    def _build_body(self):
        p = self.p
        body = Frame(self.root, bg=p["win_bg"])
        body.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        body.columnconfigure(0, weight=28, minsize=310)
        body.columnconfigure(1, weight=44, minsize=480)
        body.columnconfigure(2, weight=28, minsize=310)
        body.rowconfigure(0, weight=1)

        self._build_products(body)
        self._build_centre(body)
        self._build_receipt(body)

    # ══════════════════════════════════════════════════════════════
    #  LEFT – Products
    # ══════════════════════════════════════════════════════════════
    def _build_products(self, body):
        p = self.p
        col = Frame(body, bg=p["win_bg"])
        col.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        col.rowconfigure(1, weight=1)
        col.columnconfigure(0, weight=1)

        # ── Search panel ──────────────────────────────────────────
        sp = Panel(col, p, row=0, column=0, sticky="ew", pady=(0, 8))
        sp.columnconfigure(0, weight=1)
        SectionBar(sp, p, "Products", "📦")

        sb = Frame(sp, bg=p["panel_bg"])
        sb.pack(fill=X, padx=10, pady=10)
        sb.columnconfigure(0, weight=1)

        self.txt_search_entry = StyledEntry(sb, p, self.var_search)
        self.txt_search_entry.grid(row=0, column=0, sticky="ew",
                                   ipady=7, padx=(0, 6))
        self.txt_search_entry.insert(0, "Search products…")
        self.txt_search_entry.config(fg=p["text_muted"])
        self.txt_search_entry.bind("<FocusIn>",  self._sf_in)
        self.txt_search_entry.bind("<FocusOut>", self._sf_out)
        self.txt_search_entry.bind("<Return>",   lambda e: self.search())

        btn_row = Frame(sb, bg=p["panel_bg"])
        btn_row.grid(row=1, column=0, sticky="ew", pady=(6, 0))
        btn_row.columnconfigure(0, weight=1)
        btn_row.columnconfigure(1, weight=1)
        ttk.Button(btn_row, text="🔍  Search",
                   command=self.search,
                   style="Primary.TButton").grid(
            row=0, column=0, sticky="ew", padx=(0, 4))
        ttk.Button(btn_row, text="↺  Show All",
                   command=self.show,
                   style="Ghost.TButton").grid(
            row=0, column=1, sticky="ew")

        # ── Product table ─────────────────────────────────────────
        tp = Panel(col, p, row=1, column=0, sticky="nsew", pady=(0, 6))
        tp.rowconfigure(1, weight=1)
        tp.columnconfigure(0, weight=1)
        SectionBar(tp, p, "Available Stock", "")

        # hint strip
        Label(tp, text="  Click a product to select it",
              font=("Segoe UI", 8), bg=p["panel_border"],
              fg=p["text_dim"], anchor=W).pack(fill=X, ipady=2)

        tbl_f = Frame(tp, bg=p["panel_bg"])
        tbl_f.pack(fill=BOTH, expand=True)
        tbl_f.rowconfigure(0, weight=1)
        tbl_f.columnconfigure(0, weight=1)

        sy = ttk.Scrollbar(tbl_f, orient=VERTICAL,
                           style="Slim.Vertical.TScrollbar")
        sy.grid(row=0, column=1, sticky="ns")
        sx = ttk.Scrollbar(tbl_f, orient=HORIZONTAL,
                           style="Slim.Horizontal.TScrollbar")
        sx.grid(row=1, column=0, sticky="ew")

        self.product_Table = ttk.Treeview(
            tbl_f, style="T.Treeview",
            columns=("pid", "name", "price", "qty", "status"),
            yscrollcommand=sy.set, xscrollcommand=sx.set,
            selectmode="browse", show="headings",
        )
        sy.config(command=self.product_Table.yview)
        sx.config(command=self.product_Table.xview)
        self.product_Table.grid(row=0, column=0, sticky="nsew")

        for col_id, txt, w, anchor in [
            ("pid",    "ID",     50,  CENTER),
            ("name",   "Name",  150,  W),
            ("price",  "Price",  80,  CENTER),
            ("qty",    "Stock",  60,  CENTER),
            ("status", "Status", 65,  CENTER),
        ]:
            self.product_Table.heading(col_id, text=txt)
            self.product_Table.column(col_id, width=w, anchor=anchor)

        self.product_Table.tag_configure("odd",  background=p["tbl_row_a"])
        self.product_Table.tag_configure("even", background=p["tbl_row_b"])
        self.product_Table.bind("<ButtonRelease-1>", self.get_data)

        # note
        Label(col, text="  ℹ  Enter quantity = 0 to remove item from cart",
              font=("Segoe UI", 8), bg=p["win_bg"],
              fg=p["text_dim"], anchor=W).grid(
            row=2, column=0, sticky="ew")

    def _sf_in(self, e):
        if self.txt_search_entry.get() == "Search products…":
            self.txt_search_entry.delete(0, END)
            self.txt_search_entry.config(fg=self.p["text"])

    def _sf_out(self, e):
        if not self.txt_search_entry.get():
            self.txt_search_entry.insert(0, "Search products…")
            self.txt_search_entry.config(fg=self.p["text_muted"])

    # ══════════════════════════════════════════════════════════════
    #  CENTRE – Customer / Cart / Calculator / Add-to-cart
    # ══════════════════════════════════════════════════════════════
    def _build_centre(self, body):
        p = self.p
        col = Frame(body, bg=p["win_bg"])
        col.grid(row=0, column=1, sticky="nsew", padx=(0, 8))
        col.rowconfigure(1, weight=1)
        col.columnconfigure(0, weight=1)

        self._build_customer(col)
        self._build_cart_calc(col)
        self._build_add_cart(col)

    def _build_customer(self, col):
        p = self.p
        cp = Panel(col, p, row=0, column=0, sticky="ew", pady=(0, 8))
        cp.columnconfigure(0, weight=1)
        SectionBar(cp, p, "Customer Details", "👤")

        body = Frame(cp, bg=p["panel_bg"])
        body.pack(fill=X, padx=12, pady=10)
        for i in range(4):
            body.columnconfigure(i, weight=1)

        for c, lbl, var in [(0, "Customer Name", self.var_cname),
                            (2, "Contact Number", self.var_contact)]:
            Label(body, text=lbl, font=("Segoe UI", 9, "bold"),
                  bg=p["panel_bg"], fg=p["text_muted"]).grid(
                row=0, column=c, columnspan=2, sticky=W, padx=(0, 8))
            StyledEntry(body, p, var).grid(
                row=1, column=c, columnspan=2, sticky="ew",
                ipady=7, padx=(0, 8 if c == 0 else 0), pady=(3, 0))

    def _build_cart_calc(self, col):
        p = self.p
        row = Frame(col, bg=p["win_bg"])
        row.grid(row=1, column=0, sticky="nsew", pady=(0, 8))
        row.columnconfigure(0, weight=3)
        row.columnconfigure(1, weight=2)
        row.rowconfigure(0, weight=1)

        # ── Cart ──────────────────────────────────────────────────
        cart_p = Panel(row, p, row=0, column=0, sticky="nsew",
                       padx=(0, 8))
        cart_p.rowconfigure(2, weight=1)
        cart_p.columnconfigure(0, weight=1)

        hdr = SectionBar(cart_p, p, "Cart", "🛒")
        self.lbl_cart_count = Label(hdr, text="0 items",
                                    font=("Segoe UI", 9),
                                    bg=p["header_bg"],
                                    fg=p["hdr_sub"])
        self.lbl_cart_count.pack(side=RIGHT, padx=14, fill=Y)

        Label(cart_p, text="  Select a cart row to edit quantity",
              font=("Segoe UI", 8), bg=p["panel_border"],
              fg=p["text_dim"], anchor=W).pack(fill=X, ipady=2)

        tbl_f = Frame(cart_p, bg=p["panel_bg"])
        tbl_f.pack(fill=BOTH, expand=True)
        tbl_f.rowconfigure(0, weight=1)
        tbl_f.columnconfigure(0, weight=1)

        sy = ttk.Scrollbar(tbl_f, orient=VERTICAL,
                           style="Slim.Vertical.TScrollbar")
        sy.grid(row=0, column=1, sticky="ns")
        sx = ttk.Scrollbar(tbl_f, orient=HORIZONTAL,
                           style="Slim.Horizontal.TScrollbar")
        sx.grid(row=1, column=0, sticky="ew")

        self.CartTable = ttk.Treeview(
            tbl_f, style="T.Treeview",
            columns=("pid", "name", "price", "qty", "total"),
            yscrollcommand=sy.set,
            selectmode="browse", show="headings",
        )
        sy.config(command=self.CartTable.yview)
        sx.config(command=self.CartTable.xview)
        self.CartTable.grid(row=0, column=0, sticky="nsew")

        for col_id, txt, w, anchor in [
            ("pid",   "ID",     45, CENTER),
            ("name",  "Item",  140, W),
            ("price", "Rate",   70, CENTER),
            ("qty",   "Qty",    45, CENTER),
            ("total", "Total",  80, CENTER),
        ]:
            self.CartTable.heading(col_id, text=txt)
            self.CartTable.column(col_id, width=w, anchor=anchor)

        self.CartTable.bind("<ButtonRelease-1>", self.get_data_cart)

        # ── Calculator ────────────────────────────────────────────
        calc_p = Panel(row, p, row=0, column=1, sticky="nsew")
        calc_p.rowconfigure(1, weight=1)
        calc_p.columnconfigure(0, weight=1)
        SectionBar(calc_p, p, "Calculator", "🖩")

        cf = Frame(calc_p, bg=p["panel_bg"])
        cf.pack(fill=BOTH, expand=True, padx=8, pady=8)
        for c in range(4):
            cf.columnconfigure(c, weight=1)
        for r in range(5):
            cf.rowconfigure(r + 1, weight=1)

        disp = Entry(cf, textvariable=self.var_cal,
                     font=("Consolas", 15, "bold"),
                     bg=p["input_bg"], fg="#FF4500",
                     insertbackground=p["text"],
                     state="readonly", justify=RIGHT,
                     relief="flat",
                     highlightthickness=1,
                     highlightbackground=p["input_border"],
                     highlightcolor=p["input_focus"])
        disp.grid(row=0, column=0, columnspan=4,
                  sticky="ew", ipady=10, pady=(0, 6))

        # rows: (label, value, style)
        grid = [
            [("7","7","CNum"),("8","8","CNum"),("9","9","CNum"),("+","+","COp")],
            [("4","4","CNum"),("5","5","CNum"),("6","6","CNum"),("-","-","COp")],
            [("1","1","CNum"),("2","2","CNum"),("3","3","CNum"),("×","*","COp")],
            [("0","0","CNum"),("C","C","CClr"),("=","=","CEq"),("÷","/","COp")],
        ]
        for r, btn_row in enumerate(grid):
            for c, (lbl, val, st) in enumerate(btn_row):
                cmd = (self.clear_cal if val == "C" else
                       self.perform_cal if val == "=" else
                       lambda v=val: self.get_input(v))
                ttk.Button(cf, text=lbl, command=cmd,
                           style=f"{st}.TButton").grid(
                    row=r + 1, column=c,
                    sticky="nsew", padx=2, pady=2)

    def _build_add_cart(self, col):
        p = self.p
        ap = Panel(col, p, row=2, column=0, sticky="ew")
        ap.columnconfigure(0, weight=1)
        SectionBar(ap, p, "Add / Update Item", "✚")

        body = Frame(ap, bg=p["panel_bg"])
        body.pack(fill=X, padx=12, pady=10)
        for i in range(6):
            body.columnconfigure(i, weight=1)

        for c, lbl, var, ro in [
            (0, "Product Name",  self.var_pname, True),
            (2, "Unit Price",    self.var_price, True),
            (4, "Quantity",      self.var_qty,   False),
        ]:
            Label(body, text=lbl, font=("Segoe UI", 9, "bold"),
                  bg=p["panel_bg"], fg=p["text_muted"]).grid(
                row=0, column=c, columnspan=2,
                sticky=W, padx=(0, 8))
            StyledEntry(body, p, var, readonly=ro).grid(
                row=1, column=c, columnspan=2, sticky="ew",
                ipady=7, padx=(0, 8), pady=(3, 0))

        bot = Frame(ap, bg=p["panel_bg"])
        bot.pack(fill=X, padx=12, pady=(4, 10))
        bot.columnconfigure(1, weight=1)

        self.lbl_inStock = Label(bot, text="Stock: —",
                                 font=("Segoe UI", 10, "bold"),
                                 bg=p["panel_bg"], fg=p["green"])
        self.lbl_inStock.grid(row=0, column=0, sticky=W)

        ttk.Button(bot, text="✕  Clear",
                   command=self.clear_cart,
                   style="Warning.TButton").grid(
            row=0, column=2, padx=(0, 6))
        ttk.Button(bot, text="＋  Add / Update",
                   command=self.add_update_cart,
                   style="Primary.TButton").grid(
            row=0, column=3)

    # ══════════════════════════════════════════════════════════════
    #  RIGHT – Receipt
    # ══════════════════════════════════════════════════════════════
    def _build_receipt(self, body):

        p = self.p

        col = Frame(body, bg=p["win_bg"])
        col.grid(row=0, column=2, sticky="nsew")

        # ================= RECEIPT PANEL =================

        rp = Panel(col, p)
        rp.pack = None

        rp.grid_rowconfigure = None

        SectionBar(rp, p, "Customer Receipt", "🧾")

        content = Frame(rp, bg=p["panel_bg"])
        content.pack(fill=BOTH, expand=True, padx=4, pady=4)

        sy = ttk.Scrollbar(
            content,
            orient=VERTICAL,
            style="Slim.Vertical.TScrollbar"
        )
        sy.pack(side=RIGHT, fill=Y)

        self.txt_bill_area = Text(
            content,
            font=("Consolas", 9),
            bg=p["receipt_bg"],
            fg=p["receipt_fg"],
            insertbackground=p["receipt_fg"],
            relief="flat",
            padx=14,
            pady=10,
            yscrollcommand=sy.set,
            wrap=NONE,
            cursor="arrow",
        )

        self.txt_bill_area.pack(
            side=LEFT,
            fill=BOTH,
            expand=True
        )

        sy.config(command=self.txt_bill_area.yview)

        self.txt_bill_area.tag_configure(
            "hl",
            foreground=p["receipt_hl"],
            font=("Consolas", 9, "bold")
        )

        # ================= SUMMARY TILES =================

        tiles_frame = Frame(col, bg=p["win_bg"])
        tiles_frame.grid(row=1, column=0, sticky="ew", padx=8, pady=8)
        for i in range(3):
            tiles_frame.columnconfigure(i, weight=0)

        tile_data = [
            ("Bill Amount", "tile1_bg", "tile1_fg", "lbl_amnt"),
            ("Discount 5%", "tile2_bg", "tile2_fg", "lbl_discount"),
            ("Net Payable", "tile3_bg", "tile3_fg", "lbl_net_pay"),
        ]

        for i, (title, bg_k, fg_k, attr) in enumerate(tile_data):

            t = Frame(
                tiles_frame,
                bg=p[bg_k],
                highlightbackground=p["panel_border"],
                highlightthickness=1
            )

            t.grid(
                row=0,
                column=i,
                sticky="ew",
                padx=(0, 6 if i < 2 else 0),
            )

            Label(
                t,
                text=title,
                font=("Segoe UI", 8, "bold"),
                bg=p[bg_k],
                fg=p[fg_k]
            ).pack(pady=(8, 2))

            lbl = Label(
                t,
                text="৳  0.00",
                font=("Segoe UI", 16, "bold"),
                bg=p[bg_k],
                fg=p[fg_k]
            )

            lbl.pack(pady=(0, 8))

            setattr(self, attr, lbl)

        # ================= ACTION BUTTONS =================

        act = Frame(col, bg=p["win_bg"])
        act.grid(row=2, column=0, sticky="ew")

        for i in range(3):
            act.columnconfigure(i, weight=0)

        buttons = [
            ("🖨  Print", self.trigger_print, "Ghost.TButton"),
            ("🗑  Clear All", self.clear_all, "Warning.TButton"),
            ("💾  Generate Bill", self.generate_bill, "Success.TButton"),
        ]

        for i, (txt, cmd, st) in enumerate(buttons):
            ttk.Button(
                act,
                text=txt,
                command=cmd,
                style=st
            ).grid(
                row=0,
                column=i,
                sticky="w",         # <-- Changed from "ew" to "" so they don't stretch horizontally
                padx=6,            # <-- Even padding on both sides looks better for centered buttons
                ipady=1,
                ipadx=0            # <-- Optional: explicit small horizontal padding inside the button
            )
        # ══════════════════════════════════════════════════════════════
        #  BUSINESS LOGIC
        # ══════════════════════════════════════════════════════════════
    def get_input(self, v):
        self.var_cal.set(self.var_cal.get() + str(v))

    def clear_cal(self):
        self.var_cal.set("")

    def perform_cal(self):
        try:
            self.var_cal.set(eval(self.var_cal.get()))
        except Exception:
            messagebox.showerror("Calculator", "Invalid expression",
                                parent=self.root)
            self.var_cal.set("")

    # ── DB helpers ────────────────────────────────────────────────
    def show(self):
        con = sqlite3.connect("ims.db")
        try:
            rows = con.execute(
                "SELECT pid,name,price,qty,status FROM product "
                "WHERE status='Active'"
            ).fetchall()
            self.product_Table.delete(*self.product_Table.get_children())
            for i, r in enumerate(rows):
                tag = "odd" if i % 2 else "even"
                self.product_Table.insert("", END, values=r, tags=(tag,))
        except Exception as ex:
            messagebox.showerror("DB Error", str(ex), parent=self.root)
        finally:
            con.close()

    def search(self):
        q = self.var_search.get().strip()
        if not q or q == "Search products…":
            messagebox.showerror("Search",
                                "Enter a product name to search.",
                                parent=self.root)
            return
        con = sqlite3.connect("ims.db")
        try:
            rows = con.execute(
                "SELECT pid,name,price,qty,status FROM product "
                "WHERE name LIKE ? AND status='Active'",
                (f"%{q}%",),
            ).fetchall()
            if rows:
                self.product_Table.delete(*self.product_Table.get_children())
                for i, r in enumerate(rows):
                    tag = "odd" if i % 2 else "even"
                    self.product_Table.insert("", END, values=r, tags=(tag,))
            else:
                messagebox.showinfo("Search",
                                    "No matching products found.",
                                    parent=self.root)
        except Exception as ex:
            messagebox.showerror("DB Error", str(ex), parent=self.root)
        finally:
            con.close()

    def get_data(self, ev):
        f = self.product_Table.focus()
        row = self.product_Table.item(f)["values"]
        if not row:
            return
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_inStock.config(text=f"Stock: {row[3]}")
        self.var_stock.set(row[3])
        self.var_qty.set("1")

    def get_data_cart(self, ev):
        f = self.CartTable.focus()
        row = self.CartTable.item(f)["values"]
        if not row:
            return
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])
        # FIX: stock not in CartTable — look up from cart_list
        stock = ""
        for item in self.cart_list:
            if str(item[0]) == str(row[0]):
                stock = item[4]
                break
        self.lbl_inStock.config(text=f"Stock: {stock}")
        self.var_stock.set(stock)

    def add_update_cart(self):
        if not self.var_pid.get():
            messagebox.showerror("Cart", "Select a product first.",
                                parent=self.root)
            return
        if not self.var_qty.get():
            messagebox.showerror("Cart", "Quantity is required.",
                                parent=self.root)
            return
        try:
            qty   = int(self.var_qty.get())
            stock = int(self.var_stock.get())
        except ValueError:
            messagebox.showerror("Cart", "Quantity must be a whole number.",
                                parent=self.root)
            return
        if qty > stock:
            messagebox.showerror("Cart",
                                f"Only {stock} units available.",
                                parent=self.root)
            return

        entry = [self.var_pid.get(), self.var_pname.get(),
                self.var_price.get(), str(qty), str(stock)]

        present, idx = False, 0
        for i, r in enumerate(self.cart_list):
            if r[0] == self.var_pid.get():
                present, idx = True, i
                break

        if present:
            ok = messagebox.askyesno(
                "Update Cart",
                f"'{self.var_pname.get()}' is already in the cart.\n"
                "Update quantity / remove?",
                parent=self.root,
            )
            if ok:
                if qty == 0:
                    self.cart_list.pop(idx)
                else:
                    self.cart_list[idx][3] = str(qty)
        else:
            self.cart_list.append(entry)

        self.show_cart()
        self.bill_update()

    def show_cart(self):
        self.CartTable.delete(*self.CartTable.get_children())
        for r in self.cart_list:
            total = float(r[2]) * int(r[3])
            self.CartTable.insert("", END,
                values=(r[0], r[1], r[2], r[3], f"{total:.2f}"))

    def bill_update(self):
        self.bill_amnt = sum(
            float(r[2]) * int(r[3]) for r in self.cart_list)
        self.discount  = self.bill_amnt * 0.05
        self.net_pay   = self.bill_amnt - self.discount
        self.lbl_amnt.config(text=f"৳  {self.bill_amnt:.2f}")
        self.lbl_discount.config(text=f"৳  {self.discount:.2f}")
        self.lbl_net_pay.config(text=f"৳  {self.net_pay:.2f}")
        n = len(self.cart_list)
        self.lbl_cart_count.config(
            text=f"{n} item{'s' if n != 1 else ''}")

    def generate_bill(self):
        if not self.var_cname.get() or not self.var_contact.get():
            messagebox.showerror("Bill",
                                "Customer details are required.",
                                parent=self.root)
            return
        if not self.cart_list:
            messagebox.showerror("Bill", "Cart is empty.",
                                parent=self.root)
            return
        self.bill_top()
        self.bill_middle()
        self.bill_bottom()
        os.makedirs("bill", exist_ok=True)
        with open(f"bill/{self.invoice}.txt", "w") as f:
            f.write(self.txt_bill_area.get("1.0", END))
        messagebox.showinfo("Saved",
                            f"Bill #{self.invoice} saved successfully.",
                            parent=self.root)

    def bill_top(self):
        self.invoice = (int(time.strftime("%H%M%S")) +
                        int(time.strftime("%d%m%Y")))
        W = 42
        sep = "─" * W
        top = (
            f"\n{'':>2}{'IMS — Inventory Management':^{W-4}}\n"
            f"{'':>2}{'Phone: 09899098989  ·  Dhaka-1200':^{W-4}}\n"
            f"{sep}\n"
            f"  Customer : {self.var_cname.get()}\n"
            f"  Phone    : {self.var_contact.get()}\n"
            f"  Bill No. : {self.invoice}\n"
            f"  Date     : {time.strftime('%d %b %Y  %H:%M')}\n"
            f"{sep}\n"
            f"  {'Item':<20} {'Qty':>4}  {'Rate':>7}  {'Total':>8}\n"
            f"{sep}\n"
        )
        self.txt_bill_area.config(state=NORMAL)
        self.txt_bill_area.delete("1.0", END)
        self.txt_bill_area.insert("1.0", top)
        # highlight shop name
        self.txt_bill_area.tag_add("hl", "2.0", "2.end")

    def bill_middle(self):
        for r in self.cart_list:
            name  = r[1][:20]
            qty   = int(r[3])
            rate  = float(r[2])
            total = rate * qty
            self.txt_bill_area.insert(
                END,
                f"  {name:<20} {qty:>4}  {rate:>7.2f}  {total:>8.2f}\n"
            )

    def bill_bottom(self):
        W = 42
        sep = "─" * W
        bot = (
            f"{sep}\n"
            f"  {'Bill Amount':<28} {self.bill_amnt:>9.2f}\n"
            f"  {'Discount (5%)':<28} {self.discount:>9.2f}\n"
            f"  {'Net Payable':<28} {self.net_pay:>9.2f}\n"
            f"{sep}\n"
            f"{'Thank you for shopping at IMS!':^{W}}\n\n"
        )
        self.txt_bill_area.insert(END, bot)
        # highlight totals
        start = float(self.txt_bill_area.index("end-1c"))
        self.txt_bill_area.config(state=DISABLED)

    def clear_cart(self):
        self.var_pid.set("")
        self.var_pname.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.lbl_inStock.config(text="Stock: —")
        self.var_stock.set("")

    def clear_all(self):
        self.cart_list.clear()
        self.var_cname.set("")
        self.var_contact.set("")
        self.txt_bill_area.config(state=NORMAL)
        self.txt_bill_area.delete("1.0", END)
        self.bill_update()
        self.clear_cart()
        self.var_search.set("")
        self.show()
        self.show_cart()

    def update_clock(self):
        self.lbl_clock.config(
            text=time.strftime("  📅  %A, %d %B %Y      🕐  %H:%M:%S  ")
        )
        self.lbl_clock.after(1000, self.update_clock)

    def toggle_theme(self):
        new = "light" if self.theme_mode == "dark" else "dark"
        self.root.destroy()
        import subprocess
        subprocess.Popen([sys.executable, __file__, "--theme", new])

    def logout(self):
        self.root.destroy()
        from login import LoginWindow
        r = Tk()
        LoginWindow(r)
        r.mainloop()

    def trigger_print(self):
        # Replace 'path_to_bill.txt' with the actual variable holding your file path
        file_path = os.path.join(f"bill/{self.invoice}.txt")
        
        if not os.path.exists(file_path):
            print(f"Error: File {file_path} not found.")
            return

        current_os = platform.system()

        try:
            if current_os == "Windows":
                # Uses the Windows shell 'print' command verb
                os.startfile(file_path, "print")
            elif current_os == "Darwin":  # Darwin is macOS
                # 'lp' sends the file directly to the default system printer
                subprocess.run(["lp", file_path], check=True)
            else:
                # Linux backup
                subprocess.run(["lpr", file_path], check=True)
                
        except Exception as e:
            print(f"Failed to print: {e}")
# ══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    theme = "dark"
    if "--theme" in sys.argv:
        i = sys.argv.index("--theme")
        if i + 1 < len(sys.argv):
            theme = sys.argv[i + 1]
    root = Tk()
    BillClass(root, theme=theme)
    root.mainloop()
