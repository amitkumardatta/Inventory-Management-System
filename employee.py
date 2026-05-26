from sqlite3.dbapi2 import Cursor, connect
from tkinter import *
from PIL import ImageTk
import PIL.Image
from tkinter import ttk, messagebox
import sqlite3
import os

from ui_theme import apply_theme, colors


class employeeClass:
    def __init__(self, root, show_menu=None):
        self.root = root
        self.show_menu = show_menu
        self.palette = colors()

        if isinstance(self.root, (Tk, Toplevel)):
            apply_theme(self.root)
            self.root.geometry("1150x560+140+90")
            self.root.minsize(1000, 520)
            self.root.title("Employee | IMS | Developed by Amit")
            self.root.config(bg=self.palette["bg"])
            photo = PhotoImage(file=os.path.join("images", "i1.png"))
            self.root.iconphoto(False, photo)
            self.root.focus_force()
        #root.overrideredirect(1)

        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        #All variables

        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_emp_id = StringVar()
        self.var_name = StringVar()
        self.var_email = StringVar()
        self.var_gender = StringVar()
        self.var_contact = StringVar()
        self.var_dob = StringVar()
        self.var_doj = StringVar()
        self.var_pass = StringVar()
        self.var_utype = StringVar()
        self.var_salary = StringVar()



        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(4, weight=1)

        header_frame = Frame(self.root, bg=self.palette["bg"])
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(15, 5))
        header_frame.columnconfigure(1, weight=1)

        if self.show_menu:
            btn_menu = ttk.Button(
                header_frame,
                text="Menu",
                command=self.show_menu,
                style="Sidebar.TButton",
            )
            btn_menu.grid(row=0, column=0, sticky="w", padx=0, pady=0)

        SearchFrame = LabelFrame(self.root, text="Search Employee", bg="white", fg="black", font=("goudy old style",12,"bold"))
        SearchFrame.grid(row=0, column=0, sticky="ew", padx=(160 if self.show_menu else 0, 20), pady=(15, 5))
        SearchFrame.columnconfigure(1, weight=1)

        cms_search = ttk.Combobox(SearchFrame, textvariable=self.var_searchby, values=("Select", "Email", "Name", "Contact"), state='readonly', justify=CENTER, font=("times new roman", 15))
        cms_search.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        cms_search.current(0)

        txt_search = Entry(SearchFrame, textvariable=self.var_searchtxt, font=("times new roman", 15), bg="azure2", fg="black")
        txt_search.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        btn_search = ttk.Button(SearchFrame, command=self.search, text="Search", style="Accent.TButton")
        btn_search.grid(row=0, column=2, padx=10, pady=10, sticky="e")

        title = Label(self.root, text="Employee Details", font=("times new roman", 15), bg="#0f4d7d", fg="white")
        title.grid(row=1, column=0, sticky="ew", padx=20, pady=(5, 10))

        form_frame = Frame(self.root, bg=self.palette["bg"])
        form_frame.grid(row=2, column=0, sticky="ew", padx=20)
        form_frame.columnconfigure(0, weight=0)
        form_frame.columnconfigure(1, weight=1)

        lbl_empid = Label(form_frame, text="Employee ID", font=("times new roman", 15), bg="white", fg="black")
        lbl_empid.grid(row=0, column=0, sticky="w", padx=5, pady=4)
        txt_empid = Entry(form_frame, textvariable=self.var_emp_id, font=("times new roman", 15), bg ="azure2", fg="black")
        txt_empid.grid(row=0, column=1, sticky="ew", padx=5, pady=4)

        lbl_gender = Label(form_frame, text="Gender", font=("times new roman", 15), bg="white", fg="black")
        lbl_gender.grid(row=0, column=2, sticky="w", padx=5, pady=4)
        txt_gender = ttk.Combobox(form_frame, textvariable=self.var_gender, font=("times new roman", 15), values=("Select", "Male", "Female", "Other"), state="readonly", justify=CENTER)
        txt_gender.grid(row=0, column=3, sticky="ew", padx=5, pady=4)
        txt_gender.current(0)

        lbl_contact = Label(form_frame, text="Contact", font=("times new roman", 15), bg="white", fg="black")
        lbl_contact.grid(row=0, column=4, sticky="w", padx=5, pady=4)
        txt_contact = Entry(form_frame, textvariable=self.var_contact, font=("times new roman", 15), bg="azure2", fg="black")
        txt_contact.grid(row=0, column=5, sticky="ew", padx=5, pady=4)

        lbl_name = Label(form_frame, text="Name", font=("times new roman", 15), bg="white", fg="black")
        lbl_name.grid(row=1, column=0, sticky="w", padx=5, pady=4)
        txt_name = Entry(form_frame, textvariable=self.var_name, font=("times new roman", 15), bg ="azure2", fg="black")
        txt_name.grid(row=1, column=1, sticky="ew", padx=5, pady=4)

        lbl_dob = Label(form_frame, text="Date of birth", font=("times new roman", 15), bg="white", fg="black")
        lbl_dob.grid(row=1, column=2, sticky="w", padx=5, pady=4)
        txt_dob = Entry(form_frame, textvariable=self.var_dob, font=("times new roman", 15), bg ="azure2", fg="black")
        txt_dob.grid(row=1, column=3, sticky="ew", padx=5, pady=4)

        lbl_doj = Label(form_frame, text="Date of joining", font=("times new roman", 15), bg="white", fg="black")
        lbl_doj.grid(row=1, column=4, sticky="w", padx=5, pady=4)
        txt_doj = Entry(form_frame, textvariable=self.var_doj, font=("times new roman", 15), bg="azure2", fg="black")
        txt_doj.grid(row=1, column=5, sticky="ew", padx=5, pady=4)

        lbl_email = Label(form_frame, text="E-mail", font=("times new roman", 15), bg="white", fg="black")
        lbl_email.grid(row=2, column=0, sticky="w", padx=5, pady=4)
        txt_email = Entry(form_frame, textvariable=self.var_email, font=("times new roman", 15), bg ="azure2", fg="black")
        txt_email.grid(row=2, column=1, sticky="ew", padx=5, pady=4)

        lbl_pass = Label(form_frame, text="Password", font=("times new roman", 15), bg="white", fg="black")
        lbl_pass.grid(row=2, column=2, sticky="w", padx=5, pady=4)
        txt_pass = Entry(form_frame, textvariable=self.var_pass, font=("times new roman", 15), bg ="azure2", fg="black")
        txt_pass.grid(row=2, column=3, sticky="ew", padx=5, pady=4)

        lbl_utype = Label(form_frame, text="User type", font=("times new roman", 15), bg="white", fg="black")
        lbl_utype.grid(row=2, column=4, sticky="w", padx=5, pady=4)
        txt_utype = ttk.Combobox(form_frame, textvariable=self.var_utype, state="readonly", font=("times new roman", 15), values=("Select", "Admin", "Employee"))
        txt_utype.grid(row=2, column=5, sticky="ew", padx=5, pady=4)
        txt_utype.current(0)

        lbl_address = Label(form_frame, text="Address", font=("times new roman", 15), bg="white", fg="black")
        lbl_address.grid(row=3, column=0, sticky="nw", padx=5, pady=4)
        self.txt_address = Text(form_frame, font=("times new roman", 15), bg ="azure2", fg="black", height=3)
        self.txt_address.grid(row=3, column=1, columnspan=2, sticky="ew", padx=5, pady=4)

        lbl_salary = Label(form_frame, text="Salary", font=("times new roman", 15), bg="white", fg="black")
        lbl_salary.grid(row=3, column=3, sticky="w", padx=5, pady=4)
        txt_salary = Entry(form_frame, textvariable=self.var_salary, font=("times new roman", 15), bg ="azure2", fg="black")
        txt_salary.grid(row=3, column=4, sticky="ew", padx=5, pady=4)

        btn_frame = Frame(self.root, bg=self.palette["bg"])
        btn_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=(6, 8))
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



        self.EmployeeTable = ttk.Treeview(emp_frame, columns=("eid", "name", "email", "gender", "contact", "dob", "doj", "pass", "utype", "address", "salary"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.pack(side=BOTTOM, fill=X)
        scrollx.config(command=self.EmployeeTable.xview)
        scrolly.config(command=self.EmployeeTable.yview)

        self.EmployeeTable.heading("eid", text="Employee ID")
        self.EmployeeTable.heading("name", text="Name")
        self.EmployeeTable.heading("email", text="Email")
        self.EmployeeTable.heading("gender", text="Gender")
        self.EmployeeTable.heading("contact", text="Contact")
        self.EmployeeTable.heading("dob", text="Date of birth")
        self.EmployeeTable.heading("doj", text="Date of joining")
        self.EmployeeTable.heading("pass", text="Password")
        self.EmployeeTable.heading("utype", text="User type")
        self.EmployeeTable.heading("address", text="Address")
        self.EmployeeTable.heading("salary", text="Salary")

        self.EmployeeTable["show"] = "headings"

        self.EmployeeTable.column("eid", width=90)
        self.EmployeeTable.column("name", width=100)
        self.EmployeeTable.column("email", width=100)
        self.EmployeeTable.column("gender", width=100)
        self.EmployeeTable.column("contact", width=100)
        self.EmployeeTable.column("dob", width=100)
        self.EmployeeTable.column("doj", width=100)
        self.EmployeeTable.column("pass", width=100)
        self.EmployeeTable.column("utype", width=100)
        self.EmployeeTable.column("address", width=100)
        self.EmployeeTable.column("salary", width=100)
        self.EmployeeTable.pack(expand=1, fill=BOTH)
        self.EmployeeTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()


##########################################################################################################################################
##########################################################################################################################################

    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error", "Employee ID must be required", parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This Employee ID already assigned, try different", parent=self.root)
                else:
                    cur.execute("Insert into employee(eid, name, email, gender, contact, dob, doj, pass, utype, address, salary) values(?,?,?,?,?,?,?,?,?,?,?)", (
                                        self.var_emp_id.get(),
                                        self.var_name.get(),
                                        self.var_email.get(),
                                        self.var_gender.get(),
                                        self.var_contact.get(),

                                        self.var_dob.get(),
                                        self.var_doj.get(),

                                        self.var_pass.get(),
                                        self.var_utype.get(),
                                        self.txt_address.get('1.0', END),
                                        self.var_salary.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Employee Added Successfully", parent=self.root)
                    self.show()
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("Select * from employee")
            rows=cur.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                self.EmployeeTable.insert('',END,values=row)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def get_data(self, ev):
        f=self.EmployeeTable.focus()
        content=(self.EmployeeTable.item(f))
        row=content['values']
        self.var_emp_id.set(row[0])
        self.var_name.set(row[1])
        self.var_email.set(row[2])
        self.var_gender.set(row[3])
        self.var_contact.set(row[4])

        self.var_dob.set(row[5])
        self.var_doj.set(row[6])

        self.var_pass.set(row[7])
        self.var_utype.set(row[8])
        self.txt_address.delete('1.0', END)
        self.txt_address.insert(END,row[9])
        self.var_salary.set(row[10])

    def update(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error", "Employee ID must be required", parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Employee ID", parent=self.root)
                else:
                    cur.execute("Update employee set name=?, email=?, gender=?, contact=?, dob=?, doj=?, pass=?, utype=?, address=?, salary=? where  eid=?", (
                                        self.var_name.get(),
                                        self.var_email.get(),
                                        self.var_gender.get(),
                                        self.var_contact.get(),

                                        self.var_dob.get(),
                                        self.var_doj.get(),

                                        self.var_pass.get(),
                                        self.var_utype.get(),
                                        self.txt_address.get('1.0', END),
                                        self.var_salary.get(),
                                        self.var_emp_id.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Employee Updated Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error", "Employee ID must be required", parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Employee ID", parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?", parent=self.root)
                    if op==True:
                        cur.execute("delete from employee where eid=?",(self.var_emp_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Employee Deleted Successfully", parent=self.root)
                        self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def clear(self):
        self.var_emp_id.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_contact.set("")

        self.var_dob.set("")
        self.var_doj.set("")

        self.var_pass.set("")
        self.var_utype.set("Select")
        self.txt_address.delete('1.0', END)
        self.var_salary.set("")
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
                cur.execute("Select * from employee where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                    for row in rows:
                        self.EmployeeTable.insert('',END,values=row)

                else:
                    messagebox.showerror("Error", "No record found.", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)



    def exit(self):
        self.root.destroy()

if __name__ =="__main__":
    root = Tk()
    apply_theme(root)
    obj = employeeClass(root)
    root.mainloop()