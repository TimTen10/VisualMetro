import os
import tkinter as tk
from metro.metroline import Metroline
from metro.metronetwork import Metronetwork

def _init_test_line(name, color):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    tt_path = dir_path + f'/timetableparser/parsedtimetables/{name}'
    return Metroline(f'{name}', f'{color}', tt_path)

# width and height of the windows matters in this function
def _get_pixel_size_factor(zone):
    height = round((zone[1] - zone[0]), 6)
    width = round((zone[3] - zone[2]), 6)
    height = 1800 / height
    width = 1800 / width
    return width, height

# width and height of the windows matters in this function
def _get_zone_location(zone, location):
    width_fac, height_fac = _get_pixel_size_factor(zone)
    return 100 + (location[1] - zone[2]) * width_fac, 1900 - (location[0] - zone[0]) * height_fac

def _set_fitted_location(network):
    for metroline in network.lines:
        for station in metroline.line:
            station.location = list(_get_zone_location(network.zone, station.location))

def _draw_connections(canvas, network):
    for metroline in network.lines:
        for station in metroline.line:
            if station.next != None:
                canvas.create_line(station.location[0] + 10, station.location[1] + 10,
                                   station.next.location[0] + 10, station.next.location[1] + 10)

def _draw_stations(canvas, network):
    for metroline in network.lines:
        for station in metroline.line:
            canvas.create_oval(station.location[0], station.location[1],
                               station.location[0] + 20, station.location[1] + 20,
                               fill=metroline.color, width=2)
            canvas.create_text(station.location[0] + 10, station.location[1] - 10, font=('Purisa', 8), text=station.name) # angle=45, anchor=tk.W
            canvas.create_text(station.location[0] + 10, station.location[1] + 10, font=('Purisa', 8), text=metroline.name[0])

def _test():

    mita = _init_test_line('Mita', 'blue')
    asakusa = _init_test_line('Asakusa', 'pink')

    tkobj = tk.Tk()
    canvas = tk.Canvas(tkobj, width=1400, height=700)

    """Scrollbar Y"""
    canvas.config(scrollregion=[0, 0, 2000, 2000])

    hbar = tk.Scrollbar(tkobj)
    hbar.pack(side=tk.RIGHT, fill=tk.Y)
    hbar.config(command=canvas.yview)
    canvas.config(yscrollcommand=hbar.set)

    wbar = tk.Scrollbar(tkobj, orient=tk.HORIZONTAL)
    wbar.pack(side=tk.BOTTOM, fill=tk.X)
    wbar.config(command=canvas.xview)
    canvas.config(xscrollcommand=wbar.set)

    tkobj.title("VisualMetro")
    canvas.pack()

    test_network = Metronetwork('testing', [mita, asakusa])

    _set_fitted_location(test_network)

    _draw_connections(canvas, test_network)
    _draw_stations(canvas, test_network)

    tkobj.mainloop()

if __name__ == '__main__':
    _test()
