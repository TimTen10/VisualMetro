import os
import tkinter as tk
from metro.metroline import Metroline

def _init_test_line():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    tt_path = dir_path + f'/timetableparser/parsedtimetables'
    return Metroline('Asakusa', 'red', tt_path)

def _get_pixel_size_factor(zone):
    height = round((zone[1] - zone[0]), 6)
    width = round((zone[3] - zone[2]), 6)
    height = 600 / height
    width = 1200 / width
    return width, height

def _get_zone_location(zone, location):
    width_fac, height_fac = _get_pixel_size_factor(zone)
    return 100 + (location[1] - zone[2]) * width_fac, 650 - (location[0] - zone[0]) * height_fac

def _set_fitted_location(metroline):
    for station in metroline.line:
        station.location = list(_get_zone_location(metroline.zone, station.location))

def _draw_connections(canvas, metroline):
    for station in metroline.line:
        if station.next != None:
            canvas.create_line(station.location[0] + 10, station.location[1] + 10,
                               station.next.location[0] + 10, station.next.location[1] + 10)

def _draw_stations(canvas, metroline):
    for station in metroline.line:
        canvas.create_oval(station.location[0], station.location[1],
                           station.location[0] + 20, station.location[1] + 20,
                           fill=metroline.color)
        canvas.create_text(station.location[0] + 10, station.location[1] - 10, text=station.name)

def main():

    asakusa = _init_test_line()
    print(asakusa.zone)

    tkobj = tk.Tk()
    canvas = tk.Canvas(tkobj, width=1400, height=700)
    tkobj.title("VisualMetro")
    canvas.pack()

    _set_fitted_location(asakusa)

    _draw_connections(canvas, asakusa)
    _draw_stations(canvas, asakusa)

    tkobj.mainloop()

if __name__ == '__main__':
    main()
