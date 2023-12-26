from ckeditor_uploader.views import upload, browse

from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import never_cache

from accounts.forms import register
from accounts.views import confirm_registration
from boardapp import views
from boardapp.views import profile




urlpatterns = [
    path('admin/', admin.site.urls),
    # path('admin/', include('django.contrib.flatpages.urls')),
    # path('pages/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('accounts/signup/', register, name='register'),
    path('accounts/register/', confirm_registration, name='confirm'),
    path('profile/', profile, name='profile'),
    path('accounts/', include('allauth.urls')),
    path('', include('boardapp.urls')),
]
