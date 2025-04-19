from tkinter import*
from PIL import ImageTk
from tkinter import messagebox
import sqlite3
import os
import email_pass
import smtplib
import time


class Login_System:
    def __init__(self,root):
        self.root=root
        self.root.title("Login System | Devloped by Devansh and Ishwari")
        self.root.geometry("1920x1080+0+0")
        self.root.config(bg="#aec6cf")
        self.otp=''

        self.con, self.cur = self.connect_to_database()
        

        #title
        main_title=Label(self.root,text="Welcome to Inventory Management System",font=("times new roman",35,"bold"),bg="#89CFF0").pack(side=TOP,fill=X)
        sub_title=Label(self.root,text="Please Login to Continue",font=("times new roman",25,"bold"),justify=CENTER,bg="#aec6cf").place(x=600,y=100)

        #login frame
        self.var_employee_id=StringVar()
        self.var_password=StringVar()

        login_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        login_frame.place(x=600,y=200,width=350,height=460)

        title=Label(login_frame,text="LOGIN",font=("Elephant",30,"bold")).place(x=0,y=30,relwidth=1)

        lbl_user=Label(login_frame,text="Employee ID",font=("Andalus",15),bg="white",fg="#767171").place(x=50,y=100)
        
        txt_employee_id=Entry(login_frame,textvariable=self.var_employee_id,font=("times new roman",15),bg="#ECECEC").place(x=50,y=140,width=250)

        lbl_password=Label(login_frame,text="Password",font=("Andalus",15),bg="white",fg="#767171").place(x=50,y=200)
        txt_password=Entry(login_frame,textvariable=self.var_password,show="*",font=("times new roman",15),bg="#ECECEC").place(x=50,y=240,width=250)

        btn_login=Button(login_frame,command=self.login,text="Login",font=("Arial Rounded MT Bold",15),bg="#00B0F0",cursor="hand2",fg="white").place(x=50,y=300,width=250,height=35)

        hr=Label(login_frame,bg="light grey").place(x=50,y=370,width=250,height=2)
        or_=Label(login_frame,text="OR",font=("times new roman",15,"bold"),bg="white",fg="light grey").place(x=150,y=355)

        btn_forget=Button(login_frame,text="Forget Password?",command=self.forget_window,font=("times new roman",13),bg="white",fg="#00759E",bd=0,activebackground="white",cursor="hand2").place(x=100,y=390)

        # Footer
        lbl_footer=Label(self.root,text="IMS-Inventory Management System | Devloped by Devansh and Ishwari\n For any technical issues Contact-",font=("times new roman",12),bg="#4d636d",fg="white").pack(side=BOTTOM,fill=X)

    def login(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_employee_id.get()=="" or self.var_password.get()=="":
                messagebox.showerror('Error','All fields are required',parent=self.root)
            else:
                cur.execute('select utype from employee where eid=? AND pass=?',(self.var_employee_id.get(),self.var_password.get()))
                user=cur.fetchone()
                if user==None:
                     messagebox.showerror('Error','Invalid USERNAME/PASSWORD',parent=self.root)
                else:
                    if user[0]=="Admin":
                        self.root.destroy()
                        os.system("python dashboard.py")
                    else:
                        self.root.destroy()
                        os.system("python billing.py")

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def forget_window(self):
            con=sqlite3.connect(database=r'ims.db')
            cur=con.cursor()
            try:
                if self.var_employee_id.get()=="":
                    messagebox.showerror("Error","Employee ID is required",parent=self.root)
                else:
                    cur.execute('select email from employee where eid=?',(self.var_employee_id.get(),))
                    email=cur.fetchone()
                    if email==None:
                        messagebox.showerror('Error','Invalid UEmployee Id,try again',parent=self.root)
                    else:
                        #forget window
                        self.var_otp=StringVar()
                        self.var_newpass=StringVar()
                        self.var_confpass=StringVar()

                        #call send_email_function()
                        chk=self.send_email(email[0])
                        if chk=='f':
                            messagebox.showerror("Error","Connection Error,try again",parent=self.root)
                        else:
                            self.forget_win=Toplevel(self.root)
                            self.forget_win.title('RESET PASSWORD')
                            self.forget_win.geometry('400x350+500+100')
                            self.forget_win.focus_force()

                            title=Label(self.forget_win,text="Reset Password",font=("goudy old style",15,"bold"),bg="#3f51b5",fg="white").pack(side=TOP,fill=X)
                            lbl_reset=Label(self.forget_win,text="Enter OTP sent on register Email",font=("times new roman",15)).place(x=20,y=60)
                            txt_reset=Entry(self.forget_win,textvariable=self.var_otp,font=("times new roman",15),bg="light yellow").place(x=20,y=100,width=250,height=30)
                            
                            self.btn_reset=Button(self.forget_win,text="SUBMIT",command=self.validate_otp,font=("times new roman",15),bg="light blue")
                            self.btn_reset.place(x=280,y=100,width=100,height=30)

                            lbl_new_pass=Label(self.forget_win,text="New Password",font=("times new roman",15)).place(x=20,y=160)
                            txt_new_pass=Entry(self.forget_win,textvariable=self.var_newpass,font=("times new roman",15),bg="light yellow").place(x=20,y=190,width=250,height=30)


                            lbl_c_pass=Label(self.forget_win,text="Confirm New Password",font=("times new roman",15)).place(x=20,y=225)
                            txt_c_pass=Entry(self.forget_win,textvariable=self.var_confpass,font=("times new roman",15),bg="light yellow").place(x=20,y=255,width=250,height=30)

                            self.btn_update=Button(self.forget_win,text="Update",command=self.update_pass,state='disabled',font=("times new roman",15),bg="light blue")
                            self.btn_update.place(x=150,y=300,width=100,height=30)

            except Exception as ex:
                messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def update_pass(self):
        if self.var_newpass.get()=='' or self.var_confpass.get()=='':
            messagebox.showerror("Error","Password is required",parent=self.forget_win)
        elif self.var_newpass.get()!= self.var_confpass.get():
            messagebox.showerror("Error","New Password and confirm passowrd must be same",parent=self.forget_win)
        else:
            con=sqlite3.connect(database=r'ims.db')
            cur=con.cursor()
            try:
                cur.execute("Update employee SET pass=? where eid=?",(self.var_confpass.get(),self.var_employee_id.get()))
                con.commit()
                messagebox.showinfo("Success","Password updated successfully",parent=self.forget_win)
                self.forget_win.destroy()
            except Exception as ex:
                messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)
    
    def validate_otp(self):
        if int(self.otp)==int(self.var_otp.get()):
            self.btn_update.config(state=NORMAL)
            self.btn_reset.config(state=DISABLED)
        else:
            messagebox.showerror("Error","Invalid OTP",parent=self.forget_win)

    def send_email(self,to_):
        s=smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        email_=email_pass.email_
        pass_=email_pass.pass_

        s.login(email_,pass_)
        self.otp=int(str(time.strftime("%H%S%M")))+int(str(time.strftime("%S")))

        subj='IMS - Reset Password OTP'
        msg=f'Dear Sir/Madam\n\nYour Reset Password OTP is {str(self.otp)}.\n\nWith Regards,\nInventory Mangement System Team'
        msg="Subject:{}\n\n{}".format(subj,msg)
        s.sendmail(email_,to_,msg)
        chk=s.ehlo()
        if chk[0]==250:
            return 's'
        else:
            return 'f'
        
    def connect_to_database(self):
        #"""Connects to the SQLite database and returns a connection and cursor."""
        try:
            con = sqlite3.connect(database=r'ims.db')  # Adjust the path as needed
            cur = con.cursor()
            return con, cur
        except Exception as ex:
            messagebox.showerror("Error", f"Database connection error: {str(ex)}", parent=self.root)

root=Tk()
obj=Login_System(root)
root.mainloop()
