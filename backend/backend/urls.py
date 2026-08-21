from django.contrib import admin
from django.urls import path, include
from knowledge.views import index_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='home'),
    path('api/', include('knowledge.urls')),
]
