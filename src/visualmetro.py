import os
import tkinter as tk
from metro import metroline, metronetwork, station

def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    tt_path = dir_path + f'/../timetableparser/parsedtimetables'
    asakusa = Metroline('Asakusa', 'red', tt_path)
    print(asakusa.zone)

if __name__ == '__main__':
    main()
