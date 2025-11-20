from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Application
from .forms import ApplicationForm
from django.contrib.auth.decorators import user_passes_test
from .forms import ApplicationStatusForm, CategoryForm
from .models import Category
from django.shortcuts import get_object_or_404

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
    return render(request, 'main/profile.html', context)


@login_required
def application_detail(request, application_id):
    try:
        application = Application.objects.get(id=application_id, client=request.user)
    except Application.DoesNotExist:
        messages.error(request, 'Заявка не найдена')
        return redirect('main:profile')
    
    return render(request, 'main/application_detail.html', {
        'application': application
    })


def admin_required(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_superuser,
        login_url='/'
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

@admin_required
def admin_applications(request):
    applications = Application.objects.all().order_by('-created_at')
    
    status_filter = request.GET.get('status')
    if status_filter:
        applications = applications.filter(status=status_filter)
    
    return render(request, 'main/admin_applications.html', {
        'applications': applications
    })

from django.shortcuts import redirect
from django.contrib import messages

@admin_required
def change_application_status(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in [choice[0] for choice in Application.STATUS_CHOICES]:
            application.status = new_status
            application.save()
            messages.success(request, f'Статус заявки "{application.name}" изменен на {application.get_status_display()}')
    
    return redirect('main:admin_applications')

@admin_required
def manage_categories(request):
    categories = Category.objects.all()
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Категория добавлена')
            return redirect('main:manage_categories')
    else:
        form = CategoryForm()
    
    return render(request, 'main/manage_categories.html', {
        'categories': categories,
        'form': form
    })

@admin_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    if category.application_set.exists():
        messages.error(request, 'Нельзя удалить категорию, с которой связаны заявки')
    else:
        category.delete()
        messages.success(request, 'Категория удалена')
    
    return redirect('main:manage_categories')