from django.shortcuts import render,redirect
from .models import Search
from django.http import HttpResponse
from .forms import SearchForm
import folium
import geocoder
# Create your views here.
def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form= SearchForm()
    address= Search.objects.all().last()
    location = geocoder.osm(address)
    lat = location.lat
    lng = location.lng
    country = location.country
    if lat==None or lng==None:
        address.delete()
        return HttpResponse('Your Input is Invalid')
   
    #create map object
    m=folium.Map([19,-12],zoom_start=2)
    folium.Marker([lat,lng],tooltip='click for more',popup=country).add_to(m)
    m=m._repr_html_()
    context = {
        'm':m,
         'form': form,
    }
    return render(request, 'index.html',context)