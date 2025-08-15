from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,AcrossMenaUser
# Register your models here.



@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'phone', 'is_staff', 'is_verified')

    # Fieldsets for adding and changing a user
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone', 'image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),  # You can use 'collapse' here to hide fields by default
            'fields': ('username', 'email', 'phone', 'password1', 'password2', 'image') 
        }),
    )

    # Make the username and email fields searchable
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone')
    ordering = ('username',)

    # Optionally, define which fields are editable in admin
    readonly_fields = ('last_login', 'date_joined',)



@admin.register(AcrossMenaUser)
class CustomUserAdmin(admin.ModelAdmin):
    model = AcrossMenaUser
    list_display = ['user','country']
    ordering = ('user',)


