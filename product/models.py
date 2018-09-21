import random
import uuid
from datetime import datetime
from random import randint

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timesince import timesince
from django.utils.translation import gettext_lazy as _

from accounts.models import Manufacturer, Location


def validate_code_length(value):
    if len(str(value)) != 3:
        raise ValidationError(
            _('Product Code must have a length of 3 should not start with zeros')
        )


class ProductLine(models.Model):
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    product_name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='images', blank=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    code = models.IntegerField(validators=[validate_code_length])

    class Meta:
        verbose_name = 'Product Line'
        verbose_name_plural = 'Product Lines'

    def __str__(self):
        return "{} ({})".format(self.product_name, self.manufacturer)

    def save(self, *args, **kwargs):
        if self._state.adding:
            filtered_taken_codes = list(range(100, 999))
            for product_line in ProductLine.objects.filter(manufacturer=self.manufacturer):
                filtered_taken_codes.remove(product_line.code)
            self.code = random.choice(filtered_taken_codes)
        super().save(*args, **kwargs)


class Batch(models.Model):
    product_line = models.ForeignKey(ProductLine, on_delete=models.CASCADE)
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    production_date = models.DateField(default=datetime.now)
    expiry_date = models.DateField(default=datetime.now)
    batch_number = models.IntegerField(blank=True, null=True, default=randint(0, 999999))
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    @property
    def manufacturer(self):
        try:
            return self.location.manufacturer_name
        except:
            pass

    def __str__(self):
        return "{} ({})".format(self.batch_number, self.manufacturer)

    class Meta:
        verbose_name = 'Batch Number'
        verbose_name_plural = 'Batch Numbers'


class CodeCollection(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    product_line = models.ForeignKey(ProductLine, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return "{} Codes Generated By: {} ({})".format(self.quantity, self.manufacturer, timesince(self.created))


class ProductCode(models.Model):
    product_code = models.BigIntegerField(unique=True)
    product_line = models.ForeignKey(ProductLine, on_delete=models.CASCADE)
    collection = models.ForeignKey(CodeCollection, on_delete=models.CASCADE, null=True, blank=True)
    batch_number = models.ForeignKey(Batch, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)
    activation_count = models.IntegerField(default=0)

    @property
    def readable_product_code(self):
        code = str(self.product_code)
        return code[0:4] + ' ' + code[4:8] + ' ' + code[8:12] + ' ' + code[12:16]

    def __str__(self):
        return str(self.product_code)

    def rand_string(self, config=None):
        if config is None:
            config = {"length": 5}
        i = 0
        result_string = ""
        while (i < config["length"]):
            result_string += (str)(random.randint(0, 9))

            i += 1
        return (result_string)

    def get_timestamp(self):
        return str(datetime.timestamp(datetime.now()))

    def generate_code(self, company_code, product_line):
        common_code = str(company_code) + str(product_line)
        time_stamp = self.get_timestamp()

        new_code = common_code + self.rand_string({"length": 6}) + time_stamp[14:]
        if new_code.__len__() < 16:
            new_code += ("0" * (16 - len(new_code)))

        return new_code

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.product_code = self.generate_code(self.product_line.manufacturer.code, self.product_line.code)
        super().save(*args, **kwargs)
