from django.contrib import admin

from Product_owner_role.models import User, TaskLevel, TaskLanguage

admin.site.register(User)
admin.site.register(TaskLanguage)
admin.site.register(TaskLevel)

# Register your models here.
