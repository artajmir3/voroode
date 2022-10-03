from django.contrib import admin
from herokuapp.models import *

# Register your models here.


class SusAdmin(admin.ModelAdmin):
    pass


class StateAdmin(admin.ModelAdmin):
    pass


admin.site.register(Suspects, SusAdmin)
admin.site.register(State, StateAdmin)

