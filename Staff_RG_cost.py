import csv
import datetime


class Data:
    count_id = 0

    def __init__(self, year, month, data_field, value):
        Data.count_id += 1
        self.__data_id = Data.count_id
        self.__year = year
        self.__month = month
        self.__data_field = data_field
        self.__value = value

    # Accessor
    def get_data_id(self):
        return self.__data_id

    def get_data_field(self):
        return self.__data_field

    def get_year(self):
        return self.__year

    def get_month(self):
        return self.__month

    def get_value(self):
        return self.__value

    # Mutator Methods
    def set_data_id(self, data_id):
        self.__data_id = data_id

    def set_data_field(self, data_field):
        self.__data_field = data_field

    def set_year(self, year):
        self.__year = year

    def set_month(self, month):
        self.__month = month

    def set_value(self, value):
        self.__value = value


def read_csv():
    campaign_costs_dict = {}
    Inv_storage_costs_dict = {}
    UCE_costs_dict = {}
    UCW_costs_dict = {}
    admin_costs_dict = {}
    try:
        with open("costs.csv", "r") as data_file:
            # Converts each line from the csv file into a dictionary. For example, the first line, as a dictionary, will be,
            # {'Year': '2015', 'Month': 'JAN', 'Campaign Costs': '3992', 'Inventory Storage Costs': '1217', 'Utilities Costs: Electricity': '305', 'Utilities Cost: Water': '440', 'Administration Costs': '5782'}
            # Therefore, the key is the heading of each column and the value is the corresponding data value of that column and row
            data_reader = csv.DictReader(data_file)
            for line in data_reader:
                # Creates object for campaign cost value in the line with "Data" class.
                cc_data_object = Data(line["Year"], line["Month"], "Campaign Costs", line["Campaign Costs"])
                # Stores the object in the respective dictionary using the data_id of object as the key.
                campaign_costs_dict[cc_data_object.get_data_id()] = cc_data_object

                # Creates object for inventory storage cost value in the line with "Data" class.
                ISC_data_object = Data(line["Year"], line["Month"], "Inventory Storage Costs",
                                       line["Inventory Storage Costs"])
                # Stores the object in the respective dictionary using the data_id of object as the key.
                Inv_storage_costs_dict[ISC_data_object.get_data_id()] = ISC_data_object

                # Creates object for UCE cost value in the line with "Data" class.
                UCE_data_object = Data(line["Year"], line["Month"], "Utilities Costs: Electricity",
                                       line["Utilities Costs: Electricity"])
                # Stores the object in the respective dictionary using the data_id of object as the key.
                UCE_costs_dict[UCE_data_object.get_data_id()] = UCE_data_object

                # Creates object for UCW cost value in the line with "Data" class.
                UCW_data_object = Data(line["Year"], line["Month"], "Utilities Costs: Water",
                                       line["Utilities Cost: Water"])
                # Stores the object in the respective dictionary using the data_id of object as the key.
                UCW_costs_dict[UCW_data_object.get_data_id()] = UCW_data_object

                # Creates object for administration cost value in the line with "Data" class.
                AC_data_object = Data(line["Year"], line["Month"], "Administration Costs", line["Administration Costs"])
                # Stores the object in the respective dictionary using the data_id of object as the key.
                admin_costs_dict[AC_data_object.get_data_id()] = AC_data_object

    # Error exceptions
    except FileNotFoundError:
        print("File not Found!")

    except:
        print("Error in extracting data from file. "
              "Ensure that the headings and index of file uploaded matches the template file.")

    # Utilises the datetime module calls the now function which gets the current year,month,week,day and exact time.
    # This is later used to get the current year. It is needed to show data from different time frames.
    now = datetime.datetime.now()

    # ========== Retrieve ==========
    chart_data = []
    for key, value in campaign_costs_dict.items():
        cc = campaign_costs_dict[key].get_data_id()
        if now.year == int(value.get_year()):
            data = [value.get_month(), value.get_value()]
            chart_data.append(data)



read_csv()
