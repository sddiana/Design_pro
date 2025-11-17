from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

def home(request):
    # Определяем тип пользователя для отображения
    user_type = "Гость"
    if request.user.is_authenticated:
        if request.user.is_superuser:
            user_type = "Администратор"
        elif request.user.is_staff:
            user_type = "Персонал"
        else:
            user_type = "Пользователь"
    
    context = {
        'user_type': user_type
    }
    return render(request, 'main/home.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'main/profile.html')