from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm

def index(request):
	url = 'http://api.openweathermap.org/data/2.5/weather?q={}&APPID=7a60081fa7a88330e5e61ded7ae6c109'

	err_msg = ''
	msg = ''
	msg_cls = ''

	if request.method == 'POST':
		form = CityForm(request.POST)
		

		if form.is_valid():
			new_city = form.cleaned_data['name']
			existing_city = City.objects.filter(name=new_city).count()

			if existing_city == 0:

				r = requests.get(url.format(new_city)).json()	

				if r['cod'] == 200:
					form.save()
				else:
					err_msg = 'City Does Not Exist In the World'

			else:
				err_msg = 'City Already Exist In The Database'


		if err_msg:
			msg = err_msg
			msg_cls = 'is-danger'
		else:
			msg = 'City Added Successfully'
			msg_cls = 'is-success'
				
	
	form = CityForm()

	cities = City.objects.all()

	city_data = []
	
	for city in cities:

		r = requests.get(url.format(city)).json()
		
		city_weather = {
			'city':city.name,
			'temp':r['main']['temp'],
			'desc':r['weather'][0]['description'],
			'icon':r['weather'][0]['icon'],
		}

		city_data.append(city_weather)

	context = {
		'city_data':city_data,
		'form':form,
		'msg':msg,
		'msg_cls':msg_cls,
	}

	return render(request, 'weather/index.html', context)




def srch(request):
	url = 'http://api.openweathermap.org/data/2.5/weather?q={}&APPID=7a60081fa7a88330e5e61ded7ae6c109'

	errs = ''
	msgs = ''
	msgs_cls = ''
	
	given_name = request.POST['srchname']

	cities = City.objects.filter(name=given_name).first()

	r = requests.get(url.format(cities)).json()
	
	if r['cod'] == 404:
		errs = 'City Not Exist In The World'

	if errs:
		msgs = errs
		msgs_cls = 'is-danger'


	city_weather = {
			'city':cities,
			'temp':r['main']['temp'],
			'desc':r['weather'][0]['description'],
			'icon':r['weather'][0]['icon'],
	}

	context = {
		'city_weather':city_weather,
		'msgs':msgs,
		'msgs_cls':msgs_cls,
	}

	return render(request, 'weather/srch.html', context)








