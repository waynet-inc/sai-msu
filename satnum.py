"""Count the number of satellites in the frame of KMO SAI telescope

Module counts number of satellites
in the frame of Sternberg Astronomical Institute telescope
using Skyfield api.

The main function takes as arguments the start time of the photo,
the exposure time, geocentric coordinates, and the telescope field of view.

Function returns an integer - number of satellites in the frame of KMO SAI telescope.
"""

import skyfield.timelib
from skyfield.api import Topos, load
from datetime import timedelta


def satnum(start_time, exposition, eq_cords, field_of_view):
    """Counts number of satellites

    Arguments
    ---------
    :param start_time: skyfield.timelib.Time object
    :param exposition: int
    :param eq_cords: list of floats
    :param field_of_view: int

    Returns
    -------
    :return: int


    Examples
    --------
    import satnum
    start_time = [2020, 12, 14, 18, 00, 00]
    exposition = 15
    eq_cords = [4741.1, -2257.7, 4505.7]
    field_of_view = 45
    satnum.satnum(start_time, exposition, eq_cords, field_of_view)
    0
    """

    assert isinstance(start_time, skyfield.timelib.Time), "incorrect start time"
    assert isinstance(exposition, int), "incorrect exposition"
    assert isinstance(eq_cords, list), "incorrect coordinates"
    assert isinstance(field_of_view, int), "incorrect field of view"

    url = "https://celestrak.com/NORAD/elements/starlink.txt"
    satellites = load.tle_file(url)
    sat_counter = 0
    ts = load.timescale()
    eq_cords = Topos(*eq_cords)

    for satellite in satellites:

        difference = satellite - eq_cords

        for n in range(exposition):
            time = ts.utc(start_time.utc_datetime() + timedelta(seconds=n))
            topocentric = difference.at(time)
            altaz = topocentric.altaz()
            if altaz[0].degrees >= 90 - (field_of_view/2)/60:
                sat_counter += 1
                break

    return sat_counter


if __name__ == '__main__':
    print("open as executable")
