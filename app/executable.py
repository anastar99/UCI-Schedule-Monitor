import tkinter as tk
from scrape import getEnrollInfo, getYear, checkSpace

root = tk.Tk()
root.title("UCI-Schedule-Monitor")
canvas = tk.Canvas(root, width = 300, height = 300)
canvas.pack()

def courseCode():
    inp = inputtxt.get(1.0, "end-1c")
    label1 = tk.Label(root, text= 'Checking Open Spots', fg='blue', font=('helvetica', 12, 'bold'))
    canvas.create_window(150, 200, window=label1)
    y = getYear()
    inf = getEnrollInfo(y,str(inp))
    flag = checkSpace(inf)
    if flag:
        label2 = tk.Label(root, text= 'Spot Found', fg='blue', font=('helvetica', 12, 'bold'))
        canvas.create_window(150, 200, window=label2)


inputtxt = tk.Text(root,height = 1,width = 10)
inputtxt.pack()

button = tk.Button(text = 'Check Spots!', command = courseCode, bg='brown')
button.pack()

canvas.create_window(150,150,window=button)


root.mainloop()