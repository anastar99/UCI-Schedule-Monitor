import tkinter as tk
from scrape import getEnrollInfo, getYear, checkSpace
import time

root = tk.Tk()
root.title("UCI-Schedule-Monitor")
canvas = tk.Canvas(root, width = 300, height = 120)
canvas.pack()

def courseCode():
    inp = inputtxt.get(1.0,"end-1c")
    label1 = tk.Label(root, text= 'Checking Open Spots', fg='blue', font=('helvetica', 12, 'bold'))
    canvas.create_window(150,70,window=label1)
    y = getYear()
    while True:
        try:
            inf = getEnrollInfo(y,str(inp))
        except AttributeError:
            label1.config(text = "Invalid Class Code!")
            break
        except IndexError:
            label1.config(text = "Please Enter a Class Code!")
            break
        flag = checkSpace(inf)
        if flag:
            label1.config(text = "Spot found! Email sent")
            break
        time.sleep(300)
title = tk.Label(root, text = "UCI Schedule Monitor", font=('bold', 16), fg='blue')
canvas.create_window(150,20,window=title,)

inputtxt = tk.Text(root, height = 1,width = 10)
canvas.create_window(150,50,window=inputtxt)

button = tk.Button(text = 'Check Spots!', command = courseCode, bg='brown')
button.pack()

canvas.create_window(150,100,window=button)

root.mainloop()