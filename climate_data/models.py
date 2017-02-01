from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from common.fields import CustomFloatField
from common.models import Audit, Region


class ClimateDataTypeMixin(models.Model):

    TYPE_MAX_TEMP = 'Tmax'
    TYPE_MIN_TEMP = 'Tmin'
    TYPE_MEAN_TEMP = 'Tmean'
    TYPE_SUNSHINE = 'Sunshine'
    TYPE_RAINFALL = 'Rainfall'

    TYPE_CHOICES = (
        (TYPE_MAX_TEMP, _('Max Temp')),
        (TYPE_MIN_TEMP, _('Min Temp')),
        (TYPE_MEAN_TEMP, _('Mean Temp')),
        (TYPE_SUNSHINE, _('Sunshine')),
        (TYPE_RAINFALL, _('Rainfall')),
    )

    type = models.CharField(max_length=32, choices=TYPE_CHOICES)

    class Meta:
        abstract = True


class Request(ClimateDataTypeMixin, Audit):

    STATUS_SUBMITTED = 'submitted'
    STATUS_PROCESSING = 'processing'
    STATUS_COMPLETED = 'completed'
    STATUS_FAILED = 'failed'

    STATUS_CHOICES = (
        (STATUS_SUBMITTED, _('Submitted')),
        (STATUS_PROCESSING, _('Processing')),
        (STATUS_COMPLETED, _('Completed')),
        (STATUS_FAILED, _('Failed')),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='requests')
    region = models.ForeignKey(Region, related_name='requests')
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=STATUS_SUBMITTED)

    def __str__(self):
        return 'Request by {user} for {type} data for {region}'.format(
            user=self.user, type=self.type, region=self.region
        )

    @property
    def url(self):
        return settings.MET_DATA_BASE_URL.format(region=self.region.code, type=self.type)


class ClimateData(ClimateDataTypeMixin, Audit):

    UNIT_DEGREES = 'Degrees C'
    UNIT_TOTAL_HOURS = 'Total Hours'
    UNIT_MM = 'mm'

    UNIT_CHOICES = (
        (UNIT_DEGREES, UNIT_DEGREES),
        (UNIT_TOTAL_HOURS, UNIT_TOTAL_HOURS),
        (UNIT_MM, UNIT_MM)
    )

    TYPE_UNIT_MAP = {
        ClimateDataTypeMixin.TYPE_MAX_TEMP: UNIT_DEGREES,
        ClimateDataTypeMixin.TYPE_MIN_TEMP: UNIT_DEGREES,
        ClimateDataTypeMixin.TYPE_MEAN_TEMP: UNIT_DEGREES,
        ClimateDataTypeMixin.TYPE_SUNSHINE: UNIT_TOTAL_HOURS,
        ClimateDataTypeMixin.TYPE_RAINFALL: UNIT_MM
    }

    region = models.ForeignKey(Region, related_name='climate_data')
    year = models.IntegerField()
    unit = models.CharField(max_length=32, choices=UNIT_CHOICES)
    jan = CustomFloatField(null=True, blank=True)
    feb = CustomFloatField(null=True, blank=True)
    mar = CustomFloatField(null=True, blank=True)
    apr = CustomFloatField(null=True, blank=True)
    may = CustomFloatField(null=True, blank=True)
    jun = CustomFloatField(null=True, blank=True)
    jul = CustomFloatField(null=True, blank=True)
    aug = CustomFloatField(null=True, blank=True)
    sep = CustomFloatField(null=True, blank=True)
    oct = CustomFloatField(null=True, blank=True)
    nov = CustomFloatField(null=True, blank=True)
    dec = CustomFloatField(null=True, blank=True)
    win = CustomFloatField(null=True, blank=True)
    spr = CustomFloatField(null=True, blank=True)
    sum = CustomFloatField(null=True, blank=True)
    aut = CustomFloatField(null=True, blank=True)
    ann = CustomFloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.unit:
            self.unit = self.TYPE_UNIT_MAP.get(self.type)
        super(ClimateData, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Climate Data')
        verbose_name_plural = _('Climate Data')

    def __str__(self):
        return '{type} data for {region} for {year}'.format(type=self.type, region=self.region, year=self.year)


class ClimateTimeSeriesData(ClimateDataTypeMixin, Audit):

    record_date = models.DateField()
    measurement = CustomFloatField(null=True, blank=True)
    region = models.ForeignKey(Region, related_name='timeseries_data')

    def __str__(self):
        return '{type} data for {region} for {timestamp}'.format(type=self.type, region=self.region, timestamp=self.record_date)

    class Meta:
        verbose_name = _('Climate TimeSeries Data')
        verbose_name_plural = _('Climate TimeSeries Data')
