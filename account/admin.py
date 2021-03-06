from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# UserAdmin.fieldsets += (
#     ("فیلدهای خاص من", {'fields': ('is_author', 'spacial_user')}),
# )

UserAdmin.fieldsets[2][1]['fields'] = (
    'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'is_author', 'special_user')
UserAdmin.list_display += ('is_author', 'is_special_user')
admin.site.register(User, UserAdmin)
