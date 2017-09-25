from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# index page
def index(request):
    return render(request, 'dashboard/index.html')
