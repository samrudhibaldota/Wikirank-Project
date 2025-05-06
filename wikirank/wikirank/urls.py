from django.contrib import admin
from django.urls import path
from search.views import search_articles

urlpatterns = [
    path('admin/', admin.site.urls),
    path('search/', search_articles),  # New search endpoint
]

