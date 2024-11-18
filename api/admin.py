from django.contrib import admin
from .models import *

admin.site.register(TrukItUser)
admin.site.register(Customer)
admin.site.register(Driver)
admin.site.register(DriverInsurance)
admin.site.register(DriverTruck)
admin.site.register(DriverTruckTrailer)
admin.site.register(DeliveryItem)
admin.site.register(DeliveryEquipment)
admin.site.register(DeliveryTransaction)
