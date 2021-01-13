class Data:
    count_id = 0

    def __init__(self, month, year):
        Data.count_id += 1
        self.__data_id = Data.count_id
        self.__month = month
        self.__year = year

    # Accessor Methods
    def get_month(self):
        return self.__month

    def get_year(self):
        return self.__year

    def get_data_id(self):
        return self.__data_id

    # Mutator Methods
    def set_month(self, month):
        self.__month = month

    def set_year(self, year):
        self.__year = year

    def set_data_id(self, data_id):
        self.__data_id = data_id


class CampaignCosts(Data):
    def __init__(self, month, year, online_costs, offline_costs):
        super().__init__(month, year)
        self.__online_costs = online_costs
        self.__offline_costs = offline_costs

    # Accessor Methods
    def get_online_costs(self):
        return self.__online_costs

    def get_offline_costs(self):
        return self.__offline_costs

    def get_total(self):
        total = self.__offline_costs + self.__online_costs
        return total

    # Mutator Methods
    def set_online_costs(self, online_costs):
        self.__online_costs = online_costs

    def set_offline_costs(self, offline_costs):
        self.__offline_costs = offline_costs


class ISC(Data):
    def __init__(self, month, year, isc):
        super().__init__(month, year)
        self.__isc = isc

    # Accessor Methods
    def get_isc(self):
        return self.__isc

    # Mutator Methods
    def set_isc(self, isc):
        self.__isc = isc


class CapCosts(Data):
    def __init__(self, month, year, supplies, manpower, vr):
        super().__init__(month, year)
        self.__supplies = supplies
        self.__manpower = manpower
        self.__vr = vr

    # Accessor Methods
    def get_supplies(self):
        return self.__supplies

    def get_manpower(self):
        return self.__manpower

    def get_vr(self):
        return self.__vr

    def get_total(self):
        total = self.__supplies + self.__manpower + self.__vr
        return total

    # Mutator Methods
    def set_supplies(self, supplies):
        self.__supplies = supplies

    def set_manpower(self, manpower):
        self.__manpower = manpower

    def set_vr(self, vr):
        self.__vr = vr


class FreCosts(Data):
    def __init__(self, year, month, catering, vr, marketing):
        super().__init__(year, month)
        self.__catering = catering
        self.__vr = vr
        self.__marketing = marketing

    # Accessor Methods
    def get_catering(self):
        return self.__catering

    def get_vr(self):
        return self.__vr

    def get_marketing(self):
        return self.__marketing

    def get_total(self):
        total = self.__catering + self.__vr + self.__marketing
        return total

    # Mutator Methods
    def set_catering(self, catering):
        self.__catering = catering

    def set_vr(self, vr):
        self.__vr = vr

    def set_marketing(self, marketing):
        self.__marketing = marketing


class AdminCosts(Data):
    def __init__(self, year, month, emp_salary, emp_training, office_supplies, legal_fees):
        super().__init__(year, month)
        self.__emp_salary = emp_salary
        self.__emp_training = emp_training
        self.__office_supplies = office_supplies
        self.__legal_fees = legal_fees

    # Accessor Methods
    def get_emp_salary(self):
        return self.__emp_salary

    def get_emp_training(self):
        return self.__emp_training

    def get_office_supplies(self):
        return self.__office_supplies

    def get_legal_fees(self):
        return self.__legal_fees

    def get_total(self):
        total = self.__emp_salary + self.__emp_training + self.__office_supplies + self.__legal_fees
        return total

    # Mutator Methods
    def set_emp_salary(self, emp_salary):
        self.__emp_salary = emp_salary

    def set_emp_training(self, emp_training):
        self.__emp_training = emp_training

    def set_office_supplies(self, office_supplies):
        self.__office_supplies = office_supplies

    def set_legal_fees(self, legal_fees):
        self.__legal_fees = legal_fees


class UtilitiesCosts(Data):
    def __init__(self, year, month, water, electricity):
        super().__init__(year, month)
        self.__water = water
        self.__electricity = electricity

    # Accessor Methods
    def get_water(self):
        return self.__water

    def get_electricity(self):
        return self.__electricity

    def get_total(self):
        total = self.__water + self.__electricity
        return total

    # Mutator Methods
    def set_water(self, water):
        self.__water = water

    def set_electricity(self, electricity):
        self.__electricity = electricity
