#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: soliva
@Site: 
@file: account.py
@time: 2021/2/13
@desc:
mainly Principles:

'''

import re
import json
import urllib.request

def change_rate(money,money2)->float:
        import pandas as pd
        try:
                bank_data = pd.read_html("https://www.nbrb.by/engl/statistics/rates/ratesdaily.asp")[0]
                bank_data.to_csv("/home/soliva/progect/accountbook/flask-adminlte-scaffold/conf/rate.csv")
        except :
                bank_data  = pd.read_csv("/home/soliva/progect/accountbook/flask-adminlte-scaffold/conf/rate.csv")

        RMB = float(bank_data.query("`Foreign currency name`== 'Yuan Renminbi'")["Official rate"])
        USD = float(bank_data.query("`Foreign currency name`== 'US Dollar'")["Official rate"])
        RMB_rate = 10 / RMB#2.5
        USD_rate = USD#2.5
        rate_dict = {"CNY":{"USD":1/(RMB_rate*USD_rate),"BYN":1/RMB_rate},
                     "BYN":{"CNY":1*RMB_rate,"USD":1/USD_rate},
                     "USD":{"CNY":1*(RMB_rate*USD_rate),"BYN":1*USD_rate}}
        Results= rate_dict.get(money).get(money2)
        return Results



print(change_rate("USD","BYN"))
print(10000*change_rate("CNY","USD")*change_rate("USD","BYN"))