from rest_framework.serializers import ModelSerializer
from .models import ImageHistory

class ImageHistorySerializer(ModelSerializer):
    class Meta:
        model = ImageHistory
        fields = "__all__"