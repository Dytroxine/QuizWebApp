from django.contrib import admin
from django.urls import path, include  # Подключаем include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from main_page.views import authenticate_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('quiz/', include('quiz.urls')),  # Включаем маршруты quiz через include
    path('', include('main_page.urls')),
    path('authenticate/', authenticate_user, name='authenticate_user'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
