import requests
from lxml import etree
import re
from chemdata.models import Compound


def get_table(html):  # get the price information from TCI website
    path = '//table[@class="comp-tbl"]//span/text()|//table[@class="price-tbl"]//td//text()'
    _result = html.xpath(path)
    return _result


def separate(original_data):  # extract and separate data from original html
    b = []
    c = []
    for i in original_data:  # separate data for each compound
        i = i.strip()  # extract data
        b.append(i)
        if re.match('製品コード', i):
            c.append(b[:-1])
            b = ['製品コード']
    c.append(b)
    c = c[1:]
    return c


def get_data(_l, cas):
    a = {}
    b = []

    def _next(_list, _b):
        _a = _list[_list.index(_b)+1]
        return _a
    for list in _l:  # save data by dict
        if _next(list, "CAS RN") == cas:
            a["code"] = _next(list, "製品コード")
            a["name"] = _next(list, "製品名")
            a["pury"] = _next(list, '純度/試験方法')
            a["cas"] = _next(list, "CAS RN")
            a["pack"] = _next(list, '包装単位')
            a["price"] = int(re.sub(r'[^0-9\.]*', '', _next(list, '価格')))
            a["stock"] = '川口:{};尼崎:{};保管在庫:{}'.format(
                _next(list, '埼玉県(川口)'), _next(list, '兵庫県(尼崎)'), _next(list, '保管在庫'))
            a['maker']='tci'
            b.append(a)
            a = {}
    return b


def tci(cas):  # TCI crawler
    url = "http://www.tcichemicals.com/eshop/ja/jp/catalog/list/search?searchWord={}&client=default_frontend&output=xml_no_dtd&proxystylesheet=default_frontend&sort=date%3AD%3AL%3Ad1&oe=UTF-8&ie=UTF-8&ud=1&exclude_apps=1&site=ja_jp&pageSize=20&alignmentSequence=18&mode=0".format(
        cas)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36", "host": "www.tcichemicals.com"
    }
    req = requests.get(url=url, headers=headers)
    if req.status_code == 200:
        message = "TCI requests successfully!"
    else:
        message = "Fail in connect!"
        return message
    html = etree.HTML(req.content)
    try:
        results = get_data(separate(get_table(html)), cas)
    except BaseException:
        message = 'Fail in website data!'
    
    try:
        for i in results:
            elem = Compound()
            elem.entry(i)
            elem.save()
    except BaseException:
        message = 'Fail in inputting data to sql!'
    return message
