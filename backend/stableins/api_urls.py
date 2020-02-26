from django.urls import path, include

urlpatterns = [
    path('policy/', include('policy.rest_urls')),
    path('importer/', include('importer.rest_urls')),
    path('quote/', include('quote.rest_urls')),
    path('users/', include('users.rest_urls')),
    path('hellosign/', include('hellosign_app.urls')),
    path('', include('base.rest_urls')),    
]
