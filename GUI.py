from keras.models import load_model
from tkinter import *
import tkinter as tk
import win32gui
from PIL import ImageGrab
import numpy as np

model = load_model('HWRS.h5')


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.x = self.y = 0

        self.canvas = tk.Canvas(self, width=300, height=300, bg="white", cursor="cross")
        self.label = tk.Label(self, text="Write?", font=('Helvetica', 48))
        self.identify_btn = tk.Button(self, text="Identify", command=self.identify_digit)
        self.button_erase = tk.Button(self, text="Erase", command=self.clear_all)

        # GUI GRID Structure
        self.canvas.grid(row=0, column=0, pady=2, sticky=W)
        self.label.grid(row=0, column=1, pady=2, padx=2)
        self.identify_btn.grid(row=1, column=1, pady=2, padx=2)
        self.button_erase.grid(row=1, column=0, pady=5)

        self.canvas.bind("<B1-Motion>", self.draw_figure)

    def clear_all(self):
        self.canvas.delete("all")

    def identify_digit(self):
        Input = self.canvas.winfo_id()
        rect = win32gui.GetWindowRect(Input)
        image = ImageGrab.grab(rect)
        digit, accuracy = predict_the_digit(image)
        self.label.configure(text=str(digit) + ' ' + str(int(accuracy * 100)) + '%')

    def draw_figure(self, event):
        self.x = event.x
        self.y = event.y
        r = 8
        self.canvas.create_oval(self.x - r, self.y - r, self.x + r, self.y + r, fill='black')


def predict_the_digit(img):
    img = img.resize((28, 28))
    img = img.convert('L')
    img = np.array(img)
    img = img.reshape(-1, 28, 28, 1)
    img = img / 255.0
    res = model.predict([img], verbose=1)[0]
    return np.argmax(res), max(res)


app = App()
mainloop()
