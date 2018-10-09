from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField, RadioField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Length
from datetime import datetime


# 定义文章提交表单
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=0, max=64)])
    body = TextAreaField('正文', validators=[Length(min=0, max=1024)])
    timestramp = DateTimeField('日期', default=datetime.utcnow())
    draft = BooleanField('存为草稿', default=False)
    submit = SubmitField('Post')


# 搜索框
class SearchForm(FlaskForm):
    text = StringField('关键字', validators=[Length(min=0, max=32)])
    draft = BooleanField('包含草稿', default=False)
    submit = SubmitField('Search')
