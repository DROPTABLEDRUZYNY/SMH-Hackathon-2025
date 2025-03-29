from django.contrib import admin
from .models import Activity, Product, TrashPlace

# admin.site.register(Product)
# admin.site.register(TrashPlace)

@admin.register(TrashPlace)
class TrashPlaceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active", "trash_level")
    list_filter = ("is_active", "trash_level")
    search_fields = ("name",)

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("id", "description", "user_full_name", "user_email", "date", "collected_kg", "cleaned_all")
    list_filter = ("cleaned_all", "date")
    search_fields = ("description", "user__first_name", "user__last_name", "user__email")

    def user_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    user_full_name.short_description = "User Full Name"

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = "User Email"