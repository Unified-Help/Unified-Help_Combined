class History:

    def __init__(self, field, month, year, old_value, new_value, now_date, now_time, user):
        self.__change_id = ""
        self.__field = field
        self.__month = month
        self.__year = year
        self.__old_value = old_value
        self.__new_value = new_value
        self.__now_date = now_date
        self.__now_time = now_time
        self.__user = user

    # Accessor Methods
    def get_change_id(self):
        return self.__change_id

    def get_field(self):
        return self.__field

    def get_month(self):
         return self.__month

    def get_year(self):
        return self.__year

    def get_old_value(self):
        return self.__old_value

    def get_new_value(self):
        return self.__new_value

    def get_now_date(self):
        return self.__now_date

    def get_now_time(self):
        return self.__now_time

    def get_user(self):
        return self.__user

    # Mutator Methods
    def set_change_id(self, id):
        self.__change_id = id

    def set_field(self, field):
        self.__field = field

    def set_month(self, month):
        self.__month = month

    def set_year(self, year):
        self.__year = year

    def set_old_value(self, old_value):
        self.__old_value = old_value

    def set_new_value(self, new_value):
        self.__new_value = new_value

    def set_now_date(self, now_date):
        self.__now_date = now_date

    def set_now_time(self, now_time):
        self.__now_time = now_time

    def set_user(self, user):
        self.__user = user
