from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.urls import reverse


# Create your views here.
def logout_view(request):
    """log the user out"""
    logout(request)
    return HttpResponseRedirect(reverse("journal:index"))

def register(request):
    """register a new user"""
    if request.method != "POST":
        #display blank registration page
        form = UserCreationForm()
    else:
        #post the form
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            #log user in and redirect to home page
            authenticated_user = authenticate(username=new_user.username,
            password=request.POST["password1"])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse("journal:index"))

    context = {"form": form}
    return render(request, "users/register.html", context)
