from django.contrib import admin

# Register your models here.
from .models import (
    Member,
    Post
)

admin.site.register(Member)
admin.site.register(Post)