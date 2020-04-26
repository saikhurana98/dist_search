from django.shortcuts import render


def home(request):
    context = {}
    template = 'web/home.html'
    return render(request, template, context)
