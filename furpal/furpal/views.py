from django.shortcuts import render


def home(request):
    return render(request, 'furpal/home.html')


def about(request):
    return render(request, 'furpal/about.html', {'title': 'About'})
