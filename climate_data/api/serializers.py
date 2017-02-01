from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from climate_data import tasks
from climate_data.models import Request
from common.api.serializers import RegionSerializer
from common.models import Region


class RequestSerializer(serializers.ModelSerializer):
    regions = serializers.CharField(write_only=True, required=True, allow_null=False, allow_blank=False)
    types = serializers.CharField(write_only=True, required=True, allow_null=False, allow_blank=False)

    region = RegionSerializer(read_only=True)

    def validate_regions(self, value):
        regions = value.replace(' ', '').split(',')
        all_regions = list(Region.active_objects.all().values_list('id', flat=True))
        regions = [region for region in regions if int(region) in all_regions]
        if not regions:
            raise ValidationError('Please specify regions')
        return regions

    def validate_types(self, value):
        types = value.replace(' ', '').split(',')
        all_types = dict(Request.TYPE_CHOICES).keys()
        types = [type for type in types if type in all_types]
        if not types:
            raise ValidationError('Please specify data types to load')
        return types

    def save(self, **kwargs):
        data = self.validated_data
        for region in data.get('regions'):
            for type in data.get('types'):
                instance = self.Meta.model.objects.create(region_id=region, type=type)
                tasks.process_request.delay(instance.id)

    class Meta:
        model = Request
        read_only_fields = ('status', 'type', 'region', 'created')
        fields = ('id', 'status', 'type', 'region', 'types', 'regions', 'created')
