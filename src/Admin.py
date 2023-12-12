import tkinter as tk
from tkinter import messagebox
import sqlite3 as sq
import Login


class AdminFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.greeting_label = tk.Label(self, text="Вы зашли как Администратор", anchor="nw")
        self.greeting_label.pack()
        self.add_speciality_button = tk.Button(self, text="Добавить специальность",
                                               command=lambda: self.master.switch_frame(AddSpecialityFrame))
        self.add_applicant_button = tk.Button(self, text="Добавить абитуриента",
                                              command=lambda: self.master.switch_frame(ApplicantAdd))
        self.add_applicant_button.pack()
        self.third_button = tk.Button(self, text="Удалить абитуриента",
                                      command=lambda: self.master.switch_frame(DeleteApplicant))
        self.back_button = tk.Button(self, text="Выйти", command=lambda: self.master.switch_frame(Login.StartPage))
        self.add_speciality_button.pack()
        self.third_button.pack()
        self.back_button.pack()


class AddSpecialityFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master

        self.speciality_name_label = tk.Label(self, text="Название специальности:")
        self.speciality_name_label.pack(anchor=tk.CENTER)
        self.speciality_name_entry = tk.Entry(self)
        self.speciality_name_entry.pack(anchor=tk.CENTER)

        self.direction_specifier_label = tk.Label(self, text="Спецификатор направления XX.XX.XX:")
        self.direction_specifier_label.pack(anchor=tk.CENTER)
        self.direction_specifier_entry = tk.Entry(self)
        self.direction_specifier_entry.pack(anchor=tk.CENTER)

        self.number_of_seats_label = tk.Label(self, text="Количество мест приема:")
        self.number_of_seats_label.pack(anchor=tk.CENTER)
        self.number_of_seats_entry = tk.Entry(self)
        self.number_of_seats_entry.pack(anchor=tk.CENTER)
        self.submit_button = tk.Button(self, text="Добавить специальность", command=self.submit)
        self.submit_button.pack(anchor=tk.CENTER)

        self.back_button = tk.Button(self, text="Назад", command=lambda: self.master.switch_frame(AdminFrame))
        self.back_button.pack(anchor=tk.S, pady=50)

    def submit(self):
        speciality_name = self.speciality_name_entry.get()
        direction_specifier = self.direction_specifier_entry.get()
        number_of_seats = self.number_of_seats_entry.get()

        if not speciality_name or not direction_specifier or not number_of_seats:
            messagebox.showerror("Ошибка", "Все строки должны быть заполнены")
            return
        try:
            db = sq.connect('../database/priemka.db')
            cursor = db.cursor()
            cursor.execute("SELECT name FROM directions WHERE name = ?", [speciality_name])
            if cursor.fetchone():
                messagebox.showerror("Ошибка", "Такая специальность уже существует")
                return
            cursor.execute("SELECT num_of_direction FROM directions WHERE num_of_direction = ?", [direction_specifier])
            if cursor.fetchone():
                messagebox.showerror("Ошибка", "Такая специальность уже существует")
                return
            if not number_of_seats.isdigit():
                messagebox.showerror("Ошибка", "Количество мест должно быть целочисленным значением")
                return
            cursor.execute("INSERT INTO directions (num_of_direction, name, amount) VALUES (?, ?, ?)",
                           [direction_specifier, speciality_name, number_of_seats])
            db.commit()
        except sq.Error as e:
            print(e)
        finally:
            self.master.switch_frame(AdminFrame)
            cursor.close()
            db.close()


class ApplicantAdd(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master

        self.speciality_listbox = tk.Listbox(self, width=50)
        self.speciality_listbox.pack(anchor=tk.CENTER)

        self.load_applicants_button = tk.Button(self, text="Загрузить абитуриентов", command=self.load_applicants)
        self.load_applicants_button.pack(anchor=tk.CENTER)

        self.applicants_listbox = tk.Listbox(self, width=50)
        self.applicants_listbox.pack(anchor=tk.CENTER)
        self.confirm_button = tk.Button(self, text="Подтвердить", command=self.check_applicant)
        self.confirm_button.pack(anchor=tk.CENTER)

        self.back_button = tk.Button(self, text="Назад", command=lambda: self.master.switch_frame(AdminFrame))
        self.back_button.pack(anchor=tk.S, pady=50)
        self.picked_speciality = None
        self.load_specialities()

    def load_specialities(self):
        try:
            db = sq.connect('../database/priemka.db')
            cursor = db.cursor()
            cursor.execute("SELECT * FROM directions")
            for row in cursor.fetchall():
                self.speciality_listbox.insert(tk.END, f"{row[0]}: {row[1]} {row[2]}")
        except sq.Error as e:
            print(e)
        finally:
            cursor.close()
            db.close()

    def check_applicant(self):
        if self.applicants_listbox.curselection():
            selected_applicant = self.applicants_listbox.get(self.applicants_listbox.curselection())
            applicant_id = int(selected_applicant.split(":")[0])
            try:
                db = sq.connect('../database/priemka.db')
                cursor = db.cursor()
                cursor.execute("UPDATE admission_results SET checked = 1 WHERE applicant_id = ? AND direction_id = ?", [applicant_id, self.picked_speciality])
                db.commit()
                messagebox.showinfo("Успешно", "Абитуриент проверен")
            except sq.Error as e:
                print(e)
            finally:
                cursor.close()
                db.close()
                self.load_applicants()

    def load_applicants(self):
        if self.speciality_listbox.curselection():
            selected_speciality = self.speciality_listbox.get(self.speciality_listbox.curselection())
            speciality_id = int(selected_speciality.split(":")[0])
            self.picked_speciality = speciality_id
            try:
                db = sq.connect('../database/priemka.db')
                cursor = db.cursor()
                cursor.execute("""
                                            SELECT users.id, users.fullname FROM admission_results
                                            JOIN users ON users.id = admission_results.applicant_id
                                            WHERE direction_id = ? AND checked is NULL
                                        """, [speciality_id])
                self.applicants_listbox.delete(0, tk.END)
                for row in cursor.fetchall():
                    self.applicants_listbox.insert(tk.END, f"{row[0]}: {row[1]}")
            except sq.Error as e:
                print(e)
            finally:
                cursor.close()
                db.close()


class DeleteApplicant(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.directions_listbox = tk.Listbox(self, width=50)
        self.directions_listbox.pack(anchor=tk.CENTER)
        self.picked_direction = None
        self.load_directions_button = tk.Button(self, text="Загрузить абитуриентов", command=self.load_applicants)
        self.load_directions_button.pack(anchor=tk.CENTER)
        self.applicants_listbox = tk.Listbox(self, width=50)
        self.applicants_listbox.pack(anchor=tk.CENTER)
        self.delete_button = tk.Button(self, text="Удалить абитуриента", command=self.delete_applicant)
        self.delete_button.pack(anchor=tk.CENTER)

        self.back_button = tk.Button(self, text="Назад", command=lambda: self.master.switch_frame(AdminFrame))
        self.back_button.pack(anchor=tk.S, pady=50)

        self.load_directions()

    def load_directions(self):
        try:
            db = sq.connect('../database/priemka.db')
            cursor = db.cursor()
            cursor.execute("""
                SELECT directions.direction_id, directions.num_of_direction, directions.name, directions.amount
            FROM directions
            """)
            directions = cursor.fetchall()
            for direction in directions:
                self.directions_listbox.insert(tk.END, str(direction[0]) + ": " + direction[1] + " " + direction[2]+ "| Количество мест: " + str(direction[3]))
        except sq.Error as e:
            print(e)
        finally:
            cursor.close()
            db.close()

    def load_applicants(self):
        if self.directions_listbox.curselection():
            selected_direction = self.directions_listbox.get(self.directions_listbox.curselection())
            self.picked_direction = selected_direction
            direction_id = int(selected_direction.split(":")[0])
            try:
                db = sq.connect('../database/priemka.db')
                cursor = db.cursor()
                cursor.execute("""
                    SELECT users.id, users.fullname, applicants.sub1, applicants.sub2, applicants.sub3, applicants.original
                    FROM admission_results
                    JOIN users ON users.id = admission_results.applicant_id
                    JOIN applicants ON applicants.applicant_id = admission_results.applicant_id
                    WHERE admission_results.direction_id = ? AND admission_results.checked = 1
                """, [direction_id])
                self.applicants_listbox.delete(0, tk.END)
                rows = cursor.fetchall()
                print(rows)
                for row in rows:
                    original: str
                    if row[5]!=0: original = "Подан"
                    else: original = "Не подан"
                    self.applicants_listbox.insert(tk.END,
                                                   f"{row[0]}: {row[1]}| Баллы: {int(row[2]) + int(row[3]) + int(row[4])}| Оригинал: {original}")
            except sq.Error as e:
                print(e)
            finally:
                cursor.close()
                db.close()

    def delete_applicant(self):
        if self.applicants_listbox.curselection():
            selected_applicant = self.applicants_listbox.get(self.applicants_listbox.curselection())
            applicant_id = int(selected_applicant.split(":")[0])
            direction_id = int(self.picked_direction.split(":")[0])
            try:
                db = sq.connect('../database/priemka.db')
                cursor = db.cursor()
                cursor.execute(
                    "UPDATE admission_results SET checked = NULL WHERE applicant_id = ? AND direction_id = ?",
                    [applicant_id, direction_id])
                db.commit()
                messagebox.showinfo("Успешно", "Абитуриент удален")
            except sq.Error as e:
                print(e)
            finally:
                cursor.close()
                db.close()
                self.load_applicants()
