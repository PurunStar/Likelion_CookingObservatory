
from django.contrib import admin
from django.urls import path, include
import accounts.views
import curriculum.views
import menu.views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', menu.views.home, name="home"),
    path('notice/', menu.views.notice, name='notice'),
    path('intro/', menu.views.intro, name='intro'),
    path('accounts/', include('accounts.urls')),
    path('curriculum/', include('curriculum.urls')),
    path('photo/', include('photo.urls')),    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
