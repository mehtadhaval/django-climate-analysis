from django.contrib import admin

from climate_data import tasks
from climate_data.models import Request, ClimateData


class RequestAdmin(admin.ModelAdmin):
    readonly_fields = ('user', )
    list_display = ('id', 'user', 'region', 'type', 'status', 'updated')
    list_filter = ('region', 'type', 'status')
    search_fields = ('user__email', 'user__name')

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.user = request.user
        super(RequestAdmin, self).save_model(request, obj, form, change)

    def process_request(self, request, queryset):
        for request in queryset:
            request.status = request.STATUS_SUBMITTED
            request.save()
            tasks.process_request.delay(request.id)

    process_request.short_description = 'Process Request'

    actions = [process_request]


class ClimateDataAdmin(admin.ModelAdmin):

    list_display = ('id', 'region', 'type', 'year', 'updated')
    list_filter = ('region', 'type')
    search_fields = ('year',)


admin.site.register(Request, RequestAdmin)
admin.site.register(ClimateData, ClimateDataAdmin)
