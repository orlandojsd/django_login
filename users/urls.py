from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('update/', views.update_user, name="update"),
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),
    path('register/', views.registration_user, name="register")

]