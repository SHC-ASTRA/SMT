from django.contrib import admin
from .models import *

admin.site.register(Person)
admin.site.register(Subsystem)
admin.site.register(Assignment)
admin.site.register(PersonData)
admin.site.register(SubsystemData)
