from django.urls import path
from . import views
urlpatterns=[
    path('register/', views.register_view,name="register"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('observationPoints/',views.user_observation_points_view,name='observation_points_list'),
    path('addObservationPoint/',views.add_observation_point_view,name="add_observation_point")



]