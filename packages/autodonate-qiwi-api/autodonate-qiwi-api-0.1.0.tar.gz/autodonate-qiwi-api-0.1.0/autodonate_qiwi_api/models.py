from django.db.models import Model, IntegerField


class Payment(Model):
    txId = IntegerField(unique=True)
