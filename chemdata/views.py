from django.shortcuts import render
from chemdata.crawler.TCI import tci
from chemdata.models import Compound

# Create your views here.
def home(request):
    return render(request, 'chemdata/home.html')

def get_r(request):
    if request.method == 'POST':
        _input = request.POST
        cas = _input['cas']  #get inputted cas
        if not Compound.objects.filter(cas__iexact=cas): # if no data
            message = tci(cas)
            Comps = Compound.objects.filter(cas__iexact=cas)
            links = {'tci':"http://www.tcichemicals.com/eshop/ja/jp/catalog/list/search?searchWord={}&client=default_frontend&output=xml_no_dtd&proxystylesheet=default_frontend&sort=date%3AD%3AL%3Ad1&oe=UTF-8&ie=UTF-8&ud=1&exclude_apps=1&site=ja_jp&pageSize=20&alignmentSequence=18&mode=0".format(
        cas)}
            context = {'message':message,'Comps':Comps,'links':links}
            return render(request,'chemdata/results.html',context)
        else:
            message = 'get the data successfully!'
            Comps = Compound.objects.filter(cas__iexact=cas)
            links = {'tci':"http://www.tcichemicals.com/eshop/ja/jp/catalog/list/search?searchWord={}&client=default_frontend&output=xml_no_dtd&proxystylesheet=default_frontend&sort=date%3AD%3AL%3Ad1&oe=UTF-8&ie=UTF-8&ud=1&exclude_apps=1&site=ja_jp&pageSize=20&alignmentSequence=18&mode=0".format(
        cas)}
            context = {'message':message,'Comps':Comps,'links':links}
            return render(request,'chemdata/results.html',context)
    message = 'Please input the data!'
    return render(request,'chemdata/results.html',{'message':message})
    