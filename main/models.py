from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import os

class Category(models.Model):
    name = models.CharField(
        max_length=100, 
        verbose_name='Название категории',
        unique=True
    )
    description = models.TextField(
        verbose_name='Описание категории',
        blank=True
    )

    class Meta:
            verbose_name = 'Категория'
            verbose_name_plural = 'Категории'
            ordering = ['name']

    def __str__(self):
        return self.name

def validate_image_file(value):
    valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError(
            f'Недопустимый формат файла. Разрешены: {", ".join(valid_extensions)}'
        )
    
    # Проверка размера файла (2MB)
    max_size = 2 * 1024 * 1024  
    if value.size > max_size:
        raise ValidationError('Максимальный размер файла - 2MB')
    
class Application(models.Model):    
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'Принято в работу'),
        ('completed', 'Выполнено'),
    ]

    name = models.CharField(
        max_length=200,
        verbose_name='Название заявки'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name='Категория'
    )
    floor_plan = models.ImageField(
        upload_to='floor_plans/%Y/%m/%d/',
        verbose_name='План помещения',
        validators=[validate_image_file]
    )

    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name='Клиент'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    
   
    class Meta:
            verbose_name = 'Заявка'
            verbose_name_plural = 'Заявки'
            ordering = ['-created_at']

def __str__(self):
    return f"{self.name} - {self.client.username}"  

def save(self, *args, **kwargs):
        if not self.pk:
            self.status = 'new'
        self.full_clean()
        super().save(*args, **kwargs)