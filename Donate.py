import shelve


# Monetary Donations
class DonateMoney:
    # donatemoneyid_counter = 0

    def __init__(self, donate_who, money_amount, cardInfo_Name, cardInfo_Number, cardInfo_CVV, cardInfo_DateExpiry,
                 cardInfo_YearExpiry):
        # Money Donation ID
        # DonateMoney.donatemoneyid_counter += 1
        # self.__moneyID = "M" + str(DonateMoney.donatemoneyid_counter)
        self.__moneyID = 0

        # money donations
        self.__donate_type = "Monetary Donation"
        self.__donate_who = donate_who
        self.__money_amount = money_amount
        self.__cardInfo_Name = cardInfo_Name
        self.__cardInfo_Number = cardInfo_Number
        self.__cardInfo_CVV = cardInfo_CVV
        self.__cardInfo_DateExpiry = cardInfo_DateExpiry
        self.__cardInfo_YearExpiry = cardInfo_YearExpiry

        # Donation Status
        self.__status = ""

    # Accessors
    def get_moneyID(self):
        return self.__moneyID

    def get_donate_type(self):
        return self.__donate_type

    def get_donate_who(self):
        return self.__donate_who

    def get_money_amount(self):
        return self.__money_amount

    def get_cardInfo_Name(self):
        return self.__cardInfo_Name

    def get_cardInfo_Number(self):
        return self.__cardInfo_Number

    def get_cardInfo_CVV(self):
        return self.__cardInfo_CVV

    def get_cardInfo_DateExpiry(self):
        return self.__cardInfo_DateExpiry

    def get_cardInfo_YearExpiry(self):
        return self.__cardInfo_YearExpiry

    def get_status(self):
        return self.__status

    # Mutators
    def set_moneyID(self):
        try:
            with shelve.open('donorChoices', 'r') as db:
                if len(db['Money']) == 0:
                    donatemoneyid_counter = 0
                else:
                    donatemoneyid_counter = int(list(db['Money'].keys())[-1].split('M')[-1])
        except:
            donatemoneyid_counter = 0

        donatemoneyid_counter += 1
        self.__moneyID = "M" + str(donatemoneyid_counter)
        # self.__moneyID = moneyID

    def set_donate_type(self, donate_type):
        self.__donate_type = donate_type

    def set_donate_who(self, donate_who):
        self.__donate_who = donate_who

    def set_money_amount(self, money_amount):
        self.__money_amount = money_amount

    def set_cardInfo_Name(self, cardInfo_Name):
        self.__cardInfo_Name = cardInfo_Name

    def set_cardInfo_Number(self, cardInfo_Number):
        self.__cardInfo_Number = cardInfo_Number

    def set_cardInfo_CVV(self, cardInfo_CVV):
        self.__cardInfo_CVV = cardInfo_CVV

    def set_cardInfo_DateExpiry(self, cardInfo_DateExpiry):
        self.__cardInfo_DateExpiry = cardInfo_DateExpiry

    def set_cardInfo_YearExpiry(self, cardInfo_YearExpiry):
        self.__cardInfo_YearExpiry = cardInfo_YearExpiry

    def set_status(self, status):
        self.__status = status


# Item Donations
class DonateItem:
    # donateitemID_counter = 0

    def __init__(self, donate_who, item_type, item_name, item_weight, item_height, item_length, item_width
                 , collection_type, date, month, time, address1, address2, address3, postal_code):
        # Item Donation IDs
        self.__itemID = 0
        # DonateItem.donateitemID_counter += 1
        # self.__itemID = "I" + str(DonateItem.donateitemID_counter)

        # Item Details
        self.__donate_type = "Item Donation"
        self.__donate_who = donate_who
        self.__item_type = item_type
        self.__item_name = item_name
        self.__item_weight = item_weight
        self.__item_height = item_height
        self.__item_length = item_length
        self.__item_width = item_width

        # Collection Details
        self.__collection_type = collection_type
        self.__date = date
        self.__month = month
        self.__time = time

        # Collection PickUp Details
        self.__address1 = address1
        self.__address2 = address2
        self.__address3 = address3
        self.__postal_code = postal_code

        # Donation Status
        self.__status = ""

    # Accessors
    def get_itemID(self):
        return self.__itemID

    def get_donate_type(self):
        return self.__donate_type

    def get_donate_who(self):
        return self.__donate_who

    def get_item_type(self):
        return self.__item_type

    def get_item_name(self):
        return self.__item_name

    def get_item_weight(self):
        return self.__item_weight

    def get_item_length(self):
        return self.__item_length

    def get_item_width(self):
        return self.__item_width

    def get_item_height(self):
        return self.__item_height

    def get_collection_type(self):
        return self.__collection_type

    def get_date(self):
        return self.__date

    def get_month(self):
        return self.__month

    def get_time(self):
        return self.__time

    def get_address1(self):
        return self.__address1

    def get_address2(self):
        return self.__address2

    def get_address3(self):
        return self.__address3

    def get_postal_code(self):
        return self.__postal_code

    def get_status(self):
        return self.__status

    # Mutators
    def set_itemID(self):
        try:
            with shelve.open('donorChoices', 'r') as db:
                if len(db['Items']) == 0:
                    donateitemid_counter = 0
                else:
                    donateitemid_counter = int(list(db['Items'].keys())[-1].split('I')[-1])
        except:
            donateitemid_counter = 0

        donateitemid_counter += 1
        self.__itemID = "I" + str(donateitemid_counter)
        # self.__itemID = itemID

    def set_donate_type(self, donate_type):
        self.__donate_type = donate_type

    def set_donate_who(self, donate_who):
        self.__donate_who = donate_who

    def set_item_type(self, item_type):
        self.__item_type = item_type

    def set_item_name(self, item_name):
        self.__item_name = item_name

    def set_item_weight(self, item_weight):
        self.__item_weight = item_weight

    def set_item_length(self, item_length):
        self.__item_length = item_length

    def set_item_width(self, item_width):
        self.__item_width = item_width

    def set_item_height(self, item_height):
        self.__item_height = item_height

    def set_collection_type(self, collection_type):
        self.__collection_type = collection_type

    def set_date(self, date):
        self.__date = date

    def set_month(self, month):
        self.__month = month

    def set_time(self, time):
        self.__time = time

    def set_address1(self, address1):
        self.__address1 = address1

    def set_address2(self, address2):
        self.__address2 = address2

    def set_address3(self, address3):
        self.__address3 = address3

    def set_postal_code(self, postal_code):
        self.__postal_code = postal_code

    def set_status(self, status):
        self.__status = status
