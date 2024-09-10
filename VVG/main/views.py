from django.shortcuts import render

def index(reqquest):
    return render(request, 'main/index.html', {})