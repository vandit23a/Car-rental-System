from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth import views as auth_views
from rental import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', auth_views.LoginView.as_view(
        template_name='login.html'
    ), name='login'),

    path('home/', include('rental.urls')),

    path('register/', views.register, name='register'),
   path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)