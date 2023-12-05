import tkinter as tk


class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('600x500')
        self.title("Ordinary Weather")
        self.iconbitmap("WeatherAppIcon.ico")
        self.resizable(True, True)
        button = tk.Button(self, text= "test")
        button.pack()


def main():
    WeatherApp().mainloop()


if __name__ == '__main__':
    main()
