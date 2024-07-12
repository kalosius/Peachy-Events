
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('events.urls')),
]

# Configure admin titles
admin.site.site_header = "Peachy Boys Administration"
admin.site.site_title = "Peachy Boys Administration"
admin.site.index_title = "Welcome To The Peachy Administration Area"


