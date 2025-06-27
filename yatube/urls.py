from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls.static import static
from django.conf import settings

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("", views.index, name="index"),

    path('group/delete/<int:group_id>/', views.delete_group, name='delete_group'),
    path('group/edit/<int:group_id>/', views.edit_group, name='edit_group'),
    path('group/<int:group_id>/', views.group_detail, name='group_detail'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),

    path("about/", views.about, name="about"),
    path("orders/", views.orders, name="orders"),

    path("forms/",views.send_form, name="send_form"),

    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path("register/", views.register, name="register"),
    path("sucsess_form/", views.sucsess_form, name="sucsess_form"),

    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),

]