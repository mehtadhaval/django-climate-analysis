from django.contrib import admin

from climate_data.models import Request, ClimateData


class RequestAdmin(admin.ModelAdmin):

    list_display = ('id', 'user', 'region', 'type', 'status', 'updated')
    list_filter = ('region', 'type', 'status')
    search_fields = ('user__email', 'user__name')


class ClimateDataAdmin(admin.ModelAdmin):

    list_display = ('id', 'region', 'type', 'year', 'updated')
    list_filter = ('region', 'type')
    search_fields = ('year',)


admin.site.register(Request, RequestAdmin)
admin.site.register(ClimateData, ClimateDataAdmin)
