from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('accounts/login/', auth_views.LoginView.as_view()),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("accounts/profile/", views.Profile, name = 'profile'),
    path("accounts/bookings/", views.bookings, name = 'bookings'),
    path("accounts/seebs/", views.seebs, name = 'seebs'),
]