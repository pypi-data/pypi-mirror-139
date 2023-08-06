from django.db.models import Model, IntegerField


class Payment(Model):
    tx_id = IntegerField(unique=True)
