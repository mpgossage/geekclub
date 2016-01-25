from tkinter import *
import random

master = Tk()
w = Canvas(master, width=500, height=500)
w.pack()

colours = [ 'red','black']

for y in range(500, 0, -8):
    f = random.choice(colours)
    for x in range(y, 500-a, 7):
        w.create_line(x, a, 5-x-y, 500-a,
                      fill=f)
    w.update()

mainloop()
