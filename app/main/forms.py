from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, SelectField, TextAreaField, HiddenField, \
    DateTimeField,FloatField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from datetime import datetime

class CfgNotifyForm(FlaskForm):
    # check_order     = StringField('排序', validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    account_month   = DateTimeField("月份", format='%Y-%m',default = datetime.utcnow)
    account_type    = SelectField('收支类型', choices=[('Z', '支出'), ('S', '收入')],
                               validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    account_name    = StringField('支付项目' )#, choices=[
                                            # ('外卖', '外卖'),
                                            # ('打车', '打车'),
                                            # ('咖啡', '咖啡'),
                                            # ('超市', '超市'),
                                            # ('地铁', '地铁'),
                                            # ('游戏', '游戏'),
                                            # ('水', '水'),
                                            # ('购物', '购物'),
                                            #
                                            # ])
    account_money   = StringField('金钱', )
    status          = BooleanField('生效标识', default=True)
    account_date    = DateTimeField("时间", format='%Y-%m-%d',default = datetime.utcnow)
    account_USD     = StringField('美金')
    account_BYN     = StringField('卢布')
    submit          = SubmitField('提交')
