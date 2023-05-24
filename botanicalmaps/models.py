from django.db import models
from accounts.models import CustomUser

#エリアのテーブル（山域の親カテゴリー）
class Area(models.Model):
    area_name = models.CharField(verbose_name='エリア', max_length=20)
    def __str__(self):
        return self.area_name

# 山域のテーブル
class MountainArea(models.Model):
    mountain_name = models.CharField(verbose_name ='山域', max_length =20)
    parent = models.ForeignKey(Area, verbose_name = 'エリア', on_delete=models.PROTECT)
    mountain_latitude = models.FloatField(verbose_name ='山の緯度', blank = True, null = True)
    mountain_longitude = models.FloatField(verbose_name ='山の経度', blank = True, null = True)
    def __str__(self):
        return self.mountain_name

# 投稿写真カテゴリーのテーブル（満開、紅葉、、、等）
class PostCategory(models.Model):
    category = models.CharField(verbose_name = 'カテゴリ', max_length = 30)
    icon = models.ImageField(verbose_name='アイコン', upload_to='icons', blank = True, null = True)
    def __str__(self):
        return self.category

# 植物名のテーブル
class PlantName(models.Model):
    plantname = models.CharField(verbose_name='植物名', max_length = 30)
    def __str__(self):
        return self.plantname

# 投稿内容のテーブル
class Post(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name = 'ユーザー名', on_delete = models.CASCADE)
    posted_at = models.DateTimeField(verbose_name ='投稿日時', auto_now_add = True)
    shooting_date = models.DateTimeField(verbose_name ='撮影日')
    photo_latitude = models.FloatField(verbose_name ='写真の緯度')
    photo_longitude = models.FloatField(verbose_name ='写真の経度',)
    photo = models.ImageField(verbose_name ='写真',upload_to = 'photos')
    comment = models.TextField(verbose_name = 'コメント', blank = True, null = True)
    area = models.ForeignKey(Area, verbose_name = 'エリア', on_delete = models.PROTECT)
    mountain_name = models.ForeignKey(MountainArea, verbose_name = '山域', on_delete = models.SET_NULL, blank = True, null = True)
    category = models.ForeignKey(PostCategory,verbose_name = 'カテゴリ', on_delete = models.SET_NULL, blank = True, null = True)
    plantname = models.ManyToManyField(PlantName, verbose_name = '植物名', blank = True)
    def __str__(self):
        return self.comment