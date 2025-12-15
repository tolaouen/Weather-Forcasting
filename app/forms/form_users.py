import re
from wtforms import BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from flask_wtf import FlaskForm

from app.models.users import User
from app.database import get_db
from sqlalchemy.orm import Session

# Check for strong password validation

def strong_password(form, field):
    """"

    Require at least 8 characters, one uppercase letter, one lowercase letter, one number, and one special character.
    
    """

    if len(field.data) < 8:
        raise ValidationError("Password must be at least 8 characters long.")

    if not re.search(r'[A-Z]', field.data):
        raise ValidationError("Password must contain at least one uppercase letter.")

    if not re.search(r'[a-z]', field.data):
        raise ValidationError("Password must contain at least one lowercase letter.")

    if not re.search(r'[0-9]', field.data):
        raise ValidationError("Password must contain at least one number.")

    if not re.search(r'[!@#$%^&*]', field.data):
        raise ValidationError("Password must contain at least one special character.")
    
#  User Creation Form data validation

class CreateUserForm(FlaskForm):

    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=20)],
        render_kw={"placeholder": "Enter your username"},
    )

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Enter your email"},
    )

    full_name = StringField(
        "Full Name",
        validators=[Length(max=50)],
        render_kw={"placeholder": "Enter your full name"},
    )

    is_active = BooleanField("Is Active", default=True)

    passwod = PasswordField(
        "Password",
        validators=[DataRequired(), strong_password],
        render_kw={"placeholder": "Enter your password"},
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match.")],
        render_kw={"placeholder": "Confirm your password"},
    )

    submit = SubmitField("Save")

    def validate_username(self, username):
        db: Session = get_db()
        user = db.query(User).filter(User.username == username.data).first()
        if user:
            raise ValidationError("Username is already taken. Please choose a different one.")
        
    def validate_email(self, email):
        db: Session = get_db()
        user = db.query(User).filter(User.email == email.data).first()
        if user:
            raise ValidationError("Email is already registered. Please choose a different one.")
        
#  User Edit Form data validation

class EditUserForm(FlaskForm):

    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=20)]
    )

    email = StringField(
        "Email",
        validators=[DataRequired(), Email(), Length(max=120)]
    )

    full_name = StringField(
        "Full Name",
        validators=[Length(max=50)]
    )

    is_active = BooleanField("Is Active")

    password = PasswordField(
        "Password",
        validators=[strong_password],
        render_kw={"placeholder": "Enter new strong password"},
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[EqualTo("password", message="Passwords must match.")],
        render_kw={"placeholder": "Confirm your new password"},
    )

    submit = SubmitField("Update")

    def __init__(self, original_user: User, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.original_user = original_user

    def validate_username(self, username):
        if username.data != self.original_user.username:
            db: Session = get_db()
            user = db.query(User).filter(User.username == username.data).first()
            if user:
                raise ValidationError("Username is already taken. Please choose a different one.")

    def validate_email(self, email):
        if email.data != self.original_user.email:
            db: Session = get_db()
            user = db.query(User).filter(User.email == email.data).first()
            if user:
                raise ValidationError("Email is already registered. Please choose a different one.")   
                 
# Delete User Form validation 
 
class DeleteUserForm(FlaskForm):
    submit = SubmitField("Delete ")




