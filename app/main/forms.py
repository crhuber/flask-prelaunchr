from flask_wtf import Form
from wtforms import ValidationError, StringField, SubmitField, DateTimeField, IntegerField, TextAreaField, RadioField, SelectField, DateField,BooleanField
from wtforms.validators import Required, URL, AnyOf, DataRequired, Optional, Length, Email, Regexp, EqualTo
from datetime import datetime
from ..models import User

class ContestForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    submit = SubmitField('Step Inside')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('That email address has already signed up')
