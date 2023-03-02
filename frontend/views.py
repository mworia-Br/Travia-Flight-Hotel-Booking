from django.shortcuts import render

# Create your views here.

def Index(req):
    return render(req, 'index.html')