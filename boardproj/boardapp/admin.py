from django.contrib import admin
from .models import Notice, Response


class NoticeAdmin(admin.ModelAdmin):
    list_display = ['title', 'text', 'author', 'category', 'dateCreation']


class ResponseAdmin(admin.ModelAdmin):
    list_display = ['notice', 'author', 'text', 'status', 'dateCreation']


admin.site.register(Notice)
admin.site.register(Response)
