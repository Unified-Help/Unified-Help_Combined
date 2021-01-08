from wtforms import Form, StringField, FloatField, IntegerField, RadioField, SelectField, TextAreaField, validators
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.fields.html5 import DateField, TimeField, DecimalField


class donateMoney(Form):
    donateToWho = SelectField('Donate to Who*', [validators.DataRequired()],
                              choices=[('', 'Select'), ('Under Privileged', 'Under Privileged'),
                                       ('Physically Handicapped', 'Physically Handicapped'),
                                       ('Natural Disaster Survivors', 'Natural Disaster Survivors'),
                                       ('Persons with Intellectual Disabilities', 'Persons with Intellectual Disabilities'),
                                       ('Seniors', 'Seniors'), ('Special Needs', 'Special Needs')], default='')

    # If donor inputs Monetary Donation
    # Money Information
    moneyAmount = IntegerField("Donation Amount*",
                               [validators.NumberRange(min=1, max=1000000), validators.DataRequired()])
    cardInfo_Name = StringField('Full Name*', [validators.Length(min=1, max=150), validators.DataRequired()])
    cardInfo_Number = StringField('Card Number*', [validators.Length(min=19, max=19), validators.DataRequired()])
    cardInfo_CVV = StringField('CVV*', [validators.Length(min=3, max=3), validators.DataRequired()])

    cardInfo_DateExpiry = SelectField("Month of Expiry*", [validators.DataRequired()],
                                      choices=[('01', 'January'), ('02', 'Feburary'), ('03', 'March'), ('04', 'April'),
                                               ('05', 'May'), ('06', 'June'), ('07', 'July'), ('08', 'August'),
                                               ('09', 'September'), ('10', 'October'), ('11', 'November'),
                                               ('12', 'December')])
    cardInfo_YearExpiry = SelectField("Year of Expiry*", [validators.DataRequired()],
                                      choices=[('21', '2021'), ('22', '2022'), ('23', '2023'), ('24', '2024'),
                                               ('25', '2025'), ('26', '2026'), ('27', '2027')])
