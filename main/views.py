from pyexpat.errors import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Application, Category
from .forms import ApplicationForm, CategoryForm
from django.contrib.auth.decorators import user_passes_test


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
    applications = Application.objects.filter(client=request.user).order_by('-created_at')
    
    status_filter = request.GET.get('status', '')
    
    if status_filter:
        applications = applications.filter(status=status_filter)
    
    context = {
        'applications': applications,
    }
    return render(request, 'main/profile.html', context)

@login_required
def create_application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.client = request.user
            application.save()
            return redirect('main:profile')
    else:
        form = ApplicationForm()
    
    return render(request, 'main/create_application.html', {
        'form': form
    })

@login_required
def application_detail(request, application_id):
    try:
        application = Application.objects.get(id=application_id, client=request.user)
    except Application.DoesNotExist:
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

@admin_required
def change_application_status(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')

        if new_status in [choice[0] for choice in Application.STATUS_CHOICES]:
            
            if application.status == 'new' and new_status == 'completed':
                if request.FILES.get('design_image'):
                    application.design_image = request.FILES['design_image']
                    application.status = new_status
                    application.save()
            
            elif application.status == 'new' and new_status == 'in_progress':
                comment = request.POST.get('comment', '').strip()
                if comment:
                    application.comment = comment
                    application.status = new_status
                    application.save()
            
            else:
                application.status = new_status
                application.save()
    
    return redirect('main:admin_applications')
                

@admin_required
def manage_categories(request):
    categories = Category.objects.all().order_by('name')
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
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
    
    Application.objects.filter(category=category).delete()
    category.delete()
    
    return redirect('main:manage_categories')

@login_required
def delete_application(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    
    if request.method == 'POST':
        application.delete()
    
    return redirect('main:application_detail')

