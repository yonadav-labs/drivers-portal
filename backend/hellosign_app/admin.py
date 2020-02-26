from django.contrib import admin

from hellosign_app.models import HelloSignSignatureRequest, HelloSignSavedCallback

admin.site.register(HelloSignSignatureRequest, admin.ModelAdmin)
admin.site.register(HelloSignSavedCallback)