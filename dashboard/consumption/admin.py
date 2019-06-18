from django.contrib import admin
from .models import User_data
from .models import Consumption

admin.site.register(User_data)
admin.site.register(Consumption)