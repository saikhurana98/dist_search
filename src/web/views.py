from django.shortcuts import render


def home(request):
    context = {}
    template = 'web/home.html'
    return render(request, template, context)

def results(request):
    context = {}
    template = 'web/results.html'
    return render(request, template, context)

