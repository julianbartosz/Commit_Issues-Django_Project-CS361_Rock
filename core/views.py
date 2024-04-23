from django.shortcuts import render


def home(request):
    return render(request, 'core/home.html')


def search_select(request):
    return render(request, 'core/search_select.html')
