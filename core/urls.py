
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns =[  
    
    path('admin/', admin.site.urls),
    path('rest/', include('rest_framework.urls')),
    path('api/',include('movie.api.urls')),
    path('',include('movie.urls')),
    path('accounts/',include('django.contrib.auth.urls')),
]
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)