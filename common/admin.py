from django.contrib import admin

from common.models import Region


class RegionAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'code')


admin.site.register(Region, RegionAdmin)
