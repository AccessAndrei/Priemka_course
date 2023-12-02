import tkinter as tk
import Login






class AdminFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.title_label = tk.Label(self, text="Администратор", font="Consolas 20")
        self.title_label.pack(pady=20)

        # Виджеты для управления направлениями поступления
        self.directions_label = tk.Label(self, text="Направления поступления", font="Consolas 15")
        self.directions_label.pack(pady=10)
        self.direction_entry = tk.Entry(self, width=50, font="Consolas 15")
        self.direction_entry.pack(pady=10)
        self.add_direction_button = tk.Button(self, text="Добавить направление", font="Consolas 15",
                                              command=self.add_direction)
        self.add_direction_button.pack()
        self.directions_listbox = tk.Listbox(self, font="Consolas 15", selectmode=tk.SINGLE)
        self.directions_listbox.pack(pady=20)
        self.button_exit_admin = tk.Button(self, text="Выйти", font="Consolas 15",
                                           command=lambda: master.switch_frame(Login.StartPage))
        self.button_exit_admin.pack(pady=30)

    def add_direction(self):
        direction = self.direction_entry.get()
        if direction:
            self.directions_listbox.insert(tk.END, direction)
            self.direction_entry.delete(0, tk.END)


