from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AbstractUserAdmin
from django.contrib.auth import get_user_model

from .forms import UserChangeForm, UserCreationForm

# Register your models here.

User = get_user_model()

@admin.register(User)
class UserAdmin(AbstractUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = ((User, {"fields": ('name',),}),) + AbstractUserAdmin.fieldsets
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]

    
