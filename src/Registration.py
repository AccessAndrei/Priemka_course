
import tkinter as tk
from tkinter import ttk
import sqlite3 as sq
from tkinter import messagebox
import Login


class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.name_label = tk.Label(self, text="Имя:")
        self.name_label.pack(anchor=tk.CENTER)
        self.name_entry = tk.Entry(self)
        self.name_entry.pack(anchor=tk.CENTER)

        self.surname_label = tk.Label(self, text="Фамилия:")
        self.surname_label.pack(anchor=tk.CENTER)
        self.surname_entry = tk.Entry(self)
        self.surname_entry.pack(anchor=tk.CENTER)

        self.status_label = tk.Label(self, text="Статус:")
        self.status_label.pack(anchor=tk.CENTER)
        self.status_choice = ttk.Combobox(self, values=(
            "Аббитуриент", "Секретарь", "Служащий приёмной комиссии", "Администратор"), state="readonly")
        self.status_choice.pack(anchor=tk.CENTER)

        self.login_label = tk.Label(self, text="Логин:")
        self.login_label.pack(anchor=tk.CENTER)
        self.login_entry = tk.Entry(self)
        self.login_entry.pack(anchor=tk.CENTER)

        self.password_label = tk.Label(self, text="Пароль:")
        self.password_label.pack(anchor=tk.CENTER)
        self.password_entry = tk.Entry(self)
        self.password_entry.pack(anchor=tk.CENTER)

        self.button_authorization = tk.Button(self, text="Зарегистрироваться", font="Consolas 15", relief=tk.GROOVE,
                                              bd=5,
                                              bg="#B3E5FC", fg="white",
                                              activebackground="#B3E5FC", activeforeground="white",
                                              command=self.register_and_return)
        self.button_authorization.pack(anchor=tk.CENTER, pady=30)
        self.button_exit = tk.Button(self, text="Выйти", font="Consolas 15", command=master.destroy)
        self.button_exit.pack(anchor=tk.S, pady=50)

    def register_and_return(self):
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        status = self.status_choice.get()
        login = self.login_entry.get()
        password = self.password_entry.get()
        self.registration(name, surname, status, login, password)

    def registration(self, name, surname, status, login, password):
        if not (name and surname and status and login and password):
            messagebox.showerror("Ошибка", "Заполните все поля")
            return
        try:
            db = sq.connect('../database/priemka.db')
            cursor = db.cursor()
            cursor.execute("""
            SELECT login FROM users WHERE login = ?
            """, [login])
            if cursor.fetchone() is None:
                cursor.execute("INSERT INTO users(login, fullname, status, password) VALUES (?,?,?,?)",
                               [login, name + " " + surname, status, password])
                db.commit()
                self.master.switch_frame(Login.StartPage)
            else:
                self.login_entry.delete(0, tk.END)
                messagebox.showerror("Ошибка", "Такой логин уже существует")

        except sq.Error as e:
            print(e)
        finally:
            cursor.close()
            db.close()