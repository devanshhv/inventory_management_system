from tkinter import*
from PIL import Image,ImageTk #pip install pillow
from tkinter import ttk,messagebox
import sqlite3
class productClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System  | Developed by Devansh and Ishwari")
        self.root.config(bg="#D2E0FB")  
        self.root.focus_force()

        #------------------------
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()
        self.var_pid=StringVar()
        self.var_cat=StringVar()
        self.var_sup=StringVar()
        self.cat_list=[]
        self.sup_list=[]
        self.fetch_cat_sup()
        self.var_name=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_status=StringVar()

        product_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="#DEE5D4")
        product_Frame.place(x=10,y=10,width=450,height=480)

        #title
        title=Label(product_Frame, text="Product Details", font=("goudy old style", 18), bg="#0f4d7d", fg="white").pack(side=TOP,fill=X)
        #column1
        lbl_category=Label(product_Frame, text="Category", font=("goudy old style", 18),bg="#DEE5D4").place(x=30,y=60)
        lbl_supplier=Label(product_Frame, text="Supplier", font=("goudy old style", 18),bg="#DEE5D4").place(x=30,y=110)
        lbl_product_name=Label(product_Frame, text="Name", font=("goudy old style", 18),bg="#DEE5D4").place(x=30,y=160)
        lbl_price=Label(product_Frame, text="Price", font=("goudy old style", 18),bg="#DEE5D4").place(x=30,y=210)
        lbl_qty=Label(product_Frame, text="Quantity", font=("goudy old style", 18),bg="#DEE5D4").place(x=30,y=260)
        lbl_status=Label(product_Frame, text="Status", font=("goudy old style", 18),bg="#DEE5D4").place(x=30,y=310)

        # column2
        cmb_cat=ttk.Combobox(product_Frame,textvariable=self.var_cat,values=self.cat_list,state='readonly',justify=CENTER,font=("goudy old style",11))
        cmb_cat.place(x=150,y=60,width=200)    
        cmb_cat.current(0)

        cmb_sup=ttk.Combobox(product_Frame,textvariable=self.var_sup,values=self.sup_list,state='readonly',justify=CENTER,font=("goudy old style",11))
        cmb_sup.place(x=150,y=110,width=200)    
        cmb_sup.current(0)

        txt_name=Entry(product_Frame,textvariable=self.var_name,font=("goudy old style",11),bg="light yellow").place(x=150,y=160,width=200)    
        txt_price=Entry(product_Frame,textvariable=self.var_price,font=("goudy old style",11),bg="light yellow").place(x=150,y=210,width=200)    
        txt_qty=Entry(product_Frame,textvariable=self.var_qty,font=("goudy old style",11),bg="light yellow").place(x=150,y=260,width=200)    

        cmb_status=ttk.Combobox(product_Frame,textvariable=self.var_status,values=("Active","Inactive"),state='readonly',justify=CENTER,font=("goudy old style",11))
        cmb_status.place(x=150,y=310,width=200)    
        cmb_status.current(0)

        #button
        btn_add=Button(product_Frame,text="Add",command=self.add,font=("goudy old style",11),bg="#2196f3",fg="white",cursor="hand2").place(x=10,y=400,width=100,height=40)
        btn_update=Button(product_Frame,command=self.update,text="Update",font=("goudy old style",11),bg="#4caf50",fg="white",cursor="hand2").place(x=120,y=400,width=100,height=40)
        btn_delete=Button(product_Frame,command=self.delete,text="Delete",font=("goudy old style",11),bg="#f44336",fg="white",cursor="hand2").place(x=230,y=400,width=100,height=40)
        btn_clear=Button(product_Frame,command=self.clear,text="Clear",font=("goudy old style",11),bg="#607d8b",fg="white",cursor="hand2").place(x=340,y=400,width=100,height=40)

        # search frame
        SearchFrame=LabelFrame(self.root,text="Search Product",bg="#DEE5D4",font=("goudy old style",20,"bold"),bd=2,relief=RIDGE)
        SearchFrame.place(x=480,y=10,width=600,height=80)

        # options
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("Select","Supplier","Category","Name"),state='readonly',justify=CENTER,font=("goudy old style",11))
        cmb_search.place(x=10,y=10,width=180)    
        cmb_search.current(0)

        txt_search=Entry(SearchFrame,textvariable=self.var_searchtxt,font=("goudy old style",11),bg="light yellow").place(x=200,y=10)
        btn_search=Button(SearchFrame,text="Search",command=self.search,font=("goudy old style",11),bg="#4caf50",fg="white",cursor="hand2").place(x=410,y=8,width=150,height=30)

        #product details
        p_frame=Frame(self.root,bd=3,relief=RIDGE)
        p_frame.place(x=480,y=100,width=600,height=390)
        scrolly=Scrollbar(p_frame,orient=VERTICAL)
        scrollx=Scrollbar(p_frame,orient=HORIZONTAL)
        self.product_Table=ttk.Treeview(p_frame,columns=("pid","Category","Supplier","Name","Price","qty","Status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.product_Table.xview)
        scrolly.config(command=self.product_Table.yview)
        self.product_Table.heading("pid",text="P ID")
        self.product_Table.heading("Category",text="Category")
        self.product_Table.heading("Supplier",text="Supplier")
        self.product_Table.heading("Name",text="Name")
        self.product_Table.heading("Price",text="Price")
        self.product_Table.heading("qty",text="Quantity")
        self.product_Table.heading("Status",text="Status")
        self.product_Table["show"]="headings"

        self.product_Table.column("pid",width=90)
        self.product_Table.column("Category",width=100)
        self.product_Table.column("Supplier",width=100)
        self.product_Table.column("Name",width=100)
        self.product_Table.column("Price",width=100)
        self.product_Table.column("qty",width=100)
        self.product_Table.column("Status",width=100)
        self.product_Table.pack(fill=BOTH,expand=1)
        self.product_Table.bind("<ButtonRelease-1>",self.get_data)
        self.show()

    #functions
    def fetch_cat_sup(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("Select name from category")
            cat=cur.fetchall()
            self.cat_list.append("Empty")
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
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_cat.get()=="Select" or self.var_sup.get()=="Select" or self.var_name.get()=="":
                messagebox.showerror("Error","All fields are required",parent=self.root)
            else:
                cur.execute("Select * from product where name=?",(self.var_name.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Product already available, try another",parent=self.root)
                else:
                    cur.execute("Insert into product (Category,Supplier,Name,Price,qty,Status) values(?,?,?,?,?,?)",(            
                                                self.var_cat.get(),
                                                self.var_sup.get(),
                                                self.var_name.get(),
                                                self.var_price.get(),
                                                self.var_qty.get(),
                                                self.var_status.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Product added successfully",parent=self.root)
                    self.show()
                    
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)
    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from product")
            rows=cur.fetchall()
            self.product_Table.delete(*self.product_Table.get_children())
            for row in rows:
                self.product_Table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)
    
    def get_data(self,ev):
        f=self.product_Table.focus()
        content=(self.product_Table.item(f))
        row=content['values']
        self.var_pid.set(row[0]),
        self.var_cat.set(row[1]),
        self.var_sup.set(row[2]),
        self.var_name.set(row[3]),
        self.var_price.set(row[4]),
        self.var_qty.set(row[5]),
        self.var_status.set(row[6]),

    def update(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error","Please select product from list",parent=self.root)
            else:
                cur.execute("Select * from product where pid=?",(self.var_pid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Product",parent=self.root)
                else:
                    cur.execute("Update product set Category=?,Supplier=?,Name=?,Price=?,qty=?,Status=? where pid=?",(            
                                                self.var_cat.get(),
                                                self.var_sup.get(),
                                                self.var_name.get(),
                                                self.var_price.get(),
                                                self.var_qty.get(),
                                                self.var_status.get(),
                                                self.var_pid.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Product Updated successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error","Select Product from the list",parent=self.root)
            else:
                cur.execute("Select * from product where pid=?",(self.var_pid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Product",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Are you sure you want to delete",parent=self.root)
                    if op==True:
                        cur.execute("delete from product where pid=?",(self.var_pid.get(),))
                        con.commit()
                        messagebox.showinfo("Deleted","Product deleted successfully",parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def clear(self):
               
        self.var_cat.set("Select")
        self.var_sup.set("Select")
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_status.set("Active")
        self.var_pid.set("")
        self.var_searchby.set("")
        self.var_searchtxt.set("Select")
        self.show()

    def search(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_searchby.get()=="Select":
                messagebox.showerror("Error","Select Search Option",parent=self.root)
            elif self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Seach input required",parent=self.root)
            else:
                cur.execute("select * from product where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.product_Table.delete(*self.product_Table.get_children())
                    for row in rows:
                        self.product_Table.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

if __name__=="__main__":
    root=Tk()
    obj=productClass(root)
    root.mainloop()