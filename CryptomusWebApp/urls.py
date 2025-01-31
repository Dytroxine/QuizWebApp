from django.contrib import admin
from django.urls import path, include  # Подключаем include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # Включаем маршруты accounts через include
    path('quiz/', include('quiz.urls')),  # Включаем маршруты quiz через include
    path('', include('main_page.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
