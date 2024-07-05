# admin.py
from django.contrib import admin
from .models import *

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)

@admin.register(ChannelMember)
class ChannelMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'channel', 'joined_at')
    list_filter = ('channel', 'joined_at')
    search_fields = ('user__username', 'channel__name')
