from django.db import models
from django.conf import settings
from datetime import datetime
# Create your models here.
USER_MODEL = settings.AUTH_USER_MODEL


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Product(TimeStampModel):
    name = models.CharField(max_length=80, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    picture = models.CharField(max_length=300, null=True, blank=True)

    price = models.IntegerField(null=True, blank=True)
    amount = models.IntegerField(null=True, blank=True)


class Purchase(TimeStampModel):
    user = models.ForeignKey(USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True,  related_name='user_id')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True, related_name='product_id')
    amount = models.IntegerField(null=True, blank=True)

    def get_time_diff(self):
        now = datetime.timestamp(datetime.now())
        created_at = datetime.timestamp(self.created_at)
        return now - created_at


class Refund(TimeStampModel):
    purchase = models.ForeignKey(Purchase, on_delete=models.SET_NULL, blank=True, null=True)
    admin_confirmed = models.BooleanField(null=True)


