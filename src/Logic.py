import tkinter as tk
from tkinter import ttk

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Приемная комиссия РУТ(МИИТ)")
        self.geometry("800x600")
        self.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
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
                                      command=self.get_text)
        self.button_enter.pack(anchor=tk.CENTER, pady=30)

        self.button_authorization = tk.Button(self, text="Регистрация", font="Consolas 15", relief=tk.GROOVE, bd=5,
                                              bg="#B3E5FC", fg="white", activebackground="#B3E5FC",
                                              activeforeground="white", command=self.open_window_authorization)
        self.button_authorization.pack(anchor=tk.CENTER)

        self.button_exit = tk.Button(self, text="Выйти", font="Consolas 15", command=self.exit_application)
        self.button_exit.pack(anchor=tk.S, pady=50)

    def exit_application(self):
        self.destroy()

    def get_text(self):
        text1 = self.entry_log_in.get()
        text2 = self.entry_pass_in.get()
        data.append(text1)
        data.append(text2)
        print(data)

    def open_window_authorization(self):
        self.withdraw()  # Скрываем текущее окно
        window_authorization = WindowAuthorization(self)
        window_authorization.protocol("WM_DELETE_WINDOW", self.show_main_window)  # Обработка закрытия окна авторизации

    def show_main_window(self):
        self.deiconify()  # Восстанавливаем главное окно

class WindowAuthorization(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Приемная комиссия РУТ(МИИТ)")
        self.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
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
        self.status_choice = ttk.Combobox(self, values=("Аббитуриент", "Секретарь", "Служащий приёмной комиссии", "Администратор"), state="readonly")
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


    def register(self):
        text1 = self.name_entry.get()
        text2 = self.surname_entry.get()
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

    def register_and_return(self):
        self.register()  # Регистрируем пользователя
        self.destroy()
        self.master.show_main_window()

if __name__ == "__main__":
    data = []  # Данные, собранные при входе
    alldata = []  # Данные, собранные при регистрации
    app = Application()
    app.mainloop()
