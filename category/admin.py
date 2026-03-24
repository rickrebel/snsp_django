from django.contrib import admin

from category.models import Topic, StatusControl
from plus.models import Goal


# Register your models here.
@admin.register(StatusControl)
class StatusControlAdmin(admin.ModelAdmin):
    list_display = [
        "public_name", "name", "group", "order",
        "color", "icon", "priority"]
    list_editable = ["order", "color", "icon", "priority"]
    list_filter = ["group"]


@admin.register(Topic, Goal)
class GenericAdmin(admin.ModelAdmin):
    list_display = ["name"]
