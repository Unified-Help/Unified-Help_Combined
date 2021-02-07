import datetime

class Staff:
    count_id = 0

    def __init__(self, staff_username, staff_email, staff_gender, staff_password, staff_confirm_password):
        Staff.count_id += 1
        self.__staff_id = Staff.count_id
        self.__username = staff_username
        self.__email = staff_email
        self.__gender = staff_gender
        self.__password = staff_password
        self.__confirm_password = staff_confirm_password
        self.__account_status = "Staff"
        self.__datetime = datetime.datetime.now()

    def get_staff_id(self):
        return self.__staff_id

    def get_staff_username(self):
        return self.__username

    def get_email(self):
        return self.__email

    def get_gender(self):
        return self.__gender

    def get_staff_password(self):
        return self.__password

    def get_confirm_password(self):
        return self.__confirm_password

    def get_account_status(self):
        return self.__account_status

    def get_date_time(self):
        return self.__datetime

    def set_staff_id(self, staff_id):
        self.__staff_id = staff_id

    def set_staff_username(self, staff_username):
        self.__username = staff_username

    def set_email(self, staff_email):
        self.__email = staff_email

    def set_gender(self, staff_gender):
        self.__gender = staff_gender

    def set_staff_password(self, staff_password):
        self.__password = staff_password

    def set_confirm_password(self, staff_confirm_password):
        self.__confirm_password = staff_confirm_password

    def set_account_status(self, account_status):
        self.__account_status = account_status

    def set_date_time(self, datetime):
        self.__datetime = datetime
        self.__datetime = self.__datetime.strftime("%d %b %Y, %H:%M")
