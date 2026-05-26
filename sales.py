from sqlite3.dbapi2 import Cursor, connect
from tkinter import *
from PIL import ImageTk
import PIL.Image
from tkinter import ttk, messagebox
import sqlite3
import os

from ui_theme import apply_theme, colors


class salesClass:
    def __init__(self, root, show_menu=None):
        self.root = root
        self.show_menu = show_menu
        self.palette = colors()

        if isinstance(self.root, (Tk, Toplevel)):
            apply_theme(self.root)
            self.root.geometry("1150x560+140+90")
            self.root.minsize(1000, 520)
            self.root.title("Sales | IMS | Developed by Amit")
            self.root.config(bg=self.palette["bg"])
            photo = PhotoImage(file=os.path.join("images", "i1.png"))
            self.root.iconphoto(False, photo)
            self.root.focus_force()
        #root.overrideredirect(1)

        #----Variables----
        self.var_invoice = StringVar()
        self.bill_list=[]

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(3, weight=1)

        header_frame = Frame(self.root, bg=self.palette["bg"])
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(10, 5))
        header_frame.columnconfigure(1, weight=1)

        if self.show_menu:
            btn_menu = ttk.Button(
                header_frame,
                text="Menu",
                command=self.show_menu,
                style="Sidebar.TButton",
            )
            btn_menu.grid(row=0, column=0, sticky="w")

        title = Label(header_frame, text="View Customer Bill", font=("goudy old style", 20, "bold"), bg="purple4", fg="white", bd=1,relief=RIDGE)
        title.grid(row=0, column=1, sticky="ew", padx=10)

        search_frame = Frame(self.root, bg=self.palette["bg"])
        search_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(5, 10))
        search_frame.columnconfigure(1, weight=1)

        lbl_invoice = Label(search_frame, text="Invoice no.", font=("times new roman", 15), bg="white", fg="black")
        lbl_invoice.grid(row=0, column=0, sticky="w", padx=5)

        txt_invoice = Entry(search_frame, textvariable=self.var_invoice, font=("times new roman", 15), bg="azure2", fg="black")
        txt_invoice.grid(row=0, column=1, sticky="ew", padx=5)

        btn_search = ttk.Button(search_frame, command=self.search, text="Search", style="Accent.TButton")
        btn_search.grid(row=0, column=2, padx=5)
        btn_clear = ttk.Button(search_frame, command=self.clear, text="Clear", style="Warning.TButton")
        btn_clear.grid(row=0, column=3, padx=5)

        content_frame = Frame(self.root, bg=self.palette["bg"])
        content_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=(0, 15))
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=2)
        content_frame.columnconfigure(2, weight=1)
        content_frame.rowconfigure(0, weight=1)

        sales_frame = Frame(content_frame, bd=3, relief=RIDGE, bg="white")
        sales_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        scrolly = Scrollbar(sales_frame, orient= VERTICAL)

        self.Sales_List = Listbox(sales_frame,font=("goudy old style", 15), bg="white", fg="black", yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT, fill=Y)
        scrolly.config(command=self.Sales_List.yview)
        self.Sales_List.pack(fill=BOTH, expand=1)
        self.Sales_List.bind("<ButtonRelease-1>", self.get_data)

        #---Bill Area---

        bill_Frame = Frame(content_frame, bd=3, relief=RIDGE, bg="white")
        bill_Frame.grid(row=0, column=1, sticky="nsew", padx=(0, 10))
        
        title22 = Label(bill_Frame, text="Customer Bill Area", font=("goudy old style", 20), bg="spring green").pack(side=TOP, fill=X)

        scrolly2 = Scrollbar(bill_Frame, orient= VERTICAL)

        self.bill_area = Text(bill_Frame, font=("courier new", 15), bg="azure2", fg="black", yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT, fill=Y)
        scrolly2.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH, expand=1)

        #---Images---

        self.im1= PIL.Image.open(os.path.join("images", "sal1.png"))
        self.im1=self.im1.resize((250,200),PIL.Image.Resampling.LANCZOS)
        self.im1=ImageTk.PhotoImage(self.im1)

        self.lbl_im1 = Label(content_frame, image=self.im1, bg="white")
        self.lbl_im1.grid(row=0, column=2, sticky="nsew")
        
        self.show()
    #############################################################33333

    def show(self):
        del self.bill_list[:]
        self.Sales_List.delete(0, END)

        for i in os.listdir("bill/"):
            if i.split('.') [-1] == 'txt':
                self.Sales_List.insert(END,i)
                self.bill_list.append(i.split('.')[0])

    def get_data(self, ev):
        index_ = self.Sales_List.curselection()
        file_name=self.Sales_List.get(index_)
        self.bill_area.delete('1.0', END)
        fp=open(f'bill/{file_name}', 'r')
        for i in fp:
            self.bill_area.insert(END, i)
        fp.close()

    def search(self):
        if self.var_invoice.get()=="":
            messagebox.showerror("Error", "Invoice no. should be required", parent=self.root)

        else:
            if self.var_invoice.get() in self.bill_list:
                fp=open(f'bill/{self.var_invoice.get()}.txt', 'r')
                self.bill_area.delete('1.0', END)
                for i in fp:
                    self.bill_area.insert(END, i)
                fp.close()
            else:
                messagebox.showerror("Error", "Invalid invoice No.", parent=self.root)


    def clear(self):
        self.show()
        self.bill_area.delete('1.0', END)




if __name__ =="__main__":
    root = Tk()
    obj = salesClass(root)
    root.mainloop()        