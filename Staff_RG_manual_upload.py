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
                             choices=[("Campaign Costs: Online", "Campaign Costs: Online"),
                                      ("Campaign Costs: Offline", "Campaign Costs: Offline"),
                                      ("Inventory Storage Costs", "Inventory Storage Costs"),
                                      ("Charitable Programs: Supplies", "Charitable Programs: Supplies"),
                                      ("Charitable Programs: Manpower", "Charitable Programs: Manpower"),
                                      ("Charitable Programs: Venue Rental", "Charitable Programs: Venue Rental"),
                                      ("Fund-raising Expenses: Catering", "Fund-raising Expenses: Catering"),
                                      ("Fund Raising Expenses: Marketing", "Fund Raising Expenses: Marketing"),
                                      ("Fund-raising Expenses: Venue Rental", "Fund-raising Expenses: Venue Rental"),
                                      ("Administration Costs: Employee Salaries",
                                       "Administration Costs: Employee Salaries"),
                                      ("Administration Costs: Employee training",
                                       "Administration Costs: Employee training"),
                                      (
                                      "Administration Costs: Office Supplies", "Administration Costs: Office Supplies"),
                                      ("Administration Costs: Legal Fees", "Administration Costs: Legal Fees"),
                                      ("Utilities Costs: Water", "Utilities Costs: Water"),
                                      ("Utilities Costs: Electricity", "Utilities Costs: Electricity")],
                             default='')

    month = SelectField("Month", [validators.DataRequired()],
                        choices=[('JAN', 'January'), ('FEB', 'Feburary'), ('MAR', 'March'), ('APR', 'April'),
                                 ('MAY', 'May'), ('JUN', 'June'), ('JULY', 'July'), ('AUG', 'August'),
                                 ('SEP', 'September'), ('OCT', 'October'), ('NOV', 'November'),
                                 ('DEC', 'December')])

    global year_choices
    year = SelectField("Year", [validators.DataRequired()], choices=year_choices)

    data_value = IntegerField("", [validators.NumberRange(min=1, max=1000000), validators.DataRequired()])
