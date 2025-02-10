from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    fields = ['username', 'email', 'bio', 'role']
    list_display = (
        'username',
        'email',
        'bio',
        'role',
    )
    list_filter = (
        'role',
    )
    search_fields = ('username',)
    list_display_links = ('username',)


admin.site.register(User, UserAdmin)
