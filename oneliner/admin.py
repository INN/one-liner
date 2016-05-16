from django.contrib import admin
from oneliner.models import Organization, Services as Service


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    pass


@admin.register(Service)
class ServicesAdmin(admin.ModelAdmin):
    pass
