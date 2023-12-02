import tkinter as tk
import sqlite3 as sq
from tkinter import messagebox
import Admin
import Registration



class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.label_login = tk.Label(self, text="Логин", font="Consolas 15")
        self.label_login.pack(anchor=tk.CENTER, pady=30)
        self.entry_log_in = tk.Entry(self, width=50, font="Consolas 15", bd=3)
        self.entry_log_in.pack(anchor=tk.CENTER, pady=10)

        self.label_password = tk.Label(self, text="Пароль", font="Consolas 15")
        self.label_password.pack(anchor=tk.CENTER, pady=10)
        self.entry_pass_in = tk.Entry(self, width=50, font="Consolas 15", bd=3, show="*")
        self.entry_pass_in.pack(anchor=tk.CENTER)

        self.button_enter = tk.Button(self, text="Войти", font="Consolas 15", relief=tk.GROOVE, bd=5, bg="#B3E5FC",
                                      fg="white", activebackground="#B3E5FC", activeforeground="white",
                                      command=self.login)
        self.button_enter.pack(anchor=tk.CENTER, pady=30)

        self.button_authorization = tk.Button(self, text="Регистрация", font="Consolas 15", relief=tk.GROOVE, bd=5,
                                              bg="#B3E5FC", fg="white", activebackground="#B3E5FC",
                                              activeforeground="white", command=lambda: master.switch_frame(Registration.PageOne))
        self.button_authorization.pack(anchor=tk.CENTER)

        self.button_exit = tk.Button(self, text="Выйти", font="Consolas 15", command=master.destroy)
        self.button_exit.pack(anchor=tk.S, pady=50)

    def login(self):
        login = self.entry_log_in.get()
        password = self.entry_pass_in.get()
        try:
            db = sq.connect('../database/priemka.db')
            cursor = db.cursor()
            cursor.execute("SELECT login, password, status FROM users WHERE login = ? AND password = ?", [login, password])
            data = cursor.fetchall()
            print(data)
            if login in data[0][0] and password in data[0][1]:
                if data[0][2] == "Администратор":
                    self.master.switch_frame(Admin.AdminFrame)
            else:
                print("неверный логин или пароль")
                self.show_error_message("Ошибка", "Неверный логин или пароль")

        except sq.Error as e:
            print(e)
        finally:
            cursor.close()
            db.close()

    def show_error_message(self, title, message):
        messagebox.showerror(title, message)

