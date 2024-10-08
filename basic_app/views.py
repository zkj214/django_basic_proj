from django.shortcuts import render
from basic_app.forms import UserForm,UserProfileInfoForm

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.


def index(request):
    return render(request,"basic_app/index.html")


def register(request):
    registered=False
    user_form=UserForm()
    profile_form=UserProfileInfoForm()

    if request.method=="POST":
        user_form=UserForm(request.POST)
        profile_form=UserProfileInfoForm(request.POST)

        if user_form.is_valid and profile_form.is_valid:
            user=user_form.save()
            user.set_password(user.password)
            user.save()

            profile=profile_form.save(commit=False)
            profile.user=user
            if "profile_pic" in request.FILES:
                profile.profile_pic=request.FILES["profile_pic"]
            profile.save()
            registered=True
        else:
            print(user_form.errors,profile_form.errors)
    return render(request,"basic_app/register.html",{"user_form":user_form,"profile_form":profile_form,"registered":registered})


def user_login(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")

        user=authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse("home"))
            else:
                return HttpResponse("USER IS NOT ACTIVE!")
        else:
            return HttpResponse("Invalid username or password")

    return render(request,"basic_app/login.html")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


@login_required
def home(request):
    return render(request,"basic_app/home.html")