from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from .forms import RegistrationForm
from django.contrib.auth.models import User

def index(request):
    return render(request, 'main/index.html', {})

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username  = form.cleaned_data['username'],
                first_name = form.cleaned_data['first_name'],
                last_name = form.cleaned_data['last_name'],
                email = form.cleaned_data['email'],
                password = form.cleaned_data['password'],
            )
            user.save()
            return render(request, 'main/successful_registration.html', {})
    form = RegistrationForm()
    return render(request, 'main/register.html', {'form': form})