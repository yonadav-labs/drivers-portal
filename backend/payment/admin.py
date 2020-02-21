from django.contrib import admin

from payment.models import StripeCharge

admin.site.register(StripeCharge)