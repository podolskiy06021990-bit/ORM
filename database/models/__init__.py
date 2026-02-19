"""
Модели базы данных с использованием Django ORM для PostgreSQL.

Один файл — одна модель. Импорт из пакета сохраняет совместимость:
  from database.models import Customer, Product, Order, OrderItem
"""
from .Customer import Currency


__all__ = ['Currency']
