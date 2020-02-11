from django.contrib import admin
from django.contrib.admin import AdminSite

class StableAdminSite(AdminSite):
    site_header = "Stable Admin Portal"
    site_title = "Stable Admin Portal"
    index_title = "Welcome to Stable Admin Portal"

stable_admin = StableAdminSite(name='stable_admin')