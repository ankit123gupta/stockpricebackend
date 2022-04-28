from django.contrib import admin
from .models import *

# customize admin panel
class DailyPriceAdmin(admin.ModelAdmin):
    ordering = ['-date']
    list_display = ('symbol', 'date')
    list_filter = ['date','symbol']
    search_fields = ['date','symbol']
    actions_on_bottom=True
admin.site.register(DailyPriceModel,DailyPriceAdmin)
