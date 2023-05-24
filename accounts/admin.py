from django.contrib import admin
from .models import CustomUser

# 管理サイトの表示項目を設定
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')
    list_display_liknks = ('id', 'username', 'email')

# 管理サイトにデータベース（CustomUserとCustomUserAdmin）を登録
admin.site.register(CustomUser, CustomUserAdmin)
