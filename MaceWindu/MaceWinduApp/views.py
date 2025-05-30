from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode
from .mailsender import send_verification_mail

from .forms import CustomUserCreationForm, LoginForm, ObservationPointForm, UpdateUserUFLNameForm
from .models import ObservationPoint, SnapShot, CustomUser
from .services.weather_service import GoogleWeatherService, parse_weather_response



def register_view(request):
    if request.method=="POST":
        form=CustomUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.is_active=False
            user.is_staff=False
            user.is_superuser=False
            user.save()
            current_site=get_current_site(request)
            send_verification_mail(user,current_site)
            messages.success(request,"Poprawnie zarejestrowano konto w systemie. Przed zalogowaniem zweryfikuj konto poprzez link wysłany na adres e-mail")
            return redirect("login")
        else:
            messages.error(request,"Wystąpiły błędy w formularzu.")
            return render(request, 'register.html',{'form':form})
    else:
        form=CustomUserCreationForm()
        return render(request,'register.html',{'form':form})

def activate_account_view(request, uid, token):
    try:
        uid=urlsafe_base64_decode(uid).decode()
        user=CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active=True
        user.save()
        messages.success(request, 'Konto zostało aktywowane. Możesz się teraz zalogować.')
    else:
        messages.error(request,"Link jest nieprawidłowy lub wygasł.")
    return redirect('login')
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

@login_required
def delete_account_view(request):
    if request.method=='POST':
        password=request.POST.get('password')
        user=request.user
        if user.check_password(password):
            logout(request)
            user.delete()
            messages.success(request,'Twoje konto zostało usunięte')
            return redirect('login')
        else:
            messages.error(request,'Niepoprawne hasło')
    return render(request,'delete_account.html')
@method_decorator(login_required,name='dispatch')
class CustomPasswordChangeView(SuccessMessageMixin,PasswordChangeView):
    template_name = 'password_change_form.html'
    success_url = reverse_lazy('dashboard')
    success_message = "Hasło zostało zmienione pomyślnie"

class CustomForgotPasswordEmailView(SuccessMessageMixin,PasswordResetView):
    template_name = 'forgot_password_email_form.html'
    email_template_name = 'email_templates/forgot_password_email.html'
    subject_template_name ='email_templates/forgot_password_subject.txt'
    success_url = reverse_lazy('forgot_password_email_sent')

class CustomForgotPasswordEmailSentView(PasswordResetDoneView):
    template_name = 'forgot_password_email_sent.html'

class CustomForgotPasswordChangeView(SuccessMessageMixin, PasswordResetConfirmView):
    template_name = 'forgot_password_change_form.html'
    success_url = reverse_lazy('forgot_password_complete')

class CustomForgotPasswordCompleteView(PasswordResetCompleteView):
    template_name = 'forgot_password_complete.html'
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

    lat = float(observation_point.latitude)
    lon = float(observation_point.longitude)

    try:
        data = GoogleWeatherService.get_hourly_history(lat, lon)
        simplified_data = parse_weather_response(data)
        print(simplified_data)
        #tutaj wyciągnięte dane musimy też sobie sparsować do pythonowego query seta oraz zapisać w sesji parametry wiatru aby móc je zapisać do snapshota

    except Exception as e:
        return JsonResponse(
            {"error": "Nie udało się pobrać danych pogodowych", "details": str(e)},
            status=500,
        )

    return render(request, 'op_analysis.html', {
        "weather_data": simplified_data,
        "observation_point": observation_point
    })

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

