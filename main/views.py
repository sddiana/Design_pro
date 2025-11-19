from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    user_type = "Гость"
    if request.user.is_authenticated:
        if request.user.is_superuser:
            user_type = "Администратор"
        else:
            user_type = "Пользователь"
    
    context = {
        'user_type': user_type
    }
    return render(request, 'main/home.html', context)

@login_required
def profile(request):
    return render(request, 'main/profile.html')
