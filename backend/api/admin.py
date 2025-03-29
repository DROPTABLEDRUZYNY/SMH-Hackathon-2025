from django.contrib import admin
from .models import Activity, Product, TrashPlace

#admin.site.register(Product)
admin.site.register(Activity)
# admin.site.register(TrashPlace)



@admin.register(TrashPlace)
class TrashPlaceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active", "trash_level")
    list_filter = ("is_active", "trash_level")
    search_fields = ("name",)  