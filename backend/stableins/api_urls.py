from django.urls import path, include

urlpatterns = [
    path('importer/', include('importer.rest_urls')),
    path('users/', include('users.rest_urls'))    
]
