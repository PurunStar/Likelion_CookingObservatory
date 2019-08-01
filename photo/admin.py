from django.contrib import admin
from .models import Photo
from .models import Comment

admin.site.register(Photo)
admin.site.register(Comment)