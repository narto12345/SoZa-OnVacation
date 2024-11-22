from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def InitialPage (request):
    probando= "Finjamos que vengo de la bd"
    return render(request,'index.html', {'bd': probando})