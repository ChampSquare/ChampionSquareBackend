from django.shortcuts import render

def homepage(request):
    """The homepage for unauthenticatd users """
    return render(request, "home/index.html", {})