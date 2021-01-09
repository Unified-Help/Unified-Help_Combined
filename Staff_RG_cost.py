import csv
import datetime


class Data:
    count_id = 0

    def __init__(self, date, data_field, value):
        Data.count_id += 1
        self.__data_id = Data.count_id
        self.__data_field = data_field
        self.__value = value
        self.__date = datetime.datetime.strptime(str(date), '%d/%m/%Y').strftime('%b/%d/%Y')

    # Accessor
    def get_data_id(self):
        return self.__data_id

    def get_data_field(self):
        return self.__data_field

    def get_date(self):
        return self.__date

    def get_value(self):
        return self.__value

    # Mutator Methods
    def set_data_id(self, data_id):
        self.__data_id = data_id

    def set_data_field(self, data_field):
        self.__data_field = data_field

    def set_date(self, date):
        self.__date = date

    def set_value(self, value):
        self.__value = value
