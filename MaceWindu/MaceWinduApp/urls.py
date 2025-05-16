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
    path('observationPoints/addObservationPoint/',views.add_observation_point_view,name="add_observation_point"),
    path('observationPoints/deleteObservationPoint/<int:pk>',views.delete_observation_point_view,name="delete_observation_point"),
    path('observationPoints/updateObservationPoint/<int:pk>',views.update_observation_point_view,name="update_observation_point"),
    path('profile/updateProfile/',views.update_user_ufl_name_view,name="update_user_profile"),
    path('profile/',views.profile_view,name='profile'),
    path('profile/changePassword/',views.CustomPasswordChangeView.as_view(),name="password_change"),
    path('analysisChoice/',views.analysis_choice_view,name="analysis_choice"),
    path('ObservationPointAnalysis/',views.op_analysis_view,name="op_analysis"),
    path('SnapshotAnalysis/',views.snapshot_analysis_view,name='snapshot_analysis')



]