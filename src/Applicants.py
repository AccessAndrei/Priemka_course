import tkinter as tk
import sqlite3 as sq
from tkinter import messagebox
import Login


class ApplicantsFrame(tk.Frame):
    def __init__(self, master, user_id):
        tk.Frame.__init__(self, master)
        self.user_id = user_id

        # Получаем имя и фамилию пользователя из базы данных
        self.user_name = self.get_user_name()

        # Отображаем имя и фамилию пользователя в верхнем левом углу
        self.name_label = tk.Label(self, text=self.user_name, anchor="nw")
        self.name_label.pack()

        # Создаем кнопки для подачи документов и просмотра результатов
        self.submit_documents_button = tk.Button(self, text="Подача документов на специальность",
                                                 command=lambda: master.switch_frame(SubmitDocumentsFrame,
                                                                                     self.user_id))
        self.submit_documents_button.pack(padx=10, pady=10)

        self.view_results_button = tk.Button(self, text="Результаты конкурса",
                                             command=lambda: master.switch_frame(AdmissionResultsFrame, user_id))
        self.view_results_button.pack()
        self.select_direction_button = tk.Button(self, text="Выбрать направление",
                                                 command=lambda: master.switch_frame(DirectionsFrame, self.user_id))
        self.select_direction_button.pack(padx=10, pady=10)
        self.back_button = tk.Button(self, text="Выйти", command=lambda: self.master.switch_frame(Login.StartPage))
        self.back_button.pack(anchor=tk.S, pady=50)

    def get_user_name(self):
        try:
            db = sq.connect('../database/priemka.db')
            cursor = db.cursor()
            cursor.execute("SELECT fullname FROM users WHERE id = ?", [self.user_id])
            user_name = cursor.fetchone()[0]
            cursor.execute("SELECT sub1, sub2, sub3 FROM applicants WHERE applicant_id = ?", [self.user_id])
            if cursor.fetchone() is not None:
                user_name+=" | Документы поданы"
            else:
                user_name+=" | Документы не поданы"
        except sq.Error as e:
            print(e)
        finally:
            cursor.close()
            db.close()
        return user_name


class SubmitDocumentsFrame(tk.Frame):
    def __init__(self, master, user_id):
        tk.Frame.__init__(self, master)
        self.user_id = user_id
        self.attestat_label = tk.Label(self, text="Аттестат:")
        self.attestat_label.pack(anchor=tk.CENTER)
        self.attestat_entry = tk.Entry(self)
        self.attestat_entry.pack(anchor=tk.CENTER)

        self.sub1_label = tk.Label(self, text="Баллы 1 экзамена:")
        self.sub1_label.pack(anchor=tk.CENTER)
        self.sub1_entry = tk.Entry(self)
        self.sub1_entry.pack(anchor=tk.CENTER)

        self.sub2_label = tk.Label(self, text="Баллы 2 экзамена:")
        self.sub2_label.pack(anchor=tk.CENTER)
        self.sub2_entry = tk.Entry(self)
        self.sub2_entry.pack(anchor=tk.CENTER)

        self.sub3_label = tk.Label(self, text="Баллы 3 экзамена:")
        self.sub3_label.pack(anchor=tk.CENTER)
        self.sub3_entry = tk.Entry(self)
        self.sub3_entry.pack(anchor=tk.CENTER)

        self.submit_button = tk.Button(self, text="Подтвердить", command=self.submit_documents)
        self.submit_button.pack(anchor=tk.CENTER, pady=30)

        self.button_exit = tk.Button(self, text="Выйти", font="Consolas 15",
                                     command=lambda: master.switch_frame(ApplicantsFrame, self.user_id))
        self.button_exit.pack(anchor=tk.S, pady=50)

    def submit_documents(self):
        attestat = self.attestat_entry.get()
        sub1 = self.sub1_entry.get()
        sub2 = self.sub2_entry.get()
        sub3 = self.sub3_entry.get()
        if not (attestat.isdigit() and sub1.isdigit() and sub2.isdigit() and sub3.isdigit()):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены целочисленными значениями")
            return
        elif not (0 <= int(sub1) <= 100) or not (0 <= int(sub2) <= 100) or not (0 <= int(sub3) <= 100):
            messagebox.showerror("Ошибка", "Баллы должны быть в диапазоне от 0 до 100")
            return
        elif len(attestat) != 14:
            messagebox.showerror("Ошибка", "Аттестат должен состоять из 14 символов")
            return
        try:
            db = sq.connect('../database/priemka.db')
            cursor = db.cursor()
            cursor.execute("SELECT applicant_id FROM applicants WHERE applicant_id = ?", [self.user_id])
            if cursor.fetchone() is not None:
                messagebox.showerror("Ошибка", "Документы уже поданы")
                return
            cursor.execute(
                "INSERT INTO applicants(applicant_id, attestat, sub1, sub2, sub3, original) VALUES (?, ?, ?, ?, ?, ?)",
                [self.user_id, attestat, sub1, sub2, sub3, 0])
            db.commit()
            messagebox.showinfo("Успех", "Документы успешно поданы")
        except sq.Error as e:
            print(e)
        finally:
            cursor.close()
            db.close()
            self.master.switch_frame(ApplicantsFrame, self.user_id)


class AdmissionResultsFrame(tk.Frame):
    def __init__(self, master, user_id):
        tk.Frame.__init__(self, master)
        self.master = master
        self.user_id = user_id
        self.directions_listbox = tk.Listbox(self,width=60)
        self.directions_listbox.pack(anchor=tk.CENTER)

        self.load_directions_button = tk.Button(self, text="Загрузить абитуриентов", command=self.load_applicants)
        self.load_directions_button.pack(anchor=tk.CENTER)

        self.applicants_listbox = tk.Listbox(self, width=50)
        self.applicants_listbox.pack(anchor=tk.CENTER)

        self.back_button = tk.Button(self, text="Назад", command=lambda: self.master.switch_frame(ApplicantsFrame, self.user_id))
        self.back_button.pack(anchor=tk.S, pady=50)

        self.load_directions()

    def load_directions(self):
        try:
            db = sq.connect('../database/priemka.db')
            cursor = db.cursor()
            cursor.execute("""
                SELECT directions.direction_id, directions.num_of_direction, directions.name, directions.amount
            FROM admission_results
            JOIN directions ON directions.direction_id = admission_results.direction_id
            WHERE admission_results.applicant_id = ? AND admission_results.checked = 1
            """, [self.user_id])
            directions = cursor.fetchall()
            for direction in directions:
                self.directions_listbox.insert(tk.END, str(direction[0]) + ": " + direction[1] + " " + direction[2]+"|Количество мест: "+str(direction[3]))
        except sq.Error as e:
            print(e)
        finally:
            cursor.close()
            db.close()

    def load_applicants(self):
        if self.directions_listbox.curselection():
            selected_direction = self.directions_listbox.get(self.directions_listbox.curselection())
            direction_id = int(selected_direction.split(":")[0])
            print(direction_id)
            try:
                db = sq.connect('../database/priemka.db')
                cursor = db.cursor()
                cursor.execute("""
                    SELECT users.id, users.fullname, applicants.sub1, applicants.sub2, applicants.sub3, applicants.original
                    FROM admission_results
                    JOIN users ON users.id = admission_results.applicant_id
                    JOIN applicants ON applicants.applicant_id = admission_results.applicant_id
                    WHERE admission_results.direction_id = ? AND admission_results.checked = 1
                    ORDER BY applicants.sub1 + applicants.sub2 + applicants.sub3 DESC
                """, [direction_id])
                self.applicants_listbox.delete(0, tk.END)
                rows = cursor.fetchall()
                print(rows)
                for row in rows:
                    original: str
                    if row[5] == 1: original = "Подан"
                    else: original = "Не подан"

                    self.applicants_listbox.insert(tk.END,
                                                   f"{row[0]}: {row[1]}| Баллы: {int(row[2]) + int(row[3]) + int(row[4])} | Оригинал: {original}")
            except sq.Error as e:
                print(e)
            finally:
                cursor.close()
                db.close()


class DirectionsFrame(tk.Frame):
    def __init__(self, master, user_id):
        tk.Frame.__init__(self, master)
        self.user_id = user_id
        self.title_label = tk.Label(self, text="Выберите направление:")
        self.title_label.pack()

        self.directions_listbox = tk.Listbox(self, width=90)
        self.directions_listbox.pack(fill=tk.BOTH, expand=1)

        self.load_directions()

        self.select_button = tk.Button(self, text="Выбрать", command=self.select_direction)
        self.select_button.pack(pady=10)

        self.back_button = tk.Button(self, text="Назад",
                                     command=lambda: master.switch_frame(ApplicantsFrame, self.user_id))
        self.back_button.pack()

    def load_directions(self):
        try:
            db = sq.connect('../database/priemka.db')
            cursor = db.cursor()
            cursor.execute("SELECT direction_id,num_of_direction,name, amount FROM directions")
            directions = cursor.fetchall()
            for direction in directions:
                self.directions_listbox.insert(tk.END, str(direction[0]) + ": " +
                                               direction[1] + " " + direction[2]+" | Количество мест: "+str(direction[3]))
        except sq.Error as e:
            print(e)
        finally:
            cursor.close()
            db.close()

    def select_direction(self):
        selected_direction = self.directions_listbox.get(self.directions_listbox.curselection())
        direction_id = int(selected_direction.split(":")[0])
        try:
            db = sq.connect('../database/priemka.db')
            cursor = db.cursor()
            cursor.execute("SELECT * FROM admission_results WHERE applicant_id = ? AND direction_id = ?",
                           [self.user_id, direction_id])
            if cursor.fetchone() is not None:
                messagebox.showerror("Ошибка", "Это направление уже выбрано")
                return
            cursor.execute("INSERT INTO admission_results (applicant_id, direction_id) VALUES (?, ?)",
                           [self.user_id, direction_id])
            db.commit()
            messagebox.showinfo("Успешно", "Направление успешно выбрано")
        except sq.Error as e:
            print(e)
        finally:
            cursor.close()
            db.close()
            self.master.switch_frame(ApplicantsFrame, self.user_id)

