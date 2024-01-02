from django.contrib import admin
from .models import blogpost
# Register your models here.
@admin.register(blogpost)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id','title','des')