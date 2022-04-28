from django.db import models


class DailyPriceModel(models.Model):
    date = models.DateField()
    symbol = models.CharField(max_length=20)
    prevClose = models.DecimalField(max_digits=7,decimal_places=2)
    open = models.DecimalField(max_digits=7,decimal_places=2)
    high = models.DecimalField(max_digits=7,decimal_places=2)
    low = models.DecimalField(max_digits=7,decimal_places=2)
    last = models.DecimalField(max_digits=7,decimal_places=2)
    close = models.DecimalField(max_digits=7,decimal_places=2)
    vwap = models.DecimalField(max_digits=7,decimal_places=2)
    volume = models.IntegerField()
    # turnover = models.IntegerField()

    def __str__(self):
        return self.symbol + " "+str(self.date)


