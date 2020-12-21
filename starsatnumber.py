from skyfield.api import load
from tkinter.ttk import *
from tkinter import *
from satnum import satnum


def count(start_time, exposition, eq_cords, field_of_view):
    res_bar['value'] = 0
    window.update_idletasks()
    ts = load.timescale()
    date = start_time.get().split('-')
    date = list(map(int, date))
    start_time = ts.utc(*date)
    exposition = int(exposition.get())
    field_of_view = int(field_of_view.get())
    eq_cords = eq_cords.get().split(' ')
    eq_cords = list(map(float, eq_cords))

    res_bar['value'] = 50
    window.update_idletasks()
    answer = satnum(start_time, exposition, eq_cords, field_of_view)
    result.config(text=str(answer))
    res_bar['value'] = 100
    window.update_idletasks()


window = Tk()
window.title("Satellites Number")
window.geometry('720x640')
window.config(bg="white")

lbl = Label(window, text="Узнайте сколько спутников StarLink попадает в кадр КГО ГАИШ МГУ !", bg="white")
lbl.grid(row=0, columnspan=3, pady=20)

time_label = Label(window, text="Время начала съемки: (ГГГГ-ММ-ДД-ЧЧ-ММ-СС)", bg="white")
time_label.grid(column=0, row=1)
start = Entry(window, width=42)
start.insert(END, "2020-12-14-18-00-00")
start.grid(column=1, row=1)

exposition_label = Label(window, text="Выдержка: (в секундах)", bg="white")
exposition_label.grid(column=0, row=2)
exp = Entry(window, width=42)
exp.insert(END, "10")
exp.grid(column=1, row=2)

fov_label = Label(window, text="Поле зрения телескопа: (в минутах)", bg="white")
fov_label.grid(column=0, row=3)
fov = Entry(window, width=42)
fov.insert(END, "40")
fov.grid(column=1, row=3)

center_label = Label(window, text="Координаты центра изображение: (Геоцентрические)", bg="white")
center_label.grid(column=0, row=4)
center = Entry(window, width=42)
center.insert(END, "4741.54541529 -2257.71642333 4505.71410004")
center.grid(column=1, row=4)

cnt_label = Label(window, text="Посчитать спутники:", bg="white")
cnt_label.grid(column=0, row=6, pady=5)
cnt = Button(window, text="Count!", command=lambda: count(start, exp, center, fov))
cnt.grid(column=1, row=6, rowspan=3)

res_bar = Progressbar(window, orient=HORIZONTAL, length=200, mode="determinate")
res_bar.grid(column=0, row=7)
res_label = Label(window, text="Количество спутников:", bg="white")
res_label.grid(column=0, row=8)
result = Label(window, text="", bg="white")
result.config(font=("calibri", 30))
result.grid(column=0, row=9)

window.mainloop()
