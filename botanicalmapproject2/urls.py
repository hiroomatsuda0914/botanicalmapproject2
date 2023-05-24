from django.contrib import admin
# include関数をインポート
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # django管理サイトの名前空間はadmin
    # path('admin/', admin.site.urls),
    # 公開対応。アドミンのurlを変更する
    path('matsuda_admin/', admin.site.urls),
    # accountsアプリへのリダイレクト(accounts appのurlsのファイル名を指定)
    path('', include('accounts.urls')),
    # botanicalmapsアプリへのリダイレクト(botanicalmaps appのurlsのファイル名を指定)
    path('', include('botanicalmaps.urls')),
    # 以下は、パスワードリセットの仕組み
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name = "password_reset.html"), name = 'password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name = "password_reset_sent.html"), name = 'password_reset_done'),
    path('reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name = "password_reset_form.html"), name = 'password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name = "password_reset_done.html"), name = 'password_reset_complete'),
]

urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
