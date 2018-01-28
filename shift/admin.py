from django.contrib import admin
from .models import Shift, Locker, Manager, Marketer

# Register your models here.
admin.site.register(Shift)
admin.site.register(Locker)
admin.site.register(Manager)
admin.site.register(Marketer)