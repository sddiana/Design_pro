from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import LoginUserForm
from .forms import RegisterUserForm

def login_user(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('main:profile'))
            else:
                form.add_error(None, 'Неверный логин или пароль')
    else:
        form = LoginUserForm()
    return render(request, 'users/login.html', {'form': form})
 
 
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': "Регистрация"}
    success_url = reverse_lazy('main:profile') 

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object) 
        return response