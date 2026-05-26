from tkinter import ttk


def colors(theme="light"):
    if theme == "dark":
        return {
            "bg": "#0b1120",
            "panel": "#111827",
            "accent": "#60a5fa",
            "accent_alt": "#22d3ee",
            "text": "#e5e7eb",
            "muted": "#9ca3af",
            "sidebar": "#0f172a",
            "sidebar_text": "#e2e8f0",
            "sidebar_hover": "#1f2937",
            "warning": "#fbbf24",
            "danger": "#f87171",
            "success": "#34d399",
            "button_text": "#0b1120",
        }

    return {
        "bg": "#f4f6fb",
        "panel": "#ffffff",
        "accent": "#2563eb",
        "accent_alt": "#0ea5a7",
        "text": "#1f2a44",
        "muted": "#6b7280",
        "sidebar": "#0f172a",
        "sidebar_text": "#e2e8f0",
        "sidebar_hover": "#1e293b",
        "warning": "#f59e0b",
        "danger": "#ef4444",
        "success": "#10b981",
        "button_text": "#ffffff",
    }


def apply_theme(root, theme="light"):
    palette = colors(theme)
    root.configure(bg=palette["bg"])
    root.option_add("*Font", ("Helvetica Neue", 11))

    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass

    style.configure(
        "TButton",
        padding=6,
        relief="flat",
        background=palette["accent"],
        foreground=palette["button_text"],
        font=("Helvetica Neue", 11, "bold"),
    )
    style.map(
        "TButton",
        background=[("active", palette["accent_alt"])],
        foreground=[("active", palette["button_text"])],
    )
    style.configure("TLabel", background=palette["bg"], foreground=palette["text"])
    style.configure("TFrame", background=palette["bg"])
    style.configure(
        "Accent.TButton",
        background=palette["accent"],
        foreground=palette["button_text"],
        font=("Helvetica Neue", 12, "bold"),
    )
    style.map(
        "Accent.TButton",
        background=[("active", palette["accent_alt"])],
        foreground=[("active", palette["button_text"])],
    )
    style.configure(
        "Danger.TButton",
        background=palette["danger"],
        foreground=palette["button_text"],
        font=("Helvetica Neue", 11, "bold"),
    )
    style.map(
        "Danger.TButton",
        background=[("active", palette["danger"])],
        foreground=[("active", palette["button_text"])],
    )
    style.configure(
        "Warning.TButton",
        background=palette["warning"],
        foreground=palette["button_text"],
        font=("Helvetica Neue", 11, "bold"),
    )
    style.map(
        "Warning.TButton",
        background=[("active", palette["warning"])],
        foreground=[("active", palette["button_text"])],
    )
    style.configure(
        "AccentAlt.TButton",
        background=palette["accent_alt"],
        foreground=palette["button_text"],
        font=("Helvetica Neue", 11, "bold"),
    )
    style.map(
        "AccentAlt.TButton",
        background=[("active", palette["accent_alt"])],
        foreground=[("active", palette["button_text"])],
    )
    style.configure(
        "Sidebar.TButton",
        background=palette["sidebar"],
        foreground=palette["sidebar_text"],
        font=("Helvetica Neue", 12, "bold"),
    )
    style.map(
        "Sidebar.TButton",
        background=[("active", palette["sidebar_hover"])],
        foreground=[("active", palette["sidebar_text"])],
    )
    style.configure(
        "Calc.TButton",
        background=palette["panel"],
        foreground=palette["text"],
        font=("Helvetica Neue", 12, "bold"),
    )
    style.map(
        "Calc.TButton",
        background=[("active", palette["panel"])],
        foreground=[("active", palette["text"])],
    )
    style.configure(
        "CalcOp.TButton",
        background=palette["accent_alt"],
        foreground=palette["button_text"],
        font=("Helvetica Neue", 12, "bold"),
    )
    style.map(
        "CalcOp.TButton",
        background=[("active", palette["accent_alt"])],
        foreground=[("active", palette["button_text"])],
    )
    style.configure(
        "CalcDanger.TButton",
        background=palette["danger"],
        foreground=palette["button_text"],
        font=("Helvetica Neue", 12, "bold"),
    )
    style.map(
        "CalcDanger.TButton",
        background=[("active", palette["danger"])],
        foreground=[("active", palette["button_text"])],
    )
    style.configure(
        "CalcSuccess.TButton",
        background=palette["success"],
        foreground=palette["button_text"],
        font=("Helvetica Neue", 12, "bold"),
    )
    style.map(
        "CalcSuccess.TButton",
        background=[("active", palette["success"])],
        foreground=[("active", palette["button_text"])],
    )
    style.map(
        "Danger.TButton",
        background=[("active", palette["danger"])],
        foreground=[("active", palette["button_text"])],
    )
    style.configure("Ghost.TButton", background=palette["panel"], foreground=palette["text"])
    return palette
