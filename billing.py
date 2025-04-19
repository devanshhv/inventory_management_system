from tkinter import*
from PIL import Image,ImageTk #pip install pillow
from tkinter import ttk,messagebox
import sqlite3
import time
import os
import tempfile
class BillClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1920x1080+0+0")
        self.root.title("Inventory Management System  | Developed by Devansh and Ishwari")
        self.root.config(bg="white")
        self.cart_list=[]
        self.chk_print=0

        #TITLE
        self.icon_title=PhotoImage(file="images/logo1.png")
        title=Label(self.root,text="Inventory Management System",image=self.icon_title,compound=LEFT,font=("times new roman",40,"bold"),bg="#010c48",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)

        #BUTTON LOGOUT dashboard
        btn_logout=Button(self.root,text="Logout",command=self.logout,font=("times new roman",15,"bold"),bg="yellow",cursor="hand2").place(x=1150,y=10,height=50,width=130)

        #clock
        self.lbl_clock=Label(self.root,text="Welcome to Inventory Management System\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",font=("times new roman",15),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

# PRODUCT FRAME
        
        ProductFrame1=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        ProductFrame1.place(x=6,y=110,width=410,height=550)

        pTitle=Label(ProductFrame1,text="All Products",font=("goudy old style",20,"bold"),bg="#262626",fg="white").pack(side=TOP,fill=X)
# product search frame
        self.var_search=StringVar()
        ProductFrame2=Frame(ProductFrame1,bd=2,relief=RIDGE,bg="white")
        ProductFrame2.place(x=2,y=42,width=398,height=90)

        lbl_search=Label(ProductFrame2,text="Search Product | By Name",font=("times new roman",15,"bold"),bg="white",fg="green").place(x=2,y=5)
        lbl_search=Label(ProductFrame2,text="Product Name",font=("times new roman",15,"bold"),bg="white").place(x=2,y=45)

        txt_search=Entry(ProductFrame2,textvariable=self.var_search,font=("times new roman",15),bg="light yellow").place(x=128,y=47,width=150,height=22)
        btn_search=Button(ProductFrame2,text="Search",command=self.search,font=("goudy old style",15),bg="#2196f3",cursor="hand2").place(x=285,y=45,width=100,height=25)
        btn_show_all=Button(ProductFrame2,text="Show All",command=self.show,font=("goudy old style",15),bg="#083531",fg="white",cursor="hand2").place(x=285,y=10,width=100,height=25)

# product detail frame
        ProductFrame3=Frame(ProductFrame1,bd=3,relief=RIDGE)
        ProductFrame3.place(x=2,y=140,width=398,height=375)

        scrolly=Scrollbar(ProductFrame3,orient=VERTICAL)
        scrollx=Scrollbar(ProductFrame3,orient=HORIZONTAL)

        self.ProductTable=ttk.Treeview(ProductFrame3,columns=("pid","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.ProductTable.xview)
        scrolly.config(command=self.ProductTable.yview)
        self.ProductTable.heading("pid",text="P ID")
        self.ProductTable.heading("name",text="Name")
        self.ProductTable.heading("price",text="Price")
        self.ProductTable.heading("qty",text="Quantity")
        self.ProductTable.heading("status",text="Status")
        self.ProductTable["show"]="headings"

        self.ProductTable.column("pid",width=40)
        self.ProductTable.column("name",width=100)
        self.ProductTable.column("price",width=90)
        self.ProductTable.column("qty",width=80)
        self.ProductTable.column("status",width=70)
        self.ProductTable.pack(fill=BOTH,expand=1)
        self.ProductTable.bind("<ButtonRelease-1>",self.get_data)

        lbl_note=Label(ProductFrame1,text="Note:'Enter 0 QTY to remove the product from cart'",font=("goudy old style",12),anchor='w',bg="white",fg="red").pack(side=BOTTOM,fill=X)

#====Customer Frame=======
        self.var_cname=StringVar()
        self.var_contact=StringVar()
        CustomerFrame=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        CustomerFrame.place(x=420,y=110,width=530,height=70)

        cTitle=Label(CustomerFrame,text="Customer Details",font=("goudy old style",15),bg="light grey").pack(side=TOP,fill=X)

        lbl_name=Label(CustomerFrame,text="Name",font=("times new roman",15),bg="white").place(x=5,y=35)
        txt_name=Entry(CustomerFrame,textvariable=self.var_cname,font=("times new roman",13),bg="light yellow").place(x=80,y=35,width=180)

        lbl_contact=Label(CustomerFrame,text="Contact No.",font=("times new roman",15),bg="white").place(x=270,y=35)
        txt_contact=Entry(CustomerFrame,textvariable=self.var_contact,font=("times new roman",13),bg="light yellow").place(x=370,y=35,width=140)
#cal cart frame
        Cal_Cart_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        Cal_Cart_Frame.place(x=420,y=190,width=530,height=360)

# cart frame
        cartFrame=Frame(Cal_Cart_Frame,bd=3,relief=RIDGE)
        cartFrame.place(x=5,y=8,width=520,height=342)

        self.cartTitle=Label(cartFrame,text="Cart \t Total Products: [0]",font=("goudy old style",15),bg="light grey")
        self.cartTitle.pack(side=TOP,fill=X)

        scrolly=Scrollbar(cartFrame,orient=VERTICAL)
        scrollx=Scrollbar(cartFrame,orient=HORIZONTAL)
        self.CartTable=ttk.Treeview(cartFrame,columns=("pid","name","price","qty"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)
        self.CartTable.heading("pid",text="P ID")
        self.CartTable.heading("name",text="Name")
        self.CartTable.heading("price",text="Price")
        self.CartTable.heading("qty",text="QTY")
        self.CartTable["show"]="headings"

        self.CartTable.column("pid",width=40)
        self.CartTable.column("name",width=90)
        self.CartTable.column("price",width=90)
        self.CartTable.column("qty",width=30)
        self.CartTable.pack(fill=BOTH,expand=1)
        self.CartTable.bind("<ButtonRelease-1>",self.get_data_cart)
#add cart widgets frame
        self.var_pid=StringVar()
        self.var_pname=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_stock=StringVar()

        Add_CartWidgets_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        Add_CartWidgets_Frame.place(x=420,y=550,width=530,height=110)

        lbl_p_name=Label(Add_CartWidgets_Frame,text="Product Name",font=("times new roman",15),bg="white").place(x=5,y=5)
        txt_p_name=Entry(Add_CartWidgets_Frame,textvariable=self.var_pname,font=("times new roman",15),bg="light yellow",state='readonly').place(x=5,y=35,width=190,height=22)

        lbl_p_price=Label(Add_CartWidgets_Frame,text="Price per Qty",font=("times new roman",15),bg="white").place(x=230,y=5)
        txt_p_price=Entry(Add_CartWidgets_Frame,textvariable=self.var_price,font=("times new roman",15),bg="light yellow",state='readonly').place(x=230,y=35,width=150,height=22)

        lbl_p_qty=Label(Add_CartWidgets_Frame,text="Quantity",font=("times new roman",15),bg="white").place(x=390,y=5)
        txt_p_qty=Entry(Add_CartWidgets_Frame,textvariable=self.var_qty,font=("times new roman",15),bg="light yellow").place(x=390,y=35,width=120,height=22)

        self.lbl_instock=Label(Add_CartWidgets_Frame,text="In Stock",font=("times new roman",15),bg="white")
        self.lbl_instock.place(x=5,y=70)

        btn_clear_cart=Button(Add_CartWidgets_Frame,text="Clear",command=self.clear_cart,font=("times new roman",15,"bold"),bg="red",cursor="hand2").place(x=180,y=70,width=150,height=30)
        btn_add_cart=Button(Add_CartWidgets_Frame,text="Add | Update Cart",command=self.add_update_cart,font=("times new roman",15,"bold"),bg="green",fg="white",cursor="hand2").place(x=340,y=70,width=180,height=30)

#biling area----

        bill_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        bill_Frame.place(x=953,y=110,width=410,height=410)

        bTitle=Label(bill_Frame,text="Customer Bills",font=("goudy old style",20,"bold"),bg="orange",fg="black").pack(side=TOP,fill=X)
        scrolly=Scrollbar(bill_Frame,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)

        self.txt_billarea=Text(bill_Frame,yscrollcommand=scrolly.set)
        self.txt_billarea.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.txt_billarea.yview)

        #billing buttons

        billMenuFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billMenuFrame.place(x=953,y=520,width=410,height=140)

        self.lbl_amount=Label(billMenuFrame,text="Bill Amount\n[0]",font=("goudy old style",15,"bold"),bg="#3f51b5",fg="white")
        self.lbl_amount.place(x=2,y=5,width=120,height=70)

        self.lbl_disc=Button(billMenuFrame,text="Discount\n[5%]",command=self.apply_discount,font=("goudy old style",15,"bold"),bg="#8bc34a",fg="white",cursor="hand2")
        self.lbl_disc.place(x=124,y=5,width=120,height=70)

        self.lbl_netpay=Label(billMenuFrame,text="Net Amount\n[0]",font=("goudy old style",15,"bold"),bg="#607d8b",fg="white")
        self.lbl_netpay.place(x=246,y=5,width=160,height=70)

        btn_print=Button(billMenuFrame,text="Print",command=self.print_bill,cursor="hand2",font=("goudy old style",15,"bold"),bg="light green",fg="white")
        btn_print.place(x=2,y=80,width=120,height=50)

        btn_clear_all=Button(billMenuFrame,text="Clear All",command=self.clear_all,cursor="hand2",font=("goudy old style",15,"bold"),bg="gray",fg="white")
        btn_clear_all.place(x=124,y=80,width=120,height=50)

        btn_generate=Button(billMenuFrame,text="Generate/Save Bill",command=self.generate_bill,cursor="hand2",font=("goudy old style",15,"bold"),bg="#009688",fg="white")
        btn_generate.place(x=246,y=80,width=160,height=50)

        #footer
        footer=Label(self.root,text="IMS Inventory Management System | Developed by Devansh and Ishu \n For any Technical issue contact:",font=("times new roman",11),bg="#4d636d",fg="white").pack(side=BOTTOM,fill=X)

        self.show()
        self.update_date_time()

#-----FUNCTIONS-------
    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select pid,name,price,qty,status from product where Status='Active'")
            rows=cur.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())
            for row in rows:
                self.ProductTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def search(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_search.get()=="":
                messagebox.showerror("Error","Seach input required",parent=self.root)
            else:
                cur.execute("select pid,name,price,qty,status from product where name LIKE '%"+self.var_search.get()+"%' and status='Active'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.ProductTable.delete(*self.ProductTable.get_children())
                    for row in rows:
                        self.ProductTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)
    
    def get_data(self,ev):
        f=self.ProductTable.focus()
        content=(self.ProductTable.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_instock.config(text=f"In Stock[{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set('1')

    def get_data_cart(self,ev):
        f=self.CartTable.focus()
        content=(self.CartTable.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])
        self.lbl_instock.config(text=f"In Stock[{str(row[4])}]")
        self.var_stock.set(row[4])
        
    def add_update_cart(self):
        if self.var_pid.get()=='':
            messagebox.showerror("Error","Please Select Product",parent=self.root)
        elif self.var_qty.get()=='':
            messagebox.showerror("Error","Please Add Quantity",parent=self.root)
        elif int(self.var_qty.get())>int(self.var_stock.get()):
            messagebox.showerror("Error","Invalid Quantity",parent=self.root)
        else:
            #price_cal=int(self.var_qty.get())*float(self.var_price.get())
            #price_cal=float(price_cal)

            price_cal=self.var_price.get()

            cart_data=[self.var_pid.get(),self.var_pname.get(),price_cal,self.var_qty.get(),self.var_stock.get()]
            #update cart
            present='no'
            index_=0
            for row in self.cart_list:
                if self.var_pid.get()==row[0]:
                    present='yes'
                    break
                index_+=1       
            if present=='yes':
                op=messagebox.askyesno("Confirm","Product already present \nDo you want to Update | Remove from the cart list",parent=self.root)
                if op==True:
                    if self.var_qty.get()=="0":
                        self.cart_list.pop(index_)
                    else:
                        #self.cart_list[index_][2]=price_cal
                        self.cart_list[index_][3]=self.var_qty.get()
            
            else:
                self.cart_list.append(cart_data)
            self.show_cart()
            self.bill_updates()
    
    def bill_updates(self):
        self.bill_amnt = 0
        self.discount = 0
        self.net_pay = 0

        for row in self.cart_list:
            self.bill_amnt += (float(row[2]) * int(row[3]))

    # Check if the discount is applied
        if self.discount > 0:
            self.net_pay = self.bill_amnt - self.discount
        else:
            self.net_pay = self.bill_amnt  # If no discount, net pay is the bill amount

        self.lbl_amount.config(text=f'Bill Amount\nRs{str(self.bill_amnt)}')
        self.lbl_netpay.config(text=f'Net Amount\nRs.{self.net_pay:.2f}')  # Ensure net pay is updated
        self.cartTitle.config(text=f'Cart \t Total Products:[{str(len(self.cart_list))}]')

    def apply_discount(self):
        if self.bill_amnt == 0:
            messagebox.showerror("Error", "No bill amount available to apply discount", parent=self.root)
        else:
            self.discount=(self.bill_amnt*5) / 100  # Calculate 5% discount
            self.net_pay = self.bill_amnt - self.discount  # Update net pay
            self.lbl_amount.config(text=f'Bill Amount\nRs{str(self.bill_amnt)}')  # Update bill amount label
            self.lbl_netpay.config(text=f'Net Amount\nRs.{self.net_pay:.2f}')  # Update net amount label
            self.btn_discount.config(state='disabled')  # Disable the button after applying discount

    def show_cart(self):
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def generate_bill(self):
        if self.var_cname.get()=='' or self.var_contact.get()=='':
            messagebox.showerror("Error","Customer Details are Required",parent=self.root)
        elif len(self.cart_list)==0:
            messagebox.showerror("Error","Please Add Products to the cart",parent=self.root)
        else:
            # bill top
            self.bill_top()
            #bill middle
            self.bill_middle()
            #bill bottom
            self.bill_bottom()

            fp=open(f'bill/{str(self.invoice)}.txt','w')
            fp.write(self.txt_billarea.get('1.0',END))
            fp.close()
            messagebox.showinfo('Saved','Bill has been Saved',parent=self.root)
            self.chk_print=1
            
    def bill_top(self):
        self.invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
        bill_top_temp=f'''
\t\tIMS-Inventory Manager
\t Phone No. 98765***** , Pune-411009
{str("="*47)}
 Customer Name: {self.var_cname.get()}
 Ph no. :{self.var_contact.get()}
 Bill No. {str(self.invoice)}\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("="*47)}
 Product Name\t\t\tQTY\tPrice
{str("="*47)}
        '''
        self.txt_billarea.delete('1.0',END)
        self.txt_billarea.insert('1.0',bill_top_temp)

    def bill_bottom(self):
        bill_bottom_temp=f'''
{str("="*47)}
 Bill Amount\t\t\t\tRs.{self.bill_amnt}
 Discount\t\t\t\tRs.{self.discount}
 Total Amount\t\t\t\tRs.{self.net_pay}
{str("="*47)}\n
        '''
        self.txt_billarea.insert(END,bill_bottom_temp)

    def bill_middle(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            
            for row in self.cart_list:
            #pid,name,price,qty,stock
                pid=row[0]
                name=row[1]
                qty=int(row[4])-int(row[3])
                if int(row[3])==int(row[4]):
                    status='Inactive'
                if int(row[3])!=int(row[4]):
                    status='Active'
                price=float(row[2])*int(row[3])
                price=str(price)
                self.txt_billarea.insert(END,"\n "+name+"\t\t\t"+row[3]+"\tRs."+price)
                #update qty in product table
                cur.execute('Update product set qty=?,Status=? where pid=?',(
                    qty,
                    status,
                    pid
                ))
                con.commit()
            con.close()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def clear_cart(self):
        self.var_pid.set('')
        self.var_pname.set('')
        self.var_price.set('')
        self.var_qty.set('')
        self.lbl_instock.config(text=f"In Stock")
        self.var_stock.set('')

    def clear_all(self):
        del self.cart_list[:]
        self.var_cname.set('')
        self.var_contact.set('')
        self.var_search.set('')
        self.txt_billarea.delete('1.0',END)
        self.cartTitle.config(text=f'Cart \t Total Products:[0]')
        self.clear_cart()
        self.show()
        self.show_cart()
        self.chk_print=0

    def update_date_time(self):
        time_=time.strftime("%I:%M:%S")
        date_=time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
        self.lbl_clock.after(200,self.update_date_time)

    def print_bill(self):
        if self.chk_print==1:
            messagebox.showinfo('Print','Printing in process',parent=self.root)
            new_file=tempfile.mktemp('.txt')
            open(new_file,'w').write(self.txt_billarea.get('1.0',END))
            os.startfile(new_file,'print')
        else:
            messagebox.showerror("Print","Generate bill to print",parent=self.root)
            
    def logout(self):
        self.root.destroy()
        os.system("python login.py")
        
if __name__=="__main__":
    root=Tk()
    obj=BillClass(root)
    root.mainloop()
