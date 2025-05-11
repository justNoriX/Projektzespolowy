from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, LoginForm, ObservationPointForm
from .models import ObservationPoint


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

def logout_view(request):
    logout(request)
    return redirect('login')
@login_required
def dashboard_view(request):
    return render(request,'dashboard.html',{'user':request.user})

@login_required
def user_observation_points_view(request):
    observation_points=ObservationPoint.objects.filter(user=request.user)
    return render(request, 'observation_points.html',{'observation_points':observation_points})

@login_required
def add_observation_point_view(request):
    if request.method=="POST":
        form=ObservationPointForm(request.POST)
        observation_point=form.save(commit=False)
        observation_point.user=request.user
        observation_point.save()
        return redirect("observation_points_list")
    else:
        form=ObservationPointForm()
        return render(request,'observation_point_form.html',{'form':form})