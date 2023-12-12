import tkinter as tk
import sqlite3 as sq
from tkinter import messagebox
import Login


class Secretary(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.greeting_label = tk.Label(self, text="Вы зашли как секретарь", anchor="nw")
        self.greeting_label.pack()

        self.confirm_original_button = tk.Button(self, text="Подтвердить оригинал",
                                                 command=lambda: master.switch_frame(ConfirmOriginalFrame))
        self.confirm_original_button.pack(anchor=tk.CENTER)
        self.confirm_original_button = tk.Button(self, text="Отозвать оригинал",
                                                 command=lambda: master.switch_frame(DeleteOriginalFrame))
        self.confirm_original_button.pack(anchor=tk.CENTER)
        self.back_button = tk.Button(self, text="Выйти", command=lambda: self.master.switch_frame(Login.StartPage))
        self.back_button.pack()

        # self.end_selection_button = tk.Button(self, text="Конец конкурсного отбора",
        #                                       command=lambda: master.switch_frame(EndSelectionFrame))
        # self.end_selection_button.pack(anchor=tk.CENTER)


class ConfirmOriginalFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.directions_listbox = tk.Listbox(self)
        self.directions_listbox.pack(anchor=tk.CENTER)

        self.load_directions_button = tk.Button(self, text="Выбрать направление", command=self.load_applicants)
        self.load_directions_button.pack(anchor=tk.CENTER)

        self.applicants_listbox = tk.Listbox(self)
        self.applicants_listbox.pack(anchor=tk.CENTER)

        self.confirm_button = tk.Button(self, text="Подтвердить оригинал", command=self.confirm_original)
        self.confirm_button.pack(anchor=tk.CENTER)
        self.back_button = tk.Button(self, text="Назад",
                                     command=lambda: master.switch_frame(Secretary))
        self.back_button.pack()

        self.load_directions()

    def load_directions(self):
        try:
            db = sq.connect('../database/priemka.db')
            cursor = db.cursor()
            cursor.execute("SELECT * FROM directions")
            for row in cursor.fetchall():
                self.directions_listbox.insert(tk.END, f"{row[0]}: {row[1]}")
        except sq.Error as e:
            print(e)
        finally:
            cursor.close()
            db.close()


    def load_applicants(self):
        if self.directions_listbox.curselection():
            selected_direction = self.directions_listbox.get(self.directions_listbox.curselection())
            direction_id = int(selected_direction.split(":")[0])
            try:
                db = sq.connect('../database/priemka.db')
                cursor = db.cursor()
                cursor.execute("""
                    SELECT users.id, users.fullname FROM admission_results
                    JOIN users ON users.id = admission_results.applicant_id
                    JOIN applicants ON applicants.applicant_id = admission_results.applicant_id
                    WHERE admission_results.direction_id = ? AND applicants.original = 0
                """, [direction_id])
                self.applicants_listbox.delete(0, tk.END)
                for row in cursor.fetchall():
                    self.applicants_listbox.insert(tk.END, f"{row[0]}: {row[1]}")
            except sq.Error as e:
                print(e)
            finally:
                cursor.close()
                db.close()

    def confirm_original(self):
        if self.applicants_listbox.curselection():
            selected_applicant = self.applicants_listbox.get(self.applicants_listbox.curselection())
            applicant_id = int(selected_applicant.split(":")[0])
            try:
                db = sq.connect('../database/priemka.db')
                cursor = db.cursor()
                cursor.execute("UPDATE applicants SET original = 1 WHERE applicant_id = ?", [applicant_id])
                db.commit()
                messagebox.showinfo("Успешно", "Оригинал подтвержден")
            except sq.Error as e:
                print(e)
            finally:
                cursor.close()
                db.close()
                self.load_applicants()  # обновляем список абитуриентов после изменения статуса


class DeleteOriginalFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.directions_listbox = tk.Listbox(self)
        self.directions_listbox.pack(anchor=tk.CENTER)

        self.load_directions_button = tk.Button(self, text="Выбрать направление", command=self.load_applicant)
        self.load_directions_button.pack(anchor=tk.CENTER)

        self.applicants_listbox = tk.Listbox(self)
        self.applicants_listbox.pack(anchor=tk.CENTER)

        self.confirm_button = tk.Button(self, text="Отозвать оригинал", command=self.confirm_original)
        self.confirm_button.pack(anchor=tk.CENTER)
        self.back_button = tk.Button(self, text="Назад",
                                     command=lambda: master.switch_frame(Secretary))
        self.back_button.pack()

        self.load_directions()

    def load_directions(self):
        try:
            db = sq.connect('../database/priemka.db')
            cursor = db.cursor()
            cursor.execute("SELECT * FROM directions")
            for row in cursor.fetchall():
                self.directions_listbox.insert(tk.END, f"{row[0]}: {row[1]}")
        except sq.Error as e:
            print(e)
        finally:
            cursor.close()
            db.close()



    def load_applicant(self):
        if self.directions_listbox.curselection():
            selected_direction = self.directions_listbox.get(self.directions_listbox.curselection())
            direction_id = int(selected_direction.split(":")[0])
            print(direction_id)
            try:
                db = sq.connect('../database/priemka.db')
                cursor = db.cursor()
                cursor.execute("""
                    SELECT users.id, users.fullname FROM admission_results
                    JOIN users ON users.id = admission_results.applicant_id
                    JOIN applicants ON applicants.applicant_id = admission_results.applicant_id
                    WHERE admission_results.direction_id = ? AND applicants.original = 1
                """, [direction_id])
                self.applicants_listbox.delete(0, tk.END)
                for row in cursor.fetchall():
                    self.applicants_listbox.insert(tk.END, f"{row[0]}: {row[1]}")
            except sq.Error as e:
                print(e)
            finally:
                cursor.close()
                db.close()

    def confirm_original(self):
        if self.applicants_listbox.curselection():
            selected_applicant = self.applicants_listbox.get(self.applicants_listbox.curselection())
            applicant_id = int(selected_applicant.split(":")[0])
            try:
                db = sq.connect('../database/priemka.db')
                cursor = db.cursor()
                cursor.execute("UPDATE applicants SET original = 0 WHERE applicant_id = ?", [applicant_id])
                db.commit()
                messagebox.showinfo("Успешно", "Оригинал отозван")
            except sq.Error as e:
                print(e)
            finally:
                cursor.close()
                db.close()
                self.load_applicant()  # обновляем список абитуриентов после изменения статуса