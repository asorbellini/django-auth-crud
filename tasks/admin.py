from django.contrib import admin
from .models import Tasks
# Register your models here.
class TasksAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

admin.site.register(Tasks, TasksAdmin)