"""
Модель валюты.
"""
from django.db import models

class Currency(models.Model):
    """
    Модель валюты.

    Хранит информацию о валюте, такую как код, название и текущий курс.
    """
    code = models.CharField(max_length=3, unique=True, verbose_name="Код валюты")
    name = models.CharField(max_length=50, verbose_name="Название валюты")
    rate = models.DecimalField(max_digits=20, decimal_places=6, verbose_name="Курс по отношению к базовой валюте")
    change = models.CharField(max_length=10, verbose_name="Изменение курса", blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        db_table = 'currencies'
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"