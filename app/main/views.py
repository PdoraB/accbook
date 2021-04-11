from app import get_logger, get_config
import math
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import utils
from app.models import CfgNotify
from app.main.forms import CfgNotifyForm
from . import main
from app.account.account import change_rate
import pandas as pd
from datetime import datetime

logger = get_logger(__name__)
cfg = get_config()

# 通用列表查询
def common_list(DynamicModel, view):
    # 接收参数
    action = request.args.get('action')
    id = request.args.get('id')
    page = int(request.args.get('page')) if request.args.get('page') else 1
    length = int(request.args.get('length')) if request.args.get('length') else cfg.ITEMS_PER_PAGE

    # 删除操作
    if action == 'del' and id:
        try:
            DynamicModel.get(DynamicModel.id == id).delete_instance()
            flash('删除成功')
        except:
            flash('删除失败')

    # 查询列表
    query = DynamicModel.select()
    total_count = query.count()
    #
    # # 处理分页
    if page: query = query.paginate(page, length)

    #
    dict = {'content': utils.query_to_list(query), 'total_count': total_count,
            'total_page': math.ceil(total_count / length), 'page': page, 'length': length}


    return render_template(view, form=dict, current_user=current_user)


# 通用单模型查询&新增&修改
def common_edit(DynamicModel, form, view):
    id = request.args.get('id', '')
    if id:
        # 查询
        model = DynamicModel.get(DynamicModel.id == id)
        if request.method == 'GET':
            utils.model_to_form(model, form)
        # 修改
        if request.method == 'POST':
            if form.validate_on_submit():
                utils.form_to_model(form, model)
                model.save()
                flash('修改成功')
            else:
                utils.flash_errors(form)
    else:
        # 新增
        if form.validate_on_submit():
            model = DynamicModel()

            utils.form_to_model(form, model)

            if model.account_money!="":

                model.account_USD = round(float(model.account_money) * change_rate("CNY","USD"), 3)
                model.account_BYN = round(float(model.account_money)   * change_rate("CNY","BYN"), 3)

            elif model.account_USD !="" :
                model.account_money = round(float(model.account_USD) * change_rate("USD","CNY"), 3)
                model.account_BYN = round(float(model.account_USD) * change_rate("USD","BYN"), 3)
            elif model.account_BYN!="":
                model.account_USD = round(float(model.account_BYN) * change_rate("BYN","USD"), 3)
                model.account_money = round(float(model.account_BYN) * change_rate("BYN","CNY"), 3)

            model.save()
            flash('保存成功')
        else:
            utils.flash_errors(form)

    return render_template(view, form=form, current_user=current_user)

def index_plot(DynamicModel, view):
    query = DynamicModel.select()
    query_df =pd.DataFrame(list(query.dicts()))
    Expenses = query_df[query_df["account_type"] == "Z"].round(3)
    month_time = Expenses.groupby("account_month").sum().index
    month_time = [i.strftime('%y-%m') for i in month_time]
    Expenses['account_date']=pd.to_datetime(Expenses['account_date'])
    nowtime = datetime.now().strftime("%Y-%m")
    try:
        ruble = round(change_rate("BYN", "CNY"), 2)
        USDs = round(change_rate("USD", "CNY"), 2)
    except :
        ruble = 2.50
        USDs = 6.55


    dict = {
        'content': utils.query_to_list(query),
        "account_name": list(month_time),
        "account_money": Expenses.groupby("account_month").sum()["account_money"].round(3).to_list(),
        "days_statistic":Expenses.groupby("account_date").sum()["account_money"][-1].round(3),
        "months_statistic":Expenses.groupby("account_month").sum()["account_money"][-1].round(3),
        "Ruble":ruble,
        "USDs":USDs,
        "hist_count":Expenses.set_index('account_date').sort_index()[nowtime:].groupby("account_name").sum()["account_money"].round(3).to_list(),
        "hist_name":Expenses.set_index('account_date').sort_index()[nowtime:].groupby("account_name").sum().index
            }

    return render_template(view, form=dict, current_user=current_user)
# 根目录跳转
@main.route('/', methods=['GET'])
@login_required
def root():
    return redirect(url_for('main.index'))


# 首页
@main.route('/index', methods=['GET'])
@login_required
def index():
    return index_plot(CfgNotify, 'index.html')


# 通知方式查询
@main.route('/notifylist', methods=['GET', 'POST'])
@login_required
def notifylist():
    return common_list(CfgNotify, 'notifylist.html')


# 通知方式配置
@main.route('/notifyedit', methods=['GET', 'POST'])
@login_required
def notifyedit():
    return common_edit(CfgNotify, CfgNotifyForm(), 'notifyedit.html')
