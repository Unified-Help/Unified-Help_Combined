import datetime, shelve

class User:

    def __init__(self, username, email, contact, gender, password, confirm_password):
        self.__user_id = ''
        self.__username = username
        self.__email = email
        self.__contact = contact
        self.__gender = gender
        self.__password = password
        self.__confirm_password = confirm_password
        self.__datetime = datetime.datetime.now()

    def get_user_id(self):
        return self.__user_id

    def get_username(self):
        return self.__username

    def get_email(self):
        return self.__email

    def get_contact(self):
        return self.__contact

    def get_gender(self):
        return self.__gender

    def get_password(self):
        return self.__password

    def get_confirm_password(self):
        return self.__confirm_password

    def get_account_type(self):
        return self.__account_type

    def get_date_time(self):
        return self.__datetime

    def set_user_id(self):
        with shelve.open('account','r') as db:
            if len(db['Users']) == 0:
                user_id = 0
            else:
                user_id = list(db['Users'].keys())[-1]

        user_id += 1
        self.__user_id = user_id

    def set_username(self, username):
        self.__username = username

    def set_email(self, email):
        self.__email = email

    def set_contact(self, contact):
        self.__contact = contact

    def set_gender(self, gender):
        self.__gender = gender

    def set_password(self, password):
        self.__password = password

    def set_confirm_password(self, confirm_password):
        self.__confirm_password = confirm_password

    def set_account_type(self):
        self.__account_type = 'Customer'

    def set_date_time(self, datetime):
        self.__datetime = datetime
        self.__datetime = self.__datetime.strftime("%d %b %Y, %X")

class Staff(User):
    def __init__(self, username, email, contact, gender, password, confirm_password):
        super().__init__(username, email, contact, gender, password, confirm_password)

    def get_account_type(self):
        return self.__account_type

    def set_account_type(self):
        self.__account_type = "Staff"
