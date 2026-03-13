from django.shortcuts import render

# Create your views here.
def user_signin(request):
    return render(request,"surveys/signin.html")