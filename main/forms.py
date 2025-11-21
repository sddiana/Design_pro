from django import forms
from .models import Application, Category

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['name', 'description', 'category', 'floor_plan']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Введите название заявки'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Опишите ваши пожелания',
                'rows': 4
            }),
            'category': forms.Select(attrs={
            }),
            'floor_plan': forms.FileInput(attrs={
                'accept': '.jpg,.jpeg,.png,.bmp'
            })
        }
        labels = {
            'name': 'Название заявки',
            'description': 'Описание',
            'category': 'Категория',
            'floor_plan': 'План помещения'
        }
        help_texts = {
            'floor_plan': 'Форматы: JPG, JPEG, PNG, BMP. Максимальный размер: 2MB'
        }

class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status']
        widgets = {
            'status': forms.Select()
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Введите название категории'
            }),
        }
        labels = {
            'name': 'Название категории',
        }