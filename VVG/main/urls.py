from django.urls import path
from django.contrib.auth.views import(
        LoginView,
        LogoutView
)
from .forms import(
        AuthenticationForm,
)
from . import views


urlpatterns = [
        path(r'', views.index, name='index'),
        path(r'accounts/login/', LoginView.as_view(), {
                'template_name': 'login.html',
                'authentication_form': AuthenticationForm
        }, name='login'),
        
        path(r'accounts/logout', LogoutView.as_view(), {
                #'next_page': '/'
        }, name='logout'),
        
        path(r'accounts/register/', views.register, name='register'),
]
