from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, TemplateView, ListView, DetailView
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from geopy.geocoders import Nominatim
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from datetime import datetime, timedelta, date
import piexif
import exifread
import folium
from folium import plugins
import branca
from .forms import PostForm
from .models import Post, PostCategory, Area, MountainArea
from django.conf import settings


# トップページのview。地図と、写真のタイル表示をする。
def IndexView(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    m = image_map(request, start_date, end_date)
    queryset = Post.objects.order_by('-posted_at')
    context = {'map': m, 'items':queryset}
    return render(request, 'index.html', context)

# # マイページのview。自分の写真の地図表示とタイル表示をする。
# マイページビューは改良版をしたに作成しました。
# def MypageView(request):
#     start_date = request.GET.get('start_date')
#     end_date = request.GET.get('end_date')
#     m = image_map(start_date, end_date)
#     queryset = Post.objects.filter(user=request.user).order_by('-posted_at')
#     context = {'map': m, 'items':queryset}
#     return render(request, 'mypage.html', context)

# マップのビュー
def ImageMapView(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    m = image_map(start_date, end_date)
    # req = request
    # m = image_map(req)
    return render(request, 'index.html', {'map': m})

# カテゴリー
def CategoryView(request, category_id):
    queryset = Post.objects.filter(category=category_id).order_by('-posted_at')
    info_name = get_object_or_404(PostCategory, id = category_id)
    context = {'items':queryset}
    return render(request, 'index.html', context)

# エリア
def AreaView(request, area_id):
    queryset = Post.objects.filter(area=area_id).order_by('-posted_at')
    info_name = get_object_or_404(Area, id = area_id)
    context = {'items':queryset}
    return render(request, 'index.html', context)

# 山の名前
def MountainView(request, mountain_name_id):
    queryset = Post.objects.filter(mountain_name=mountain_name_id).order_by('-posted_at')
    info_name = get_object_or_404(MountainArea, id = mountain_name_id)
    context = {'items':queryset}
    return render(request, 'index.html', context)

# ユーザー別
def UserView(request, user_id):
    queryset = Post.objects.filter(user=user_id).order_by('-posted_at')
    info_name = get_object_or_404(MountainArea, id = user_id)
    context = {'items':queryset}
    return render(request, 'index.html', context)

#詳細ページ
def photo_detail(request, photo_id):
    photo = get_object_or_404(Post, pk=photo_id)
    return render(request, 'photo_detail.html', {'photo': photo})

# post_photo.htmlから画像をアップロードする際の処理。
# shooting_dateとphoto_latitude、photo_longitudeは下の関数で読み込んで代入する。
def upload_photo(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.shooting_date = get_date_taken(request.FILES['photo'])
            photo.user = request.user
            photo.photo_latitude = get_latitude(request.FILES['photo'])
            photo.photo_longitude = get_longitude(request.FILES['photo'])
            photo.save()
            return render(request, 'post_success.html')
    else:
        form = PostForm()
    return render(request, 'post_photo.html', {'form': form})

# 撮影日をExifから取得するための処理
def get_date_taken(image_file):
    image = Image.open(image_file)
    exif_data = image._getexif()
    if exif_data:
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            if tag_name == 'DateTimeOriginal':
                date_string = value
                date_time_obj = datetime.strptime(date_string, '%Y:%m:%d %H:%M:%S')
                return date_time_obj
    return None

# 緯度をExifから取得する処理
def get_latitude(image_file):
    image = Image.open(image_file)
    exif_data = image._getexif()
    if exif_data:
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            if tag_name == 'GPSInfo':
                gps_info = value
                latitude = gps_info[2][0] + (gps_info[2][1] / 60) + (gps_info[2][2] / 3600)
                if gps_info[3] == 'S':
                    latitude = -latitude
                return latitude
    return None

# 経度をExifから取得する処理
def get_longitude(image_file):
    image = Image.open(image_file)
    exif_data = image._getexif()
    if exif_data:
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            if tag_name == 'GPSInfo':
                gps_info = value
                longitude = gps_info[4][0] + (gps_info[4][1] / 60) + (gps_info[4][2] / 3600)
                if gps_info[5] == 'W':
                    longitude = -longitude
                return longitude
    return None

# Postに保存されている画像と緯度経度から、地図上に表示をする関数
# def image_map(request):
# def image_map(req):
def image_map(request, start_date=date(1990, 1, 1), end_date=date.today(), *args, **kwargs):
    try:
        images = Post.objects.all()
        initial_images = Post.objects.all().order_by('-posted_at')
    # モデルから取ってきたレコードを撮影日でフィルタ
        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date() + timedelta(days=1)
            images = images.filter(shooting_date__range=(start_date, end_date))
    # foliumの地図を設定
        m = folium.Map(
            location =[initial_images[0].photo_latitude, initial_images[0].photo_longitude],
            zoom_start = 14,)
    # レコードから一件取り出して、foliumの地図に表示する
        for image in images:
            try:
                domain = get_current_site(request).domain
                img_url = f"http://{domain}{image.photo.url}"
                # img_url = "http://3.27.9.171:8000"+image.photo.url
                folium.Marker(
                    location = [image.photo_latitude, image.photo_longitude],
                    icon = folium.features.CustomIcon(icon_image=img_url, icon_size = (80,80)),
                    popup = folium.Popup(f"<img src='{image.photo.url}' width='400px'> 撮影日： {image.shooting_date} <br> 山域名： {image.mountain_name} <br> コメント： {image.comment}")
            ).add_to(m)
            except Exception as e:
                print("Error:", e)
    # foliumの地図をhtmlに変換
        m = m._repr_html_()
        return m
    except Exception as e:
        print("Error:", e)
        return None


# マイページのview。自分の写真の地図表示とタイル表示をする。
@login_required
def MypageView(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    mymap = my_image_map(request, start_date, end_date)
    queryset = Post.objects.filter(user=request.user).order_by('-posted_at')
    context = {'map': mymap, 'items':queryset}
    return render(request, 'mypage.html', context)



def my_image_map(request, start_date, end_date, *args, **kwargs):
    try:
        images = Post.objects.filter(user=request.user)
        initial_images = Post.objects.filter(user=request.user).order_by('-posted_at')
        # モデルから取ってきたレコードを撮影日でフィルタ
        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date() + timedelta(days=1)
            images = images.filter(shooting_date__range=(start_date, end_date))
        # foliumの地図を設定
        mymap = folium.Map(
            location =[initial_images[0].photo_latitude, initial_images[0].photo_longitude],
            zoom_start = 14,)
        # レコードから一件取り出して、foliumの地図に表示する
        for image in images:
            try:
                domain = get_current_site(request).domain
                img_url = f"http://{domain}{image.photo.url}"
                # img_url = "http://3.27.9.171:8000"+image.photo.url
                folium.Marker(
                    location = [image.photo_latitude, image.photo_longitude],
                    icon = folium.features.CustomIcon(icon_image=img_url, icon_size = (80,80)),
                    popup = folium.Popup(f"<img src='{image.photo.url}' width='400px'> 撮影日： {image.shooting_date} <br> 山域名： {image.mountain_name} <br> コメント： {image.comment}")
                ).add_to(mymap)
            except Exception as e:
                print("Error:", e)
        # foliumの地図をhtmlに変換
        mymap = mymap._repr_html_()
        return mymap
    except Exception as e:
        print("Error:", e)
        return None

class PostSuccessView(TemplateView):
    template_name = 'post_success.html'