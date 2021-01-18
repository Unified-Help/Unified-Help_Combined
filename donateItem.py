from wtforms import Form, StringField, FloatField, IntegerField, RadioField, SelectField, \
    TextAreaField, validators
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.fields.html5 import DateField, TimeField, DecimalField


class donateItem(Form):
    donateToWho = SelectField('Donate to Who*', validators=[DataRequired(message="Pick who to donate to!")],
                              choices=[('', 'Select'), ('Under Privileged', 'Under Privileged'),
                                       ('Physically Handicapped', 'Physically Handicapped'),
                                       ('Natural Disaster Survivors', 'Natural Disaster Survivors'),
                                       ('Persons with Intellectual Disabilities',
                                        'Persons with Intellectual Disabilities'),
                                       ('Seniors', 'Seniors'), ('Special Needs', 'Special Needs')], default='')

    # If donor inputs Item Donation
    # Item Information
    itemType = SelectField('Item Type*', [validators.DataRequired()],
                           choices=[('Clothes', 'Clothes'), ('Furniture', 'Furniture'), ('Electronics', 'Electronics'),
                                    ('Books', 'Books')], default='C')
    itemName = StringField("Name of Item*",
                           [validators.Length(min=1, max=150), validators.DataRequired()])
    itemWeight = FloatField("Weight of Item*", [validators.NumberRange(min=0, max=150), validators.DataRequired()])
    itemHeight = FloatField("Height of Item*", [validators.NumberRange(min=0, max=150), validators.DataRequired()])
    itemLength = FloatField("Length of Item*", [validators.NumberRange(min=0, max=150), validators.DataRequired()])
    itemWidth = FloatField("Width of Item*", [validators.NumberRange(min=0, max=150), validators.DataRequired()])
    # itemImage = FileField('Picture of Item', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])

    # Collection Types and Information
    collectionDate = SelectField("Pick Collection Date*", [validators.DataRequired()],
                                 choices=[('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'), ('05', '05'),
                                          ('06', '06'), ('07', '07'), ('08', '08'), ('09', '09'), ('10', '10'),
                                          ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'),
                                          ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'),
                                          ('21', '21'), ('22', '22'), ('23', '23'), ('24', '24'), ('25', '25'),
                                          ('26', '26'), ('27', '27'), ('28', '28'), ('29', '29'), ('30', '30'),
                                          ('31', '31')])

    collectionMonth = SelectField("Pick Collection Month*", [validators.DataRequired()],
                                  choices=[('01', 'January'), ('02', 'Feburary'), ('03', 'March'), ('04', 'April'),
                                           ('05', 'May'), ('06', 'June'), ('07', 'July'), ('08', 'August'),
                                           ('09', 'September'), ('10', 'October'), ('11', 'November'),
                                           ('12', 'December')])

    collectionTime = StringField("Pick a Time*", [validators.Length(min=1, max=4),
                                                  validators.DataRequired()])
    collectionType = RadioField('Type of Collection*', choices=[('Drop Off', 'Drop Off'), ('We Pick Up', 'We Pick Up')],
                                default='Drop Off')

    # Pick Up Collection information
    pickupAddress1 = StringField("Address Line 1", [validators.Length(min=1, max=150), validators.Optional()])
    pickupAddress2 = StringField("Address Line 2", [validators.Length(min=1, max=150), validators.Optional()])
    pickupAddress3 = StringField("Address Line 3", [validators.Length(min=1, max=150), validators.Optional()])
    pickupPostalCode = StringField("Postal Code", [validators.Length(min=1, max=6), validators.Optional()])
