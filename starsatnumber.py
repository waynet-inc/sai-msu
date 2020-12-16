# Скачать актуальные эфемериды спутников StarLink
# и определить сколько спутников попадет в кадр снятый из КГО ГАИШ МГУ,
# как функцию времени начала и конца экспозиции,
# экваториальных координат центра изображения и
# поле зрения телескопа.

from skyfield.api import EarthSatellite, Topos, load
from datetime import timedelta
from tkinter.ttk import *
from tkinter import *
import requests


def update():
    progress['value'] = 25
    window.update_idletasks()

    url = "https://celestrak.com/NORAD/elements/starlink.txt"
    download = requests.get(url)

    progress['value'] = 50
    window.update_idletasks()

    with open("starlink.txt", "wb") as f:
        f.write(download.content)

    progress['value'] = 100
    window.update_idletasks()


def satnum(start_time, exposition, eq_cords, field_of_view):
    date = start_time.get().split('-')
    date = list(map(int, date))
    start_time = ts.utc(*date)
    exposition = int(exposition.get())
    field_of_view = int(field_of_view.get())

    with open("starlink.txt") as file_input:
        sat_counter = 0
        res_bar['value'] = 0

        for line in file_input:
            name = line
            line1 = next(file_input)
            line2 = next(file_input)
            satellite = EarthSatellite(line1, line2, name)

            difference = satellite - eq_cords

            for n in range(exposition):
                time = ts.utc(start_time.utc_datetime() + timedelta(minutes=n))
                topocentric = difference.at(time)
                altaz = topocentric.altaz()
                if altaz[0].degrees >= (90 - field_of_view/2):
                    sat_counter += 1
                    break

            res_bar['value'] += 0.1105
            window.update_idletasks()

    result.config(text=sat_counter)


ts = load.timescale()
eq_cords = Topos("43.4410 N", "42.4003 E", elevation_m=2112)

window = Tk()
window.title("Satellites Number")
window.geometry('520x640')
window.config(bg="white")

lbl = Label(window, text="Узнайте сколько спутников StarLink попадает в кадр КГО ГАИШ МГУ !", bg="white")
lbl.grid(row=0, columnspan=3, pady=20)

time_label = Label(window, text="Время начала съемки: (ГГГГ-ММ-ДД-ЧЧ-ММ-СС)", bg="white")
time_label.grid(column=0, row=1)
start = Entry(window, width=19)
start.insert(END, "2020-12-14-18-00-00")
start.grid(column=1, row=1)

exposition_label = Label(window, text="Выдержка: (в минутах)", bg="white")
exposition_label.grid(column=0, row=2)
exp = Entry(window, width=19)
exp.insert(END, "10")
exp.grid(column=1, row=2)

fov_label = Label(window, text="Поле зрения телескопа: (в градусах)", bg="white")
fov_label.grid(column=0, row=3)
fov = Entry(window, width=19)
fov.insert(END, "45")
fov.grid(column=1, row=3)

upd_label = Label(window, text="Обновление эфемерид:", bg="white")
upd_label.grid(column=0, row=4, pady=5)
upd = Button(window, text="Update!", command=update)
upd.grid(column=1, row=4, rowspan=3)

progress = Progressbar(window, orient=HORIZONTAL, length=200, mode="determinate")
progress.grid(column=0, row=5)

cnt_label = Label(window, text="Посчитать спутники:", bg="white")
cnt_label.grid(column=0, row=6, pady=5)
cnt = Button(window, text="Count!", command=lambda: satnum(start, exp, eq_cords, fov))
cnt.grid(column=1, row=6, rowspan=3)

res_bar = Progressbar(window, orient=HORIZONTAL, length=200, mode="determinate")
res_bar.grid(column=0, row=7)
res_label = Label(window, text="Количество спутников:", bg="white")
res_label.grid(column=0, row=8)
result = Label(window, text="", bg="white")
result.config(font=("calibri", 30))
result.grid(column=0, row=9)

window.mainloop()
