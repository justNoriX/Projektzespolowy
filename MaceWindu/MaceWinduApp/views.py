from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
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
@login_required
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
    user=request.user
    observation_point_count=ObservationPoint.objects.filter(user=user).count()
    if observation_point_count>=10:
        messages.error(request, "Osiągnięto limit 10 lokalizacji. Usuń jedną, aby dodać nową.")
        return redirect("observation_points_list")

    if request.method=="POST":
        form=ObservationPointForm(request.POST)
        observation_point=form.save(commit=False)
        observation_point.user=user
        observation_point.save()
        return redirect("observation_points_list")
    else:
        form=ObservationPointForm()
        return render(request,'observation_point_form.html',{'form':form})

@login_required
def delete_observation_point_view(request,pk):
    observation_point=get_object_or_404(ObservationPoint,pk=pk,user=request.user)
    if request.method=="POST":
        observation_point.delete()
        return redirect("observation_points_list")
    return render(request,"delete_observation_point.html",{"observation_point":observation_point})

@login_required
def update_observation_point_view(request,pk):
    observation_point = get_object_or_404(ObservationPoint, pk=pk, user=request.user)
    if request.method=="POST":
        form=ObservationPointForm(request.POST, instance=observation_point)
        if form.is_valid():
            form.save()
            return redirect("observation_points_list")
    else:
        form=ObservationPointForm(instance=observation_point)
        return render(request,"update_observation_point.html",{"form":form, "observation_point":observation_point})

