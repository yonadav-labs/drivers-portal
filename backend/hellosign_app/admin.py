from django.contrib import admin

from hellosign_app.models import HelloSignSignatureRequest

admin.site.register(HelloSignSignatureRequest, admin.ModelAdmin)
