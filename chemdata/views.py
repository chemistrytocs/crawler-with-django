from django.shortcuts import render
from chemdata.crawler.TCI import tci
from chemdata.models import Compound

# Create your views here.
def home(request):
    return render(request, 'chemdata/home.html')

def get_r(request):
    if request.method == 'POST':
        _input = request.POST
        cas = _input['cas']
        message = tci(cas)
        Comps = Compound.objects.filter(cas__contains=cas)
        context = {'message':message,'Comps':Comps}
        return render(request,'chemdata/results.html',context)
    return render(request,'chemdata/results.html',{'message':message})
    