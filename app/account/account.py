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
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        url = "http://webforex.hermes.hexun.com/forex/quotelist?code=FOREX{}{}&column=Code,LastClose".format(money,money2)
        req = urllib.request.Request(url, headers=headers)
        f = urllib.request.urlopen(req)
        html = f.read().decode("utf-8")
        s = re.findall("{.*}", str(html))[0]
        sjson = json.loads(s)
        Results = sjson["Data"][0][0][1] / 10000

        return Results



print(change_rate("BYN","CNY"))
