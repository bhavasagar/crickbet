from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    path('rest/api/v1/', include('rest_framework.urls')),            
    path('api/v1/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]