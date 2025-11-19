from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Application, Category
from .forms import ApplicationForm

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

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Application
from .forms import ApplicationForm

@login_required
def create_application(request):
    """Создание новой заявки"""
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.client = request.user
            application.save()
            
            messages.success(request, 'Заявка успешно создана!')
            return redirect('main:profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{form.fields[field].label}: {error}')
    else:
        form = ApplicationForm()
    
    return render(request, 'main/create_application.html', {
        'form': form
    })

@login_required
def profile(request):
    applications = Application.objects.filter(client=request.user).order_by('-created_at')
    
    status_filter = request.GET.get('status', '')
    
    if status_filter:
        applications = applications.filter(status=status_filter)
    
    context = {
        'applications': applications,
    }
    return render(request, 'main/application_detail.html', context)


@login_required 
def application_detail(request, application_id):
    """Детальная страница заявки"""
    try:
        application = Application.objects.get(id=application_id, client=request.user)
        return render(request, 'main/application_detail.html', {'application': application})
    except Application.DoesNotExist:
        messages.error(request, 'Заявка не найдена')
        return redirect('main:profile')