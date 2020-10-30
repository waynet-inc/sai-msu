# Скачать актуальные эфемериды спутников Starlink
# и определить сколько спутников попадет в кадр снятый из КГО ГАИШ МГУ,
# как функцию времени начала и конца экспозиции,
# экваториальных координат центра изображения и
# поле зрения телескопа.

from skyfield.api import EarthSatellite, Topos, load
import requests
from datetime import timedelta

def satnum(start_time, end_time, eq_cords, field_of_view):
    with open("starlink.txt") as file_input:
        sat_counter = 0

        for line in file_input:
            name = line
            line1 = next(file_input)
            line2 = next(file_input)
            satellite = EarthSatellite(line1, line2, name)

            difference = satellite - eq_cords
            start = start_time

            while start != end_time:
                topocentric = difference.at(start)
                altaz = topocentric.altaz()
                if altaz[0].degrees >= (90 - field_of_view/2):
                    sat_counter += 1
                    break
                start = ts.utc(start.utc_datetime() + timedelta(minutes=1))

    return sat_counter


url = "https://celestrak.com/NORAD/elements/starlink.txt"
download = requests.get(url)
with open("starlink.txt", "wb") as f:
    f.write(download.content)

ts = load.timescale()

start_time = ts.utc(2020, 10, 29, 18, 0, 0)
end_time = ts.utc(2020, 10, 29, 19, 0, 0)
eq_cords = Topos("43.4410 N", "42.4003 E", elevation_m=2112)
field_of_view = 50

num = satnum(start_time, end_time, eq_cords, field_of_view)
print("The number of satellites: ", num)
