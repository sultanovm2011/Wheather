from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from cities_light.models import City
from ajax_select.fields import AutoCompleteSelectMultipleField
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

class Cities(models.Model):
    city = models.ForeignKey(City, related_name='cities', on_delete=models.PROTECT)
    weather = models.CharField(max_length=2000, db_index=True, verbose_name="weather")
    date = models.DateTimeField(auto_now_add=True)
    Latitude = models.DecimalField(max_digits=10, decimal_places=6,verbose_name="Latitude",  blank=True, null=True, validators=[MinValueValidator(Decimal('-90.0')), MaxValueValidator(Decimal('90.0'))])
    Longitude = models.DecimalField(max_digits=10, decimal_places=6, verbose_name="Longitude",  blank=True, null=True, validators=[MinValueValidator(Decimal('-180.0')), MaxValueValidator(Decimal('180.0'))])


    def __unicode__(self):
        return u'%s %i %s %s %s %s' % ("#", self.id,"weather", self.weather, "date" )


    def get_absolute_url(self):
         return reverse('setings:ShowWeather', args=[self.id])
