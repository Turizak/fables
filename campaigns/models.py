import uuid

from django.db import models


class Account(models.Model):
    index = models.AutoField(
        null=False,
        primary_key=True,
    )
    uuid = models.UUIDField(null=False, default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(null=False, max_length=100)
    last_updated = models.DateTimeField(null=False, auto_now=True)
    created_date = models.DateTimeField(null=False, auto_now_add=True)
    deleted = models.BooleanField(null=False, default=False)

    class Meta:
        db_table = "account"

    def __str__(self):
        return self.username


class Campaign(models.Model):
    index = models.AutoField(
        null=False,
        primary_key=True,
    )
    uuid = models.UUIDField(null=False, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(null=False, max_length=100)
    account_uuid = models.ForeignKey(
        Account, on_delete=models.CASCADE, to_field="uuid", db_column="account_uuid"
    )
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    last_updated = models.DateTimeField(null=False, auto_now=True)
    created_date = models.DateTimeField(null=False, auto_now_add=True)
    deleted = models.BooleanField(null=False, default=False)

    class Meta:
        db_table = "campaign"

    def __str__(self):
        return self.name
