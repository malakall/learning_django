from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path("", views.index, name="index"),

    path('group/delete/<int:group_id>/', views.delete_group, name='delete_group'),

    path("about/", views.about, name="about"),
    path("orders/", views.orders, name="orders"),

    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path("register/", views.register, name="register"), 
    
]