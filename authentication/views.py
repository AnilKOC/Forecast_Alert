from django.shortcuts import render
from django.db import connection
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm

def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/dashboard/")
            else:    
                msg = 'Invalid credentials'    
        else:
            msg = 'Error validating the form'
    return render(request, "accounts/login.html", {"form": form, "msg" : msg})

def register_user2(request):
    msg     = None
    success = False
    if request.method == "POST":
        form = SignUpForm(request.POST)
        print(form.username)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            msg     = 'User created.'
            success = True
        else:
            msg = 'Form is not valid'    
    else:
        form = SignUpForm()
    return render(request, "accounts/register.html", {"form": form, "msg" : msg, "success" : success })

def register_user(request,division):
    msg     = None
    success = False
    role = None
    if division == 1:
        role="Silver"
    if division == 2:
        role="Gold"
    if division == 3:
        role="Platinium"
    if division == 4:
        role="Diamond"
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user_id=form.save().id
            cursor = connection.cursor()
            sql = "INSERT INTO auth_user_groups SET user_id=%s, group_id=%s"
            val = int(user_id),int(division)
            cursor.execute(sql, val)
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            msg = 'User created.'
            success = True
        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()
    return render(request, "accounts/register.html", {"form": form,"msg" : msg, "success" : success ,"role":role})
