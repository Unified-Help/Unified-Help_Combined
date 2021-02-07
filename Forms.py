from wtforms import Form, StringField, SelectField, validators, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf import FlaskForm

class CreateUserForm(Form):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    contact = StringField('Phone Number', validators=[DataRequired(), Length(min=8, max=8)])
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

class CreateStaffForm(Form):
    staff_username = StringField('Username', validators=[DataRequired(), Length(min=2, max=25)])
    staff_email = StringField('Email', validators=[DataRequired(), Email()])
    staff_gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    staff_password = PasswordField('Password', validators=[DataRequired()])
    staff_confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('staff_password')])

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
