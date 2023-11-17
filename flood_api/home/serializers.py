from rest_framework import serializers
from .models import *


class FloodedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FloodedImage
        exclude = ['created_at', 'updated_at']

class FloodedImagePatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = FloodedImagePatch
        exclude = ['created_at', 'updated_at']