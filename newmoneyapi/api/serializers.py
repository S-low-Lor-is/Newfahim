from .models import BubbleDataRequestGraph
from rest_framework import serializers

class BubbleDataRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BubbleDataRequestGraph
        fields = '__all__'

