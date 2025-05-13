from django.urls import path
from django.views.generic import RedirectView

from . import views
urlpatterns=[
    path('', RedirectView.as_view(url='/MaceWindu/dashboard/', permanent=False)),
    path('register/', views.register_view,name="register"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('observationPoints/',views.user_observation_points_view,name='observation_points_list'),
    path('addObservationPoint/',views.add_observation_point_view,name="add_observation_point"),
    path('deleteObservationPoint/<int:pk>',views.delete_observation_point_view,name="delete_observation_point"),
    path('updateObservationPoint/<int:pk>',views.update_observation_point_view,name="update_observation_point"),
    path('updateProfile/',views.update_user_ufl_name_view,name="update_user_profile"),
    path('profile/',views.profile_view,name='profile')



]