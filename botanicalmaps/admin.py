from django.contrib import admin
# 管理画面に表示するモデルを設定
from .models import Area, MountainArea, PostCategory, Post

class AreaAdmin(admin.ModelAdmin):
    list_display = ('id', 'area_name')
    list_display_links = ('id', 'area_name')

class MountainAreaAdmin(admin.ModelAdmin):
    list_display = ('id', 'mountain_name')
    list_display_links = ('id', 'mountain_name')

class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category')
    list_display_links = ('id', 'category')

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'shooting_date', 'photo_latitude', 'photo_longitude', 'photo', 'comment', 'area')
    list_display_links = ('id', 'user', 'shooting_date', 'photo_latitude', 'photo_longitude', 'photo', 'comment', 'area')

admin.site.register(Area, AreaAdmin)
admin.site.register(MountainArea, MountainAreaAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Post, PostAdmin)