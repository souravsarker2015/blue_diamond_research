from apps.core.models import BaseModel
from django.db import models


class Company(BaseModel):
    name = models.CharField(max_length=254)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=254, null=True, blank=True)
    address = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'company'
