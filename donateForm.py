from wtforms import Form, StringField, FloatField, IntegerField, RadioField, SelectField, TextAreaField, validators
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.fields.html5 import DateField, TimeField, DecimalField


class donationForm(Form):
    donateToWho = SelectField('Donate to Who*', [validators.DataRequired()],
                              choices=[('', 'Select'), ('Under Privileged', 'Under Privileged'),
                                       ('Physically Handicapped', 'Physically Handicapped'),
                                       ('Natural Disaster Survivors', 'Natural Disaster Survivors'),
                                       ('Special Needs', 'Special Needs')], default='')
    donationType = RadioField('Type of Donation*', choices=[('Monetary Donation', 'Monetary Donation'),
                                                            ('Item Donation', 'Item Donation')], default='M')

# Delete if not using pls
