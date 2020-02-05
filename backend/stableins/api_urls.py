from django.urls import path, include

urlpatterns = [
    path('importer/', include('importer.rest_urls')),
    path('quote/', include('quote.rest_urls')),
    path('users/', include('users.rest_urls'))    
]
