"""Count the number of satellites in the frame of KMO SAI telescope

Module counts number of satellites
in the frame of Sternberg Astronomical Institute telescope
using Skyfield api.

The main function takes as arguments the start time of the photo,
the exposure time, celestial coordinates, and the telescope field of view.

Function returns an integer - number of satellites in the frame of KMO SAI telescope.
"""


from skyfield.api import load
from skyfield.units import Angle
from datetime import timedelta
import math as m
from cachetools import cached, TTLCache

__all__ = ('satnum',)


@cached(cache=TTLCache(maxsize=1024, ttl=86400))
def get_sat(url):
    return load.tle_file(url)


def satnum(start_time, exposition, eq_cords, field_of_view):
    """Counts number of satellites

    Arguments
    ---------
    :param start_time: list of ints (full date)
    :param exposition: int (in milliseconds)
    :param eq_cords: list of floats (right ascension, declination)
    :param field_of_view: float (in minutes)

    Returns
    -------
    :return: int


    Examples
    --------
    >>> import satnum
    >>> start_time = [2020, 12, 14, 18, 00, 00]
    >>> exposition = 1500
    >>> eq_cords = [45.0, 45.0]
    >>> field_of_view = 600
    >>> satnum.satnum(start_time, exposition, eq_cords, field_of_view)
    1
    """
    if not isinstance(start_time, list):
        raise TypeError("incorrect start time")
    if not all(isinstance(x, (int, float)) for x in start_time):
        raise ValueError("incorrect start time")
    if not isinstance(exposition, int):
        raise ValueError("incorrect exposition")
    if not isinstance(eq_cords, list):
        raise TypeError("incorrect coordinates")
    if not all(isinstance(x, (int, float)) for x in eq_cords):
        raise ValueError("incorrect start time")
    if not isinstance(field_of_view, (int, float)) or field_of_view < 0:
        raise ValueError("incorrect field of view")

    url = "https://celestrak.com/NORAD/elements/starlink.txt"
    satellites = get_sat(url)

    sat_counter = 0
    ts = load.timescale()
    start_time = ts.utc(*start_time)
    eq_cords = [Angle(degrees=eq_cords[0], preference="hours"), Angle(degrees=eq_cords[1])]
    fov_h = Angle(degrees=field_of_view/60, preference="hours")
    fov_d = Angle(degrees=field_of_view/60)
    cos0 = m.cos(m.radians(eq_cords[1].degrees))

    for satellite in satellites:
        for n in range(exposition):
            time = ts.utc(start_time.utc_datetime() + timedelta(seconds=n/1000))
            ra, dec, dist = satellite.at(time).radec()
            cos1 = m.cos(m.radians(dec.degrees))

            w = 0.83
            ws = w*3600

            if abs(eq_cords[0].hours * cos0 - ra.hours * cos1) > (exposition/1000)*ws or abs(eq_cords[1].degrees - dec.degrees) > (exposition/1000)*w:
                break
            if abs(eq_cords[0].hours * cos0 - ra.hours * cos1) <= fov_h.hours/2 and abs(eq_cords[1].degrees - dec.degrees) <= fov_d.degrees/2:
                sat_counter += 1
                break

    return sat_counter


if __name__ == '__main__':
    print("open as executable")
