auth_user_model_file_content = """from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass
"""


auth_user_admin_file_content = """from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


admin.site.register(User, UserAdmin)
"""
