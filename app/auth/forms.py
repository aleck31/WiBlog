from flask import g
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField, PasswordField, RadioField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email, Length
from app.models import User


# 定义登录表单
class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()], render_kw={"placeholder": "username"})
    password = PasswordField('password', validators=[DataRequired()], render_kw={"placeholder": "password"})
    remember_me = BooleanField('', default=False)
    submit = SubmitField('Submit')


# 定义用户注册表单
class RegForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    nickname = StringField('Nickname', validators=[Length(min=0, max=32)])
    email = StringField('Email', description="* We do not share your email with anybody.", validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    role = RadioField('Role', choices=[('0', u'User'), ('1', u'Admin')], default='0', validators=[DataRequired()])
    submit = SubmitField('Register')

    # 数据重复性验证
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError('Please use a different email address.')


# 定义用户资料表单
class ProfileForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    nickname = StringField('Nickname', validators=None)
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)], render_kw={"placeholder": "不超过140字符"})
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data == g.user.email:
            return True
        else:
            email = User.query.filter_by(email=email.data).first()
            if email is not None:
                raise ValidationError('Please use a different email address.')
