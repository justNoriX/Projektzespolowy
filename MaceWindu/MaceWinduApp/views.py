from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from .forms import CustomUserCreationForm, LoginForm, ObservationPointForm, UpdateUserUFLNameForm
from .models import ObservationPoint, SnapShot


def register_view(request):
    if request.method=="POST":
        form=CustomUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request, user)
            messages.success(request,"Poprawnie zarejestrowano konto w systemie.")
            return redirect("dashboard")
        else:
            messages.error(request,"Wystąpiły błędy w formularzu.")
            return render(request, 'register.html',{'form':form})
    else:
        form=CustomUserCreationForm()
        return render(request,'register.html',{'form':form})

def login_view(request):
    if request.method=="POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            messages.success(request,"Poprawnie zalogowano się do systemu")
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
def update_user_ufl_name_view(request):
    user=request.user
    if request.method=="POST":
        form=UpdateUserUFLNameForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            messages.success(request,"Zaktualizowano dane dotyczące profilu")
            return redirect('profile')
        else:
            messages.error(request,"Wystąpiły błędy w formularzu")
            return render(request, 'update_user_ufl.html', {'form': form})
    else:
        form=UpdateUserUFLNameForm(instance=user)
    return render(request,'update_user_ufl.html',{'form':form})

@method_decorator(login_required,name='dispatch')
class CustomPasswordChangeView(SuccessMessageMixin,PasswordChangeView):
    template_name = 'password_change_form.html'
    success_url = reverse_lazy('dashboard')
    success_message = "Hasło zostało zmienione pomyślnie"


@login_required
def dashboard_view(request):
    return render(request,'dashboard.html',{'user':request.user})
@login_required
def analysis_choice_view(request):
    observation_points=ObservationPoint.objects.filter(user=request.user)
    snapshots=SnapShot.objects.filter(observation_point__user=request.user)
    return render(request,'analysis_choice.html',{'observation_points':observation_points, 'snapshots':snapshots})
@login_required
def op_analysis_view(request):
    observation_point_id=request.GET.get('observation_point_id')
    observation_point=get_object_or_404(ObservationPoint,pk=observation_point_id, user=request.user)
    #TUTAJ KOMUNIKACJA Z ZEWNĘTRZNYM API
    #TUTAJ ODBYWA SIĘ PARSOWANIE WYNIKU Z API
    #TUTAJ ODBYWA SIĘ ZAPIS DO SESJI TYCH ODEBRANYCH I SPARSOWANYCH WYNIKÓW
    #ODEBRANE DANE ZOSTAJĄ PRZEKAZANE DO RENDERU PONIŻEJ
    return render(request,'op_analysis.html')

@login_required
def snapshot_analysis_view(request):
    snapshot_id=request.GET.get('snapshot_id')
    snapshot=get_object_or_404(SnapShot,pk=snapshot_id,user=request.user)
    #DO PÓŹNIEJSZEJ IMPLEMENTACJI
    return render(request,'snapshot_analysis.html')
@login_required
def profile_view(request):
    return render(request,'profile.html',{'user':request.user})
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
        if form.is_valid():
            observation_point=form.save(commit=False)
            observation_point.user=user
            observation_point.save()
            messages.success(request,"Dodano lokalizację")
            return redirect("observation_points_list")
        else:
            messages.error(request,"Wystąpiły błędy w formularzu")
            return render(request, 'observation_point_form.html', {'form': form})
    else:
        form=ObservationPointForm()
        return render(request,'observation_point_form.html',{'form':form})

@login_required
def delete_observation_point_view(request,pk):
    observation_point=get_object_or_404(ObservationPoint,pk=pk,user=request.user)
    if request.method=="POST":
        observation_point.delete()
        messages.success(request,"Usunięto lokalizację")
        return redirect("observation_points_list")
    return render(request,"delete_observation_point.html",{"observation_point":observation_point})

@login_required
def update_observation_point_view(request,pk):
    observation_point = get_object_or_404(ObservationPoint, pk=pk, user=request.user)
    if request.method=="POST":
        form=ObservationPointForm(request.POST, instance=observation_point)
        if form.is_valid():
            form.save()
            messages.success(request,"Zaktualizowano lokalizację")
            return redirect("observation_points_list")
        else:
            messages.error(request,"Wystąpiły błędy w formularzu")
            return render(request, "update_observation_point.html",{"form": form, "observation_point": observation_point})

    else:
        form=ObservationPointForm(instance=observation_point)
        return render(request,"update_observation_point.html",{"form":form, "observation_point":observation_point})

