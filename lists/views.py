from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_page(request):
	return render(request,'home.html',{ #item_Text es el name del input con el que se asocia
		'new_item_text': request.POST.get('item_text',''),
	}) # En lugar de usar HttpResponse, se usa render, necesita un request y la plantilla
