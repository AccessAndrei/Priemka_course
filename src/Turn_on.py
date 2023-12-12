import tkinter as tk
import Login



class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Приемная комиссия РУТ(МИИТ)")
        self._frame = None
        self.switch_frame(Login.StartPage)

    def switch_frame(self, frame_class, user_id=None):
        """Уничтожает текущий фрейм и заменяет его на новый фрейм."""
        new_frame = frame_class(self, user_id) if user_id else frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()






if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
