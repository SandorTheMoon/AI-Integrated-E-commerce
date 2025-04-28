from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.welcome_page, name="welcome"),   
    path("csignup/", views.signup_page, name="signup"),
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_account, name="logout"),

    path("home/", views.home_page, name="home"),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
