from django.db import models
from django.contrib.auth.models import User

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

