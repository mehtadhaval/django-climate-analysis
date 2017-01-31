from django.db import models

# Create your models here.


class Audit(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ActiveObjectsManager(models.Manager):
    def get_queryset(self):
        return super(ActiveObjectsManager, self).get_queryset().filter(is_active=True)


class SoftDelete(models.Model):
    """
    Adds active_objects manager, which filters out inactive records
    """
    is_active = models.BooleanField(default=True)
    objects = models.Manager()
    active_objects = ActiveObjectsManager()

    class Meta:
        abstract = True


class Region(Audit, SoftDelete):
    """
    Region list
    """
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.code, )

    def get_by_natural_key(self, code):
        return Region.objects.get(code=code)
