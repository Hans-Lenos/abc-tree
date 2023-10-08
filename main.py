import tkinter as tk
from view import View


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('ABC Tree')

        # create a view and place it on the root window
        self.geometry("1000x800")
        view = View(self)
        view.grid(row=0, column=0, padx=10, pady=10)


if __name__ == '__main__':
    app = App()
    app.mainloop()
