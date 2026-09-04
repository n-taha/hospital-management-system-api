from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import my_view
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from users.views import UserLoginView, UserRegisterView

urlpatterns = [
    path("", my_view , name="my-view"),
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path('api/v1/', include('api.urls')),
    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/auth/login/', UserLoginView.as_view(), name='obtain_token'),
    path('api/v1/auth/register/', UserRegisterView.as_view(), name='register_user'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root = settings.MEDIA_ROOT
    )

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
