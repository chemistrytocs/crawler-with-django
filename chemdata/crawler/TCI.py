import requests
from lxml import etree
import re
from chemdata.models import Compound


def get_table(html):  # get the price information from TCI website
    result = [[], []]
    # get compound information
    for comp_tbl in html.xpath('//table[@class="comp-tbl"]'):
        comp = {}
        for a in comp_tbl.xpath('.//tr'):
            b = a.xpath('.//span/text()')
            if b[0] in ["製品コード","製品名",'純度/試験方法',"CAS RN"]: # the position of necessary data
                comp[b[0]] = b[1]
        result[0].append(comp)
    # get price information
    for comp_price in html.xpath('//table[@class="price-tbl"]'):
        comp = []
        for elem in comp_price.xpath('.//tr[position()>2]'):
            comp_d_s = []
            for n, i in enumerate(elem.xpath('.//td/text()')):
                if n in [1, 3, 6, 8, 10]:  # the position of necessary data in table
                    comp_d_s.append(i.strip())
            comp.append(comp_d_s)
        result[1].append(comp)
    return result  # [[compound information],[price information]]


def separate(_l, cas):  # clean up the data and save it to dict
    a = {}
    b = []
    for n, comp in enumerate(_l[0]):  # separate compound
        if comp["CAS RN"] == cas:  # check data
            a["code"] = comp["製品コード"]
            a["name"] = comp["製品名"]
            a["pury"] = comp['純度/試験方法']
            a["cas"] = comp["CAS RN"]
            a['maker'] = 'tci'
            if len(_l[1][n]) == 1:
                i = _l[1][n][0]
                a["pack"] = i[0]
                a["price"] = int(re.sub(r'[^0-9\.]*', '', i[1])) # clean up price to int
                a["stock"] = '川口:{};尼崎:{};保管在庫:{}'.format(
                    i[2], i[3], i[4])
                b.append(a)
                a = {}
            else:  # separate for different pack
                for i in _l[1][n]:
                    a["pack"] = i[0]
                    a["price"] = int(re.sub(r'[^0-9\.]*', '', i[1]))
                    a["stock"] = '川口:{};尼崎:{};保管在庫:{}'.format(
                        i[2], i[3], i[4])
                    b.append(a.copy())
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
        results = separate(get_table(html), cas)
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
