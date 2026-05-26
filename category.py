from sqlite3.dbapi2 import Cursor, connect
from tkinter import *
from tkinter.font import BOLD
from PIL import ImageTk
import PIL.Image
from tkinter import ttk, messagebox
import sqlite3
import os

from ui_theme import apply_theme, colors


class categoryClass:
    def __init__(self, root, show_menu=None):
        self.root = root
        self.show_menu = show_menu
        self.palette = colors()

        if isinstance(self.root, (Tk, Toplevel)):
            apply_theme(self.root)
            self.root.geometry("1150x560+140+90")
            self.root.minsize(1000, 520)
            self.root.title("Category | IMS | Developed by Amit")
            self.root.config(bg=self.palette["bg"])
            photo = PhotoImage(file=os.path.join("images", "i1.png"))
            self.root.iconphoto(False, photo)
            self.root.focus_force()
        #root.overrideredirect(1)

        #============Variables===========

        self.var_cat_id=StringVar()
        self.var_name=StringVar()

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

        title = Label(header_frame, text="Manage Product Category", font=("goudy old style", 20, "bold"), bg="#184a45", fg="white", bd=0,relief=RIDGE)
        title.grid(row=0, column=1, sticky="ew", padx=10)

        form_frame = Frame(self.root, bg=self.palette["bg"])
        form_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(5, 10))
        form_frame.columnconfigure(1, weight=1)

        lbl_name = Label(form_frame, text="Enter Category Name", font=("goudy old style", 20, "bold"), bg="white", fg="black")
        lbl_name.grid(row=0, column=0, sticky="w", padx=5)
        txt_name = Entry(form_frame, textvariable=self.var_name, font=("goudy old style", 18), bg="azure2", fg="black")
        txt_name.grid(row=0, column=1, sticky="ew", padx=5)

        btn_add = ttk.Button(form_frame, command=self.add, text="Add", style="Accent.TButton")
        btn_add.grid(row=0, column=2, padx=5)
        btn_delete = ttk.Button(form_frame, command=self.delete, text="Delete", style="Danger.TButton")
        btn_delete.grid(row=0, column=3, padx=5)

        cat_frame = Frame(self.root, bd=3, relief=RIDGE)
        cat_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 10))

        scrolly = Scrollbar(cat_frame, orient= VERTICAL)
        scrollx = Scrollbar(cat_frame, orient= HORIZONTAL)



        self.CategoryTable = ttk.Treeview(cat_frame, columns=("cid", "name"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.pack(side=BOTTOM, fill=X)
        scrollx.config(command=self.CategoryTable.xview)
        scrolly.config(command=self.CategoryTable.yview)

        self.CategoryTable.heading("cid", text="Category ID")
        self.CategoryTable.heading("name", text="Name")
        self.CategoryTable["show"] = "headings"

        self.CategoryTable.column("cid", width=90)
        self.CategoryTable.column("name", width=100)
        self.CategoryTable.pack(expand=1, fill=BOTH)
        self.CategoryTable.bind("<ButtonRelease-1>", self.get_data)

        #====Images====
        self.im1= PIL.Image.open(os.path.join("images", "cat1.png"))
        self.im1=self.im1.resize((490,240),PIL.Image.Resampling.LANCZOS)
        self.im1=ImageTk.PhotoImage(self.im1)

        images_frame = Frame(self.root, bg=self.palette["bg"])
        images_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=(0, 15))
        images_frame.columnconfigure(0, weight=1)
        images_frame.columnconfigure(1, weight=1)

        self.lbl_im1 = Label(images_frame, image=self.im1, bd=1,relief=RAISED, bg="white")
        self.lbl_im1.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.im2= PIL.Image.open(os.path.join("images", "cat2.png"))
        self.im2=self.im2.resize((490,240),PIL.Image.Resampling.LANCZOS)
        self.im2=ImageTk.PhotoImage(self.im2)

        self.lbl_im2 = Label(images_frame, image=self.im2, bd=1,relief=RAISED, bg="white")
        self.lbl_im2.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        self.show()
    ######################Function############################
      
    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_name.get()=="":
                messagebox.showerror("Error", "Category name should be required", parent=self.root)
            else:
                cur.execute("Select * from category where name=?",(self.var_name.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This Category already present, try different", parent=self.root)
                else:
                    cur.execute("Insert into category(name) values(?)", (self.var_name.get(),))
                    con.commit()
                    messagebox.showinfo("Success", "Category Added Successfully", parent=self.root)
                    self.show()
                    self.var_name.set("")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("Select * from category")
            rows=cur.fetchall()
            self.CategoryTable.delete(*self.CategoryTable.get_children())
            for row in rows:
                self.CategoryTable.insert('',END,values=row)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def get_data(self, ev):
        f=self.CategoryTable.focus()
        content=(self.CategoryTable.item(f))
        row=content['values']

        self.var_cat_id.set(row[0])
        self.var_name.set(row[1])

    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_cat_id.get()=="":
                messagebox.showerror("Error", "Please select category from the list", parent=self.root)
            else:
                cur.execute("Select * from category where cid=?",(self.var_cat_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Error, Please try again", parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?", parent=self.root)
                    if op==True:
                        cur.execute("delete from category where cid=?",(self.var_cat_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Category Deleted Successfully", parent=self.root)
                        self.show()
                        self.var_cat_id.set("")
                        self.var_name.set("")

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


if __name__ =="__main__":
    root = Tk()
    obj = categoryClass(root)
    root.mainloop()