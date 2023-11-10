from django.db import models

# Create your models here.
class BubbleDataRequestGraph(models.Model):
    user_name = models.CharField(max_length=100)
    type_of_graph = models.IntegerField()

class Email_Set_Device(models.Model):
    email = models.CharField(max_length=250)
    device_model = models.CharField(max_length=250)

