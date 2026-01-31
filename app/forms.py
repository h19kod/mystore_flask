from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('اسم المستخدم', 
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('البريد الإلكتروني', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('كلمة المرور', 
                             validators=[DataRequired()])
    confirm_password = PasswordField('تأكيد كلمة المرور', 
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('إنشاء حساب')

    # التحقق من أن الاسم غير مكرر
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('هذا الاسم مستخدم بالفعل، اختر اسماً آخر.')

    # التحقق من أن الإيميل غير مكرر
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('هذا البريد الإلكتروني مسجل بالفعل.')

class LoginForm(FlaskForm):
    email = StringField('البريد الإلكتروني', validators=[DataRequired(), Email()])
    password = PasswordField('كلمة المرور', validators=[DataRequired()])
    remember = BooleanField('تذكرني')
    submit = SubmitField('تسجيل الدخول')