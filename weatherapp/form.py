from django.forms import TextInput, ModelForm
from weather.models import City

class CityForm(ModelForm):
    class Meta:
        model=City
        fields=['name']
        widgets={
            'name':TextInput(attrs={'class':'form-control' , 'placeholder':'City Name'})}

