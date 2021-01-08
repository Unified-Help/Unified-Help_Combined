from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators


class ManualUploadForm(Form):
    data_fields = RadioField('Data Field', choices=[('OD', 'Offline Donations'), ('SC', 'Storage Costs'),
                                                   ('ADVC', 'Advertising Costs'), ('ADMC', "Administration Costs"),
                                                   ('UCE','Utilities Cost: Electricity'), ('UCW', 'Utilities Cost: Water')],
                            default='')
    data_value = StringField('Input Data', [validators.Length(min=1, max=150), validators.DataRequired()])
