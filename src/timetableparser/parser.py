import os
import json
from bs4 import BeautifulSoup

def _remove_brackets(word):
    # Only works if the only other possiblity is a number with only one pair of brackets
    return word if word.isdigit() else word[1:-1]

def _parse_times(soup):
    # TODO: Change this function if platform (or other) information is needed
    departures = []
    # 'th ~ td .time' means: select all tags with "time" as class (.) that are
    # beneath a td tag which is a sibling (~) tag to a th tag
    for dt in soup.select('th ~ td .time'):
        #print(dt.find_parent('td').find_previous_sibling().string, dt.string)
        hour = str(dt.find_parent('td').find_previous_sibling().string)
        minutes = _remove_brackets(str(dt.string))
        departures.append(f'{hour}:{minutes}')
    return departures

def _parse_timetable(timetable):
    # parse the given timetable html file
    # save a timetable in json format with the most basic and needed information
    # example dictionary
    # timetable_station = {
    #     "name": "name",
    #     "prev": "name",
    #     "next": "name",
    #     "departures": [
    #         5:15,
    #         5:30,
    #         etc.
    #     ],
    #     "location": [
    #         {"breitengrad": 5.5},
    #         {"laengengrad": 78.0}
    #     ]
    # }
    with open(timetable, encoding="utf8") as tt:
        soup = BeautifulSoup(tt, "lxml")

    station_name = str(soup.find('h1', {'class': 'station-name'}).string)

    try:
        prev_station_name = str(soup.find('div', {'class': 'prev'}).p.a.string)[:-7]
    except AttributeError:
        prev_station_name = None

    # TODO: the [:-7] is sloppy, it is used to remove the line/station number
    try:
        next_station_name = str(soup.find('div', {'class': 'next'}).p.a.string)[:-7]
    except AttributeError:
        next_station_name = None

    departures = _parse_times(soup)

    parsed_tt = dict()
    parsed_tt['name'] = station_name
    parsed_tt['prev'] = prev_station_name
    parsed_tt['next'] = next_station_name
    parsed_tt['departures'] = departures
    parsed_tt['location'] = [None, None]

    return parsed_tt

def parse_timetables(folder_path):
    # IMPORTANT: there has to be a 'parsedtimetables' folder in the same parent
    # directory as the 'timetables' folder
    try:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.html'):
                    tt_dict = _parse_timetable(folder_path + f'/{file}')
                    with open(folder_path + f'/../parsedtimetables/{tt_dict["name"]}.json', 'w') as json_file:
                        json.dump(tt_dict, json_file)
    except:
        print('Unable to save the parsed timetables.'
            + ' Make sure a "parsedtimetables" folder exists in the same parent'
            + ' directory as the folder containing the timetables.')


def main():
    # For each timetable in the timetables folder,
    # create a json containing all necessary information.
    # This timetables folder has to be in the same directory as the parser.py file
    dir_path = os.path.dirname(os.path.realpath(__file__))
    parse_timetables(dir_path + '/timetables')

if __name__ == '__main__':
    main()
