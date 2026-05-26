from sqlite3.dbapi2 import Cursor, connect
from tkinter import *
from PIL import ImageTk
import PIL.Image
from tkinter import ttk, messagebox
import sqlite3
import os

from ui_theme import apply_theme, colors


class supplierClass:
    def __init__(self, root, show_menu=None):
        self.root = root
        self.show_menu = show_menu
        self.palette = colors()

        if isinstance(self.root, (Tk, Toplevel)):
            apply_theme(self.root)
            self.root.geometry("1150x560+140+90")
            self.root.minsize(1000, 520)
            self.root.title("Supplier | IMS | Developed by Amit")
            self.root.config(bg=self.palette["bg"])
            photo = PhotoImage(file=os.path.join("images", "i1.png"))
            self.root.iconphoto(False, photo)
            self.root.focus_force()
        #root.overrideredirect(1)

        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        #All variables

        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_sup_invoice = StringVar()
        self.var_name = StringVar()
        self.var_contact = StringVar()



        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(4, weight=1)

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

        title = Label(header_frame, text="Supplier Details", font=("goudy old style", 20, "bold"), bg="#0f4d7d", fg="white")
        title.grid(row=0, column=1, sticky="ew", padx=10)

        search_frame = Frame(self.root, bg=self.palette["bg"])
        search_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(5, 10))
        search_frame.columnconfigure(1, weight=1)

        lbl_search = Label(search_frame, text="Invoice No.", bg="white", fg="black", font=("goudy old style", 15))
        lbl_search.grid(row=0, column=0, sticky="w", padx=5)
        txt_search = Entry(search_frame, textvariable=self.var_searchtxt, font=("goudy old style", 15), bg="azure2", fg="black")
        txt_search.grid(row=0, column=1, sticky="ew", padx=5)
        btn_search = ttk.Button(search_frame, command=self.search, text="Search", style="Accent.TButton")
        btn_search.grid(row=0, column=2, padx=5)

        form_frame = Frame(self.root, bg=self.palette["bg"])
        form_frame.grid(row=2, column=0, sticky="ew", padx=20)
        form_frame.columnconfigure(0, weight=0)  # Label column stays tight to its text size
        form_frame.columnconfigure(1, weight=1)


        lbl_supplier_invoice = Label(form_frame, text="Invoice No.", font=("goudy old style", 15), bg="white", fg="black")
        lbl_supplier_invoice.grid(row=0, column=0, sticky="w", padx=5, pady=4)
        txt__supplier_invoice = Entry(form_frame, textvariable=self.var_sup_invoice, font=("goudy old style", 15), bg ="azure2", fg="black")
        txt__supplier_invoice.grid(row=0, column=1, sticky="ew", padx=5, pady=4)

        lbl_name = Label(form_frame, text="Supplier Name", font=("goudy old style", 15), bg="white", fg="black")
        lbl_name.grid(row=0, column=2, sticky="w", padx=5, pady=4)
        txt_name = Entry(form_frame, textvariable=self.var_name, font=("goudy old style", 15), bg ="azure2", fg="black")
        txt_name.grid(row=0, column=3, sticky="ew", padx=5, pady=4)

        lbl_contact = Label(form_frame, text="Contact", font=("goudy old style", 15), bg="white", fg="black")
        lbl_contact.grid(row=1, column=0, sticky="w", padx=5, pady=4)
        txt_contact = Entry(form_frame, textvariable=self.var_contact, font=("goudy old style", 15), bg ="azure2", fg="black")
        txt_contact.grid(row=1, column=1, sticky="ew", padx=5, pady=4)

        lbl_desc = Label(form_frame, text="Description", font=("goudy old style", 15), bg="white", fg="black")
        lbl_desc.grid(row=2, column=0, sticky="nw", padx=5, pady=4)
        self.txt_desc = Text(form_frame, font=("goudy old style", 15), bg ="azure2", fg="black", height=4)
        self.txt_desc.grid(row=2, column=1, columnspan=3, sticky="ew", padx=5, pady=4)

        btn_frame = Frame(self.root, bg=self.palette["bg"])
        btn_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=(8, 10))
        for col in range(5):
            btn_frame.columnconfigure(col, weight=1)

        btn_add = ttk.Button(btn_frame, command=self.add, text="Save", style="Accent.TButton")
        btn_add.grid(row=0, column=0, padx=5, pady=2, sticky="ew")

        btn_update = ttk.Button(btn_frame, command=self.update, text="Update", style="AccentAlt.TButton")
        btn_update.grid(row=0, column=1, padx=5, pady=2, sticky="ew")

        btn_delete = ttk.Button(btn_frame, command=self.delete, text="Delete", style="Danger.TButton")
        btn_delete.grid(row=0, column=2, padx=5, pady=2, sticky="ew")

        btn_clear = ttk.Button(btn_frame, command=self.clear, text="Clear", style="Warning.TButton")
        btn_clear.grid(row=0, column=3, padx=5, pady=2, sticky="ew")

        btn_exit = ttk.Button(btn_frame, text="Exit", command=self.exit, style="Sidebar.TButton")
        btn_exit.grid(row=0, column=4, padx=5, pady=2, sticky="ew")

        emp_frame = Frame(self.root, bd=3, relief=RIDGE)
        emp_frame.grid(row=4, column=0, sticky="nsew", padx=20, pady=(0, 15))

        scrolly = Scrollbar(emp_frame, orient= VERTICAL)
        scrollx = Scrollbar(emp_frame, orient= HORIZONTAL)



        self.SupplierTable = ttk.Treeview(emp_frame, columns=("invoice", "name", "contact", "desc"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.pack(side=BOTTOM, fill=X)
        scrollx.config(command=self.SupplierTable.xview)
        scrolly.config(command=self.SupplierTable.yview)

        self.SupplierTable.heading("invoice", text="Invoice")
        self.SupplierTable.heading("name", text="Supplier Name")
        self.SupplierTable.heading("contact", text="Contact")
        self.SupplierTable.heading("desc", text="Description")
        self.SupplierTable["show"] = "headings"

        self.SupplierTable.column("invoice", width=90)
        self.SupplierTable.column("name", width=100)
        self.SupplierTable.column("contact", width=100)
        self.SupplierTable.column("desc", width=100)
        self.SupplierTable.pack(expand=1, fill=BOTH)
        self.SupplierTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()


##########################################################################################################################################
##########################################################################################################################################

    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error", "Invoice must be required", parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This Invoice no. already assigned, try different", parent=self.root)
                else:
                    cur.execute("Insert into supplier(invoice, name, contact, desc) values(?,?,?,?)", (
                                        self.var_sup_invoice.get(),
                                        self.var_name.get(),
                                        self.var_contact.get(),
                                        self.txt_desc.get('1.0', END)
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Supplier Added Successfully", parent=self.root)
                    self.show()
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("Select * from supplier")
            rows=cur.fetchall()
            self.SupplierTable.delete(*self.SupplierTable.get_children())
            for row in rows:
                self.SupplierTable.insert('',END,values=row)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def get_data(self, ev):
        f=self.SupplierTable.focus()
        content=(self.SupplierTable.item(f))
        row=content['values']
        self.var_sup_invoice.set(row[0])
        self.var_name.set(row[1])
        self.var_contact.set(row[2])

        self.txt_desc.delete('1.0', END)
        self.txt_desc.insert(END,row[3])

    def update(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error", "Invoice no. must be required", parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Invoice no.", parent=self.root)
                else:
                    cur.execute("Update supplier set name=?, contact=?, desc=? where  invoice=?", (
                                        self.var_name.get(),
                                        self.var_contact.get(),
                                        self.txt_desc.get('1.0', END),
                                        self.var_sup_invoice.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Supplier Updated Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error", "Invoice no. must be required", parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Invoice no.", parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?", parent=self.root)
                    if op==True:
                        cur.execute("delete from supplier where invoice=?",(self.var_sup_invoice.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Supplier Deleted Successfully", parent=self.root)
                        self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def clear(self):
        self.var_sup_invoice.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.txt_desc.delete('1.0', END)
        self.var_searchtxt.set("")
        self.show()

    def search(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_searchtxt.get()=="":   
                messagebox.showerror("Error", "Invoice no. should be required", parent=self.root)

            else:
                cur.execute("Select * from supplier where invoice=?",(self.var_searchtxt.get(),))
                row=cur.fetchone()
                if row!=None:
                    self.SupplierTable.delete(*self.SupplierTable.get_children())
                    self.SupplierTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error", "No record found.", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)



    def exit(self):
        self.root.destroy()

if __name__ =="__main__":
    root = Tk()
    obj = supplierClass(root)
    root.mainloop()