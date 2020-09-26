from django.contrib import admin

from app.models import TruckModel, Truck, Warehouse, Shipping


@admin.register(TruckModel)
class TruckModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Truck)
class TruckAdmin(admin.ModelAdmin):
    pass


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    pass


@admin.register(Shipping)
class ShippingAdmin(admin.ModelAdmin):
    pass
