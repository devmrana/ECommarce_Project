from django.urls import path
from LoginApp import views

app_name = "LoginApp"


urlpatterns = [
    path('signup/',views.signUpUser, name='signup'),
    path('login/',views.loginUser, name='login'),
    path('logout/',views.logoutUser, name='logout'),
    path('profile/',views.profile, name='profile'),
    path('change-profile/',views.userProfile, name='changeprofile'),
]