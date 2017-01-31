from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

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
    status = models.CharField(max_length=32, choices=STATUS_CHOICES)

    def __str__(self):
        return 'Request by {user} for {type} data for {region}'.format(
            user=self.user, type=self.type, region=self.region
        )


class ClimateData(ClimateDataTypeMixin, Audit):

    UNIT_DEGREES = 'Degrees C'
    UNIT_TOTAL_HOURS = 'Total Hours'
    UNIT_MM = 'mm'

    UNIT_CHOICES = (
        (UNIT_DEGREES, UNIT_DEGREES),
        (UNIT_TOTAL_HOURS, UNIT_DEGREES),
        (UNIT_MM, UNIT_DEGREES)
    )

    TYPE_UNIT_MAP = {
        ClimateDataTypeMixin.TYPE_MAX_TEMP: UNIT_DEGREES,
        ClimateDataTypeMixin.TYPE_MIN_TEMP: UNIT_DEGREES,
        ClimateDataTypeMixin.TYPE_MEAN_TEMP: UNIT_DEGREES,
        ClimateDataTypeMixin.TYPE_SUNSHINE: UNIT_TOTAL_HOURS,
        ClimateDataTypeMixin.TYPE_RAINFALL: UNIT_MM
    }

    region = models.ForeignKey(Region)
    year = models.IntegerField()
    unit = models.CharField(max_length=32, choices=UNIT_CHOICES)
    jan = models.FloatField(null=True, blank=True)
    feb = models.FloatField(null=True, blank=True)
    mar = models.FloatField(null=True, blank=True)
    apr = models.FloatField(null=True, blank=True)
    may = models.FloatField(null=True, blank=True)
    jun = models.FloatField(null=True, blank=True)
    jul = models.FloatField(null=True, blank=True)
    aug = models.FloatField(null=True, blank=True)
    sep = models.FloatField(null=True, blank=True)
    oct = models.FloatField(null=True, blank=True)
    nov = models.FloatField(null=True, blank=True)
    dec = models.FloatField(null=True, blank=True)
    win = models.FloatField(null=True, blank=True)
    spr = models.FloatField(null=True, blank=True)
    sum = models.FloatField(null=True, blank=True)
    aut = models.FloatField(null=True, blank=True)
    ann = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.unit:
            self.unit = self.TYPE_UNIT_MAP.get(self.type)
        super(ClimateData, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Climate Data')
        verbose_name_plural = _('Climate Data')

    def __str__(self):
        return '{type} data for {region} for {year}'.format(type=self.type, region=self.region, year=self.year)
