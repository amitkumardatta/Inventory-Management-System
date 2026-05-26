from sqlite3.dbapi2 import Cursor, connect
from tkinter import *
from tkinter.font import BOLD
from PIL import ImageTk
import PIL.Image
from tkinter import ttk, messagebox
import sqlite3
import os

from ui_theme import apply_theme, colors


class productClass:
    def __init__(self, root, show_menu=None):
        self.root = root
        self.show_menu = show_menu
        self.palette = colors()

        if isinstance(self.root, (Tk, Toplevel)):
            apply_theme(self.root)
            self.root.geometry("1150x560+140+90")
            self.root.minsize(1000, 520)
            self.root.title("Product | IMS | Developed by Amit")
            self.root.config(bg=self.palette["bg"])
            photo = PhotoImage(file=os.path.join("images", "i1.png"))
            self.root.iconphoto(False, photo)
            self.root.focus_force()
        #root.overrideredirect(1)

        #########################################

        self.var_pid =StringVar()
        self.var_cat =StringVar()
        self.var_sup =StringVar()
        self.cat_list=[]
        self.sup_list=[]
        self.fetch_cat_sup()

        self.var_name =StringVar()
        self.var_price =StringVar()
        self.var_qty =StringVar()
        self.var_status =StringVar()

        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()


        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

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

        main_frame = Frame(self.root, bg=self.palette["bg"])
        main_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 15))
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        #---Frame---
        product_Frame=Frame(main_frame, bd=2, relief=RIDGE, bg="white")
        product_Frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 10))
        product_Frame.columnconfigure(0, weight=0) 
        product_Frame.columnconfigure(1, weight=1)
        
        #---Title--
        title = Label(product_Frame, text="Manage Product Details", font=("goudy old style", 15, "bold"), bg="IndianRed4", fg="white")
        title.grid(row=0, column=0, columnspan=2, sticky="ew")

        #---colum1---
        lbl_category = Label(product_Frame, text="Category", font=("times new roman", 15), bg="white", fg="black")
        lbl_category.grid(row=1, column=0, sticky="w", padx=20, pady=6)
        lbl_supplier = Label(product_Frame, text="Supplier", font=("times new roman", 15), bg="white", fg="black")
        lbl_supplier.grid(row=2, column=0, sticky="w", padx=20, pady=6)
        lbl_product = Label(product_Frame, text="Name", font=("times new roman", 15), bg="white", fg="black")
        lbl_product.grid(row=3, column=0, sticky="w", padx=20, pady=6)
        lbl_price = Label(product_Frame, text="Price", font=("times new roman", 15), bg="white", fg="black")
        lbl_price.grid(row=4, column=0, sticky="w", padx=20, pady=6)
        lbl_qty = Label(product_Frame, text="Quantity", font=("times new roman", 15), bg="white", fg="black")
        lbl_qty.grid(row=5, column=0, sticky="w", padx=20, pady=6)
        lbl_status = Label(product_Frame, text="Status", font=("times new roman", 15), bg="white", fg="black")
        lbl_status.grid(row=6, column=0, sticky="w", padx=20, pady=6)

        #---colum2---

        self.cmb_cat = ttk.Combobox(
            product_Frame,
            textvariable=self.var_cat,
            values=self.cat_list,
            state='readonly',
            justify=CENTER,
            font=("goudy old style", 15),
            postcommand=self.refresh_cat_sup,
        )
        self.cmb_cat.grid(row=1, column=1, sticky="ew", padx=20, pady=6)
        self.cmb_cat.current(0)

        self.cmb_sup = ttk.Combobox(
            product_Frame,
            textvariable=self.var_sup,
            values=self.sup_list,
            state='readonly',
            justify=CENTER,
            font=("goudy old style", 15),
            postcommand=self.refresh_cat_sup,
        )
        self.cmb_sup.grid(row=2, column=1, sticky="ew", padx=20, pady=6)
        self.cmb_sup.current(0)

        #--------

        txt_name = Entry(product_Frame, textvariable=self.var_name, font=("times new roman", 15), bg="azure2", fg="black")
        txt_name.grid(row=3, column=1, sticky="ew", padx=20, pady=6)

        txt_price = Entry(product_Frame, textvariable=self.var_price, font=("times new roman", 15), bg="azure2", fg="black")
        txt_price.grid(row=4, column=1, sticky="ew", padx=20, pady=6)

        txt_qty = Entry(product_Frame, textvariable=self.var_qty, font=("times new roman", 15), bg="azure2", fg="black")
        txt_qty.grid(row=5, column=1, sticky="ew", padx=20, pady=6) 

        #-----
        cmb_status = ttk.Combobox(product_Frame, textvariable=self.var_status, values=("Active", "Inactive"), state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_status.grid(row=6, column=1, sticky="ew", padx=20, pady=6)
        cmb_status.current(0)   

        #---Button--
        btn_add = ttk.Button(product_Frame, command=self.add, text="Save", style="Accent.TButton")
        btn_add.grid(row=7, column=0, padx=10, pady=10, sticky="ew")

        btn_update = ttk.Button(product_Frame, command=self.update, text="Update", style="AccentAlt.TButton")
        btn_update.grid(row=7, column=1, padx=10, pady=10, sticky="ew")

        btn_delete = ttk.Button(product_Frame, command=self.delete, text="Delete", style="Danger.TButton")
        btn_delete.grid(row=8, column=0, padx=10, pady=5, sticky="ew")

        btn_clear = ttk.Button(product_Frame, command=self.clear, text="Clear", style="Warning.TButton")
        btn_clear.grid(row=8, column=1, padx=10, pady=5, sticky="ew")


        #---Search---
        SearchFrame=LabelFrame(main_frame, text="Search Product", bg="white", font=("times new roman",12,"bold"), fg="red")
        SearchFrame.grid(row=0, column=1, sticky="ew", pady=(0, 10))
        SearchFrame.columnconfigure(1, weight=1)

        #====Options====
        cms_search = ttk.Combobox(SearchFrame, textvariable=self.var_searchby, values=("Select", "Category", "Supplier", "Name"), state='readonly', justify=CENTER, font=("times new roman", 15))
        cms_search.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        cms_search.current(0)

        txt_search = Entry(SearchFrame, textvariable=self.var_searchtxt, font=("times new roman", 15), bg="azure2")
        txt_search.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        btn_search = ttk.Button(SearchFrame, command=self.search, text="Search", style="Accent.TButton")
        btn_search.grid(row=0, column=2, padx=10, pady=10)

        #===Product details===

        p_frame = Frame(main_frame, bd=3, relief=RIDGE)
        p_frame.grid(row=1, column=1, sticky="nsew")

        scrolly = Scrollbar(p_frame, orient= VERTICAL)
        scrollx = Scrollbar(p_frame, orient= HORIZONTAL)



        self.product_table = ttk.Treeview(p_frame, columns=("pid", "Category", "Supplier", "name", "price", "qty", "status"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.pack(side=BOTTOM, fill=X)
        scrollx.config(command=self.product_table.xview)
        scrolly.config(command=self.product_table.yview)

        self.product_table.heading("pid", text="Product ID")    
        self.product_table.heading("Category", text="Category") 
        self.product_table.heading("Supplier", text="Supplier")  
        self.product_table.heading("name", text="Name")
        self.product_table.heading("price", text="Price")
        self.product_table.heading("qty", text="Quantity")
        self.product_table.heading("status", text="Status")
        self.product_table["show"] = "headings"

        self.product_table.column("pid", width=90)
        self.product_table.column("Category", width=100)
        self.product_table.column("Supplier", width=100)        
        self.product_table.column("name", width=100)
        self.product_table.column("price", width=100)
        self.product_table.column("qty", width=100)
        self.product_table.column("status", width=100)
        self.product_table.pack(expand=1, fill=BOTH)
        self.product_table.bind("<ButtonRelease-1>", self.get_data)

        self.show()



##########################################################################################################################################
##########################################################################################################################################

    def fetch_cat_sup(self):
        self.cat_list.clear()
        self.sup_list.clear()
        self.cat_list.append("Empty")
        self.sup_list.append("Empty")        
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("Select name from category")
            cat=cur.fetchall()

            if len(cat)>0:
                del self.cat_list[:]
                self.cat_list.append("Select")
                for i in cat:
                    self.cat_list.append(i[0])

            cur.execute("Select name from supplier")
            sup=cur.fetchall()

            if len(sup)>0:
                del self.sup_list[:]
                self.sup_list.append("Select")
                for i in sup:
                    self.sup_list.append(i[0])

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def refresh_cat_sup(self):
        self.fetch_cat_sup()
        self.cmb_cat.configure(values=self.cat_list)
        self.cmb_sup.configure(values=self.sup_list)

        if self.var_cat.get() not in self.cat_list:
            self.var_cat.set(self.cat_list[0])
        if self.var_sup.get() not in self.sup_list:
            self.var_sup.set(self.sup_list[0])


    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_cat.get()=="Select" or self.var_cat.get()=="Empty" or self.var_sup.get() =="Select" or self.var_sup.get()=="Empty" or self.var_name.get() == "":
                messagebox.showerror("Error", "All fields are required", parent=self.root)
            else:
                cur.execute("Select * from product where name=?",(self.var_name.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Product already present, try different", parent=self.root)
                else:
                    cur.execute("Insert into product(Category, Supplier, name, price, qty, status) values(?,?,?,?,?,?)", (
                                        self.var_cat.get(),
                                        self.var_sup.get(),                                        
                                        self.var_name.get(),
                                        self.var_price.get(),
                                        self.var_qty.get(),

                                        self.var_status.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Product Added Successfully", parent=self.root)
                    self.show()
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("Select * from product")
            rows=cur.fetchall()
            self.product_table.delete(*self.product_table.get_children())
            for row in rows:
                self.product_table.insert('',END,values=row)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def get_data(self, ev):
        f=self.product_table.focus()
        content=(self.product_table.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_cat.set(row[1])        
        self.var_sup.set(row[2])
        self.var_name.set(row[3])
        self.var_price.set(row[4])
        self.var_qty.set(row[5])
        self.var_status.set(row[6])
 

    def update(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error", "Please select product from list", parent=self.root)
            else:
                cur.execute("Select * from product where pid=?",(self.var_pid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Product", parent=self.root)
                else:
                    cur.execute("Update product set Category=?, Supplier=?, name=?, price=?, qty=?, status=? where  pid=?", (
                                        self.var_cat.get(),
                                        self.var_sup.get(),
                                        self.var_name.get(),
                                        self.var_price.get(),
                                        self.var_qty.get(),
                                        self.var_status.get(),
                                        self.var_pid.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Product Updated Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error", "Select product from the list", parent=self.root)
            else:
                cur.execute("Select * from product where pid=?",(self.var_pid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Product", parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?", parent=self.root)
                    if op==True:
                        cur.execute("delete from product where pid=?",(self.var_pid.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Product Deleted Successfully", parent=self.root)
                        self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def clear(self):
        self.var_sup.set("Select"),
        self.var_cat.set("Select"),
        self.var_name.set(""),
        self.var_price.set(""),
        self.var_qty.set(""),
        self.var_status.set("Active"),
        self.var_pid.set("")

        self.var_searchtxt.set("")
        self.var_searchby.set("Select")
        self.show()

    def search(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_searchby.get()=="Select":
                messagebox.showerror("Error", "Select search by option", parent=self.root)

            elif self.var_searchtxt.get()=="":   
                messagebox.showerror("Error", "Select input should be required", parent=self.root)

            else:
                cur.execute("Select * from product where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.product_table.delete(*self.product_table.get_children())
                    for row in rows:
                        self.product_table.insert('',END,values=row)

                else:
                    messagebox.showerror("Error", "No record found.", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)




if __name__ =="__main__":
    root = Tk()
    obj = productClass(root)
    root.mainloop()