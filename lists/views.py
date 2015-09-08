from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_page(request):
	return render(request,'home.html') # En lugar de usar HttpResponse, se usa render, necesita un request y la plantilla