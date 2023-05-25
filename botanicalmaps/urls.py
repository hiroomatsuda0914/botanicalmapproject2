from django.urls import path
from . import views

app_name = 'botanicalmaps'

urlpatterns = [
    path('',views.IndexView, name='index'),
    path('mypage/',views.MypageView, name='mypage'),
    # path('mypage_2/',views.MypageView2, name='mypage'),
    # path('', views.image_map, name='index'),
    path('post_photo/', views.upload_photo, name ='post_photo'),
    path('image_map/', views.ImageMapView, name='image_map'),
    path('photo_detail/<int:photo_id>/', views.photo_detail, name='photo_detail'),
    path('photo_cat/<int:category_id>', views.CategoryView, name = 'photo_cat'),
    path('area/<int:area_id>', views.AreaView, name = 'area'),
    path('mountain_name/<int:mountain_name_id>', views.MountainView, name = 'mountain_name'),
    path('user/<int:user_id>', views.UserView, name = 'user'),
    path('post_done/', views.PostSuccessView.as_view(), name = 'post_done'),
]