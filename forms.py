from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email


class NewShop(FlaskForm):
    store_name = StringField("Store Name (Neighborhood)", default="Just Another Coffee Shop Co. (Midtown)", validators=[DataRequired()])
    open = StringField("Opening Time e.g. 6AM", validators=[DataRequired()])
    close = StringField("Closing TIme e.g. 8PM", validators=[DataRequired()])
    coffee = SelectField("Coffee & Drink Rating (1-5)", choices=["☕", "☕" * 2, "☕"* 3, "☕"* 4, "☕"* 5], validators=[DataRequired()])
    wifi = SelectField("Location has Wifi?", choices=[ "✘","📶👍"], validators=[DataRequired()])
    seating = SelectField("Seating and Power Availablity (1-5)", choices=["✘", "⚡", "⚡" * 2, "⚡"* 3, "⚡"* 4, "⚡"* 5], validators=[DataRequired()])
    location_url = StringField("Address", default="123 Espresso St, City, ST, 12345", validators=[DataRequired()])
    posted_by = StringField("Added By", default="Your Name", validators=[DataRequired()])
    submit = SubmitField("Add Location")


class EditShop(FlaskForm):
    store_name = StringField("Store Name (Neighborhood)", default="Just Another Coffee Shop Co. (Midtown)", validators=[DataRequired()])
    open = StringField("Opening Time e.g. 6AM", validators=[DataRequired()])
    close = StringField("Closing TIme e.g. 8PM", validators=[DataRequired()])
    coffee = SelectField("Coffee & Drink Rating (1-5)", choices=["☕", "☕" * 2, "☕"* 3, "☕"* 4, "☕"* 5], validators=[DataRequired()])
    wifi = SelectField("Location has Wifi?", choices=[ "✘","📶👍"], validators=[DataRequired()])
    seating = SelectField("Seating and Power Availablity (1-5)", choices=["✘", "⚡", "⚡" * 2, "⚡"* 3, "⚡"* 4, "⚡"* 5], validators=[DataRequired()])
    location_url = StringField("Address", default="123 Espresso St, City, ST, 12345", validators=[DataRequired()])
    posted_by = StringField("Added By", default="Your Name", validators=[DataRequired()])
    update = SubmitField("Save Changes")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In!")


class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register!")
