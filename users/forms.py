from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re

class LoginUserForm(forms.Form):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль',widget=forms.PasswordInput())

class RegisterUserForm(forms.ModelForm):

    full_name = forms.CharField(
        label='ФИО',
        max_length=100,
        required=True,
    )

    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput,
        required=True
    )
    
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput,
        required=True
    )
    
    agree_to_terms = forms.BooleanField(
        label='',
        required=True,
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'email']
        labels = {
            'email': 'E-mail',
            'username': 'Логин',
        }
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        if not username:
            raise ValidationError('Логин обязателен для заполнения.')
        
        pattern = r'^[a-zA-Z\-]+$'
        if not re.match(pattern, username):
            raise ValidationError('Логин должен содержать только латинские буквы и дефис.')
        
        if User.objects.filter(username=username).exists():
            raise ValidationError('Пользователь с таким логином уже существует.')
        
        return username

    def clean_full_name(self):
            full_name = self.cleaned_data.get('full_name')
            if not full_name:
                raise ValidationError('ФИО обязательно для заполнения.')
            
            pattern = r'^[а-яА-ЯёЁ\s\-]+$'
            if not re.match(pattern, full_name):
                raise ValidationError('ФИО должно содержать только кириллические буквы, дефис и пробелы.')
            
            parts = full_name.strip().split()
            if len(parts) < 2:
                raise ValidationError('Введите хотя бы имя и фамилию.')
            return full_name
    
    def clean_agree_to_terms(self):
        agree_to_terms = self.cleaned_data.get('agree_to_terms')
        if not agree_to_terms:
            raise ValidationError('Вы должны согласиться на обработку персональных данных.')
        return agree_to_terms
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Такой E-mail уже существует!")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        
        full_name = self.cleaned_data.get('full_name', '')
        if full_name:
            parts = full_name.strip().split()
            if len(parts) >= 2:
                user.last_name = parts[0] 
                user.first_name = ' '.join(parts[1:])
        
        if commit:
            user.save()
        return user
