from django.contrib import admin

from .models import Picture

@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ('alt', 'create_date')
    list_filter = ('create_date', 'alt')
