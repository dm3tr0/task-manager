from django.contrib import admin
from django.contrib.auth import get_user_model
from authentication.models import User

user = get_user_model()


admin.register(user)

admin.site.register(User)