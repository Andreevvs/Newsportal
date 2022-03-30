from django.contrib import admin
from django.urls import path, include
from main.views import UserDetailView


urlpatterns = [
    path('', UserDetailView.as_view()),
    path('admin/', admin.site.urls),
    path('news/', include('main.urls')),  # делаем так, чтобы все адреса из нашего приложения (simpleapp/urls.py) сами автоматически подключ
    path('accounts/', include('allauth.urls')),
]
