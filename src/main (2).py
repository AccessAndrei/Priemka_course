from tkinter.ttk import Combobox
import tkinter as tk
from tkinter import *



class Window_main(tk.Toplevel):
    def __init__(self,master=None):
        super().__init__(master)
        self.title ("Приемная комиссия РУТ(МИИТ)")
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.geometry("%dx%d" % (width, height))
        self.resizable(False,False)
        self.label_login = Label(self,text="Логин",font="Consolas 15").pack(anchor=CENTER,pady=30)
        self.entry_log_in = Entry(self, width=50, font="Consolas 15", bd=3).pack(anchor=CENTER, pady=30)
        self.label_password = Label(self, text="Пароль",font="Consolas 15").pack(anchor=CENTER,pady=30)
        self.entry_pass_in = Entry(self, width=50, font="Consolas 15", bd=3, show="*").pack(anchor=CENTER)
        self.button_enter=Button(self,text="Войти",font="Consolas 15",relief=GROOVE,bd=5,bg="#B3E5FC",fg="white",
                                 activebackground="#B3E5FC",activeforeground="white",command=self.get_text).pack(anchor=CENTER,pady=50)
        self.button_authorization=Button(self,text="Регистрация",font="Consolas 15",relief=GROOVE,bd=5,bg="#B3E5FC",fg="white",
                                         activebackground="#B3E5FC",activeforeground="white",
                                         command=self.open_window_authorization).pack(anchor=CENTER)
        self.button_exit=Button(self,text="Выйти",font="Consolas 15",command=self.destroy).pack(anchor=S,pady=50)


    def get_text(self):
        text1=self.entry_log_in.get()
        text2=self.entry_pass_in.get()
        data.append(text1)
        data.append(text2)
        print(data)

    def open_window_authorization(self):
        self.destroy()
        window_autorization=Window_authorization(self.master)



class Window_authorization(tk.Toplevel):
    def __init__(self,master=None):
        super().__init__(master)
        self.title ("Приемная комиссия РУТ(МИИТ)")
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.geometry("%dx%d" % (width, height))
        self.name_label=Label(self,text="Имя:").pack(anchor=CENTER)
        self.name_entry = Entry(self).pack(anchor=CENTER)
        self.surname_label=Label(self, text="Фамилия:").pack(anchor=CENTER)
        self.surname_entry = Entry(self).pack(anchor=CENTER)
        self.status_label=Label(self, text="Статус:").pack(anchor=CENTER)
        self.status_entry = Entry(self)
        self.status_choice = Combobox(self, values=(
        "Аббитуриент", "Секретарь", "Служащий приёмной комиссии", "Администратор"), state="readonly").pack()
        self.login_label=Label(self, text="Логин:").pack(anchor=CENTER)
        self.login_entry = Entry(self).pack(anchor=CENTER)
        self.password_label=Label(self, text="Пароль:").pack(anchor=CENTER)
        self.password_entry = Entry(self).pack(anchor=CENTER)
        self.button_authorization = Button(self, text="Зарегистрироваться", font="Consolas 15", relief=GROOVE, bd=5, bg="#B3E5FC",
                                   fg="white",
                                   activebackground="#B3E5FC", activeforeground="white", command=self.get_text).pack(anchor=CENTER,pady=30)

    def get_text(self):
        data = []
        text1=self.name_entry.get()
        text2=self.surname_entry.get()
        text3 = self.status_choice.get()
        text4 = self.login_entry.get()
        text5 = self.password_entry.get()
        data.append(text1)
        data.append(text2)
        data.append(text3)
        data.append(text4)
        data.append(text5)
        print(data)
        alldata.append(data)
        print(alldata)
        data.clear()




alldata=[]
data=[]
root=tk.Tk()
window=Window_main(root)
root.mainloop()