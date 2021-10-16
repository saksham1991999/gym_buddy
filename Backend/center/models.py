from django.contrib.gis.db import models


class CenterType(models.Model):
    title = models.CharField(max_length=128)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Center(models.Model):
    type = models.ForeignKey("center.CenterType", null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=256)
    employees = models.ManyToManyField("accounts.User", blank=True, null=True)
    contact_name = models.CharField(max_length=64)
    contact = models.CharField(max_length=16)

    location = models.CharField(max_length=256)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=64)

    point_location = models.PointField(max_length=40)

    def __str__(self):
        return self.name


class CenterImages(models.Model):
    center = models.ForeignKey("center.Center", on_delete=models.CASCADE)
    image = models.ImageField()
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.center

    class Meta:
        verbose_name_plural = "Center Images"