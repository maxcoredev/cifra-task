from django.db import models
from django.core.validators import MaxValueValidator


class TruckModel(models.Model):
    """Модель самосвала"""

    name = models.CharField('Название', max_length=255)
    load_capacity = models.IntegerField('Грузоподъёмность (т)', blank=True, null=True)

    def __str__(self):
        return self.name


class Truck(models.Model):
    """Самосвал"""

    tail_number = models.CharField('Бортовой номер', max_length=255)
    model = models.ForeignKey(verbose_name='Модель', to=TruckModel, on_delete=models.RESTRICT)

    def __str__(self):
        return self.tail_number


class Warehouse(models.Model):
    """Склад"""

    name = models.CharField('Название', max_length=255)
    polygon = models.TextField('Полигон (WKT)', blank=True, null=True)
    current_amount = models.IntegerField('Текущее кол-во руды (т)', blank=True, null=True)
    current_sio2 = models.IntegerField('Содержание SiO2 (%)', blank=True, null=True, validators=[MaxValueValidator(100)])
    current_fe = models.IntegerField('Содержание Fe (%)', blank=True, null=True, validators=[MaxValueValidator(100)])

    def __str__(self):
        return self.name


class Shipping(models.Model):
    """Перевозка"""

    truck = models.ForeignKey(verbose_name='Самосвал', to=Truck, on_delete=models.RESTRICT)
    warehouse = models.ForeignKey(verbose_name='Склад', to=Warehouse, on_delete=models.RESTRICT)
    current_load = models.IntegerField('Текущая загрузка (т)', blank=True, null=True)
    current_sio2 = models.IntegerField('Содержание SiO2 (%)', blank=True, null=True, validators=[MaxValueValidator(100)])
    current_fe = models.IntegerField('Содержание Fe (%)', blank=True, null=True, validators=[MaxValueValidator(100)])

    def get_overload(self):
        load_copacity = self.truck.model.load_capacity
        overload = (self.current_load - load_copacity) / load_copacity * 100
        return max(0, round(overload, 3))

    def __str__(self):
        return f'{self.truck} в {self.warehouse}'
