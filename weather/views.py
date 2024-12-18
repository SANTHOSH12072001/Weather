from django.shortcuts import render, redirect
import requests
from weatherapp.form import CityForm
from .models import City
from django.contrib import messages

API_KEY=""
url='https://api.openweathermap.org/data/2.5/weather?q={},&appid=63f6776935b8c38f2c15d5ccd9d707ca&units=metric'

# Create your views here.
def home(request):
    if request.method=="POST":
        form=CityForm(request.POST)
        if form.is_valid():
            Cname=form.cleaned_data['name']
            print(Cname)
            city=City.objects.filter(name=Cname).count()
            if city==0:  
                res=requests.get(url.format(Cname)).json()
                print(res)
                if res['cod']==200:
                    form.save()
                    messages.success(request,"City Added Successfully")
                    return redirect('home')
                else:
                    messages.error(request,"City not found")
                    return redirect('home')
            else:
                messages.error(request,'City Already Exists')
                return redirect('home')
        return render(request,'weather.html',{'form':form})
    form=CityForm()
    cities=City.objects.all()
    data=[]
    for Wcity in cities:
        res=requests.get(url.format(Wcity)).json()
        city_weather={
            'city':Wcity,
            'temperature':res['main']['temp'],
            'description':res['weather'][0]['description'],
            'country':res['sys']['country'],
            'icon':res['weather'][0]['icon']
        }
        data.append(city_weather)
    return render(request,'weather.html',{'data':data, 'form':form})

def delete(request,name):
    deletes=City.objects.get(name=name)
    deletes.delete()
    messages.error(request, "City Deleted Successfully")
    return redirect('home')


    
