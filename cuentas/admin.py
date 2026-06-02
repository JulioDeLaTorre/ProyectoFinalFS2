
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
# Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'nombre_completo',
        'telefono',
        'is_staff',
        'is_active',
    )

    search_fields = (
        'username',
        'email',
        'nombre_completo',
        'telefono',
    )

    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {
            'fields': (
                'nombre_completo',
                'telefono',
            )
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información adicional', {
            'fields': (
                'nombre_completo',
                'telefono',
            )
        }),
    )