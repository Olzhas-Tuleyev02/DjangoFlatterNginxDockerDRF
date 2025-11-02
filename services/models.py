from django.db import models
from django.conf import settings

class Category(models.Model):
    """Модель категорий услуг"""
    name = models.CharField(max_length=255, unique=True, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="URL-слаг")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    # Для вложенности категорий (например, "Декор" -> "Шары")
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name="Родительская категория"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name

class Service(models.Model):
    """Модель Услуги, предоставляемой исполнителем."""
    provider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="services",
        verbose_name="Исполнитель"
    )
    name = models.CharField(max_length=255, verbose_name="Название услуги")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="URL-слаг")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='services',
        verbose_name="Категория"
    )
    city = models.CharField(max_length=100, verbose_name="Город")
    available_dates = models.TextField(
        verbose_name="Доступные даты",
        help_text="Перечислите доступные даты, например, в формате YYYY-MM-DD, YYYY-MM-DD"
    )
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, verbose_name="Рейтинг")
    image = models.ImageField(upload_to='services/', blank=True, null=True, verbose_name="Изображение")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.provider.username})"
