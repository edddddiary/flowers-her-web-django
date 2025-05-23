from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegistrationForm, Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method=="POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            # if form.cleaned_data("password")== form.cleaned_data(confim_password):
            password = form.cleaned_data["password"]
            phone_number = form.cleaned_data["phone_number"]
            username =email.split("@")[0]
            user = Account.objects.create_user(first_name= first_name, last_name=last_name, email=email, username =username,password= password)
            user.phone_number = phone_number
            user.save()
            messages.success(request,"Registration Sucsesfull.")
            return redirect("account:register")
        else:
            messages.error(request, "error")
    else:
        form = RegistrationForm()

    context ={
        "form" : form,
    }
    return render (request,"account/register.html", context)


def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = auth.authenticate(email=email, password=password)  # ← perbaikan di sini
        if user is not None:
            auth.login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Log in unsuccessful.")
            return redirect("account:login")
    return render(request, "account/sign_in.html")

@login_required(login_url="account:login")
def logout(request):
    auth.logout(request)
    messages.success(request,"You are log out")
    return redirect("account:login")