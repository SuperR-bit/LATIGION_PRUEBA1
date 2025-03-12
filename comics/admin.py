from django.contrib import admin

from .models import Chapter, Comic

# Register your models here.

admin.site.register(Comic)
admin.site.register(Chapter)