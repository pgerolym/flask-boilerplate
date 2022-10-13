from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length

# Set your classes here.


class RegisterForm(Form):
    name = StringField(
        'Όνομα Χρήστη', validators=[DataRequired(), Length(min=6, max=25)]
    )
    email = StringField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
    password = PasswordField(
        'Κωδικός Χρήστη', validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        'Επανάληψη Κωδικού Χρήστη',
        [DataRequired(),
        EqualTo('password', message='Οι κωδικοί πρέπει να ταυτίζονται!')]
    )


class LoginForm(Form):
    email = StringField('Email Χρήστη', [DataRequired()])
    password = PasswordField('Κωδικός Χρήστη', [DataRequired()])


class ForgotForm(Form):
    email = StringField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
