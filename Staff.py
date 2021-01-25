import datetime

class Staff:
    countID = 0

    def __init__(self, username, email, gender, password, confirm_password):
        Staff.countID += 1
        self.__staff_id = Staff.countID
        self.__username = username
        self.__email = email
        self.__gender = gender
        self.__password = password
        self.__confirm_password = confirm_password
        self.__datetime = datetime.datetime.now()

    def get_staff_id(self):
        return self.__staff_id

    def get_username(self):
        return self.__username

    def get_email(self):
        return self.__email

    def get_gender(self):
        return self.__gender

    def get_password(self):
        return self.__password

    def get_confirm_password(self):
        return self.__confirm_password

    def get_date_time(self):
        return self.__datetime

    def set_staff_id(self, staff_id):
        self.__staff_id = staff_id

    def set_username(self, username):
        self.__username = username

    def set_email(self, email):
        self.__email = email

    def set_gender(self, gender):
        self.__gender = gender

    def set_password(self, password):
        self.__password = password

    def set_confirm_password(self, confirm_password):
        self.__confirm_password = confirm_password

    def set_date_time(self, datetime):
        self.__datetime = datetime
        self.__datetime = self.__datetime.strftime("%d %b %Y, %H:%M")
