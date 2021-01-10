<<<<<<< Updated upstream
from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators


class ManualUploadForm(Form):
    data_field = RadioField("Select a data Field", [validators.DataRequired()],
=======
from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, IntegerField, validators
import datetime

year_choices = []
x = datetime.datetime.now()
y = 0
while True:
    value = str(x.year - y)
    choice = (value, value)
    if value == "2014":
        break
    else:
        year_choices.append(choice)
        y += 1

class ManualUploadForm(Form):
    data_field = SelectField("", [validators.DataRequired()],
>>>>>>> Stashed changes
                            choices=[("Campaign Costs: Online", "Campaign Costs: Online"),
                                     ("Campaign Costs: Offline", "Campaign Costs: Offline"),
                                     ("Inventory Storage Costs", "Inventory Storage Costs"),
                                     ("Charitable Programs: Supplies", "Charitable Programs: Supplies"),
                                     ("Charitable Programs: Manpower", "Charitable Programs: Manpower"),
                                     ("Charitable Programs: Venue Rental", "Charitable Programs: Venue Rental"),
                                     ("Fund-raising Expenses: Catering", "Fund-raising Expenses: Catering"),
                                     ("Fund Raising Expenses: Marketing", "Fund Raising Expenses: Marketing"),
                                     ("Fund-raising Expenses: Venue Rental", "Fund-raising Expenses: Venue Rental"),
                                     ("Administration Costs: Employee Salaries", "Administration Costs: Employee Salaries"),
                                     ("Administration Costs: Employee training", "Administration Costs: Employee training"),
                                     ("Administration Costs: Office Supplies", "Administration Costs: Office Supplies"),
                                     ("Administration Costs: Legal Fees", "Administration Costs: Legal Fees"),
                                     ("Utilities Costs: Water", "Utilities Costs: Water"),
                                     ("Utilities Costs: Electricity", "Utilities Costs: Electricity")],
                            default='')

<<<<<<< Updated upstream
    cardInfo_DateExpiry = SelectField("Month of Expiry*", [validators.DataRequired()],
=======
    month = SelectField("Month", [validators.DataRequired()],
>>>>>>> Stashed changes
                                      choices=[('01', 'January'), ('02', 'Feburary'), ('03', 'March'), ('04', 'April'),
                                               ('05', 'May'), ('06', 'June'), ('07', 'July'), ('08', 'August'),
                                               ('09', 'September'), ('10', 'October'), ('11', 'November'),
                                               ('12', 'December')])
<<<<<<< Updated upstream
    cardInfo_YearExpiry = SelectField("Year of Expiry*", [validators.DataRequired()],
                                      choices=[('21', '2021'), ('22', '2022'), ('23', '2023'), ('24', '2024'),
                                               ('25', '2025'), ('26', '2026'), ('27', '2027')])
=======
    
    global year_choices
    year = SelectField("Year", [validators.DataRequired()], choices= year_choices)

    data_value = IntegerField("", [validators.NumberRange(min=1, max=1000000), validators.DataRequired()])

    
>>>>>>> Stashed changes
