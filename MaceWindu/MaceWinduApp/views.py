from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, LoginForm

def register_view(request):
    if request.method=="POST":
        form=CustomUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form=CustomUserCreationForm()
        return render(request,'register.html',{'form':form})

def login_view(request):
    if request.method=="POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            return redirect("dashboard")
        else:
            return render(request, 'login.html', {'form': form})

    else:
        form=LoginForm()
        return render(request,'login.html',{'form':form})

@login_required
def dashboard_view(request):
    return render(request,'dashboard.html',{'user':request.user})

def logout_view(request):
    logout(request)
    return redirect('login')