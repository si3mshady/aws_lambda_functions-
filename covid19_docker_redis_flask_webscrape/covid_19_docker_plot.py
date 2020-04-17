from collections import OrderedDict
import gmplot
import xlrd
import redis 
import re


class ProcessCSV:
    def __init__(self):
        self._filename = 'uscities.xlsx'
        self._workbook = self.open_xlsx()

    def open_xlsx(self) -> xlrd:
        return xlrd.open_workbook(self._filename)

    def get_sheets(self) -> xlrd:
        return self._workbook.sheets()

    def get_cities_states_lats_longs(self) -> tuple:
        #preserve list order dont sort yet
        sheet = self.get_sheets()[0]
        cities =  sheet.col_values(colx=0)[1:]
        states =  sheet.col_values(colx=3)[1:]       
        latitudes = sheet.col_values(colx=8)[1:] #N/S
        longitudes = sheet.col_values(colx=9)[1:] #E/W
        zip_code = sheet.col_values(colx=17)[1:]
        return (cities,states,latitudes,longitudes,zip_code)

    def map_cites_states_lats_longs(self) -> dict:
        container = OrderedDict()
        cities,states,lats,longs, zip_code = self.get_cities_states_lats_longs()
        for i,_ in enumerate(cities):
            container[cities[i] +','+ states[i]] = {'City':cities[i],\
                'State':states[i],'Latitude':lats[i], \
                    'Longitude':longs[i],'Zipcode':zip_code[i]}
        return container

    


    


    

        




#https://xlrd.readthedocs.io/en/latest/api.html