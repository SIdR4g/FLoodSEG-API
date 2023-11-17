from django.db import models
from django.contrib.auth.models import User 


import uuid

class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, editable = False, default = uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class FloodedImage(BaseModel):
    user = models.ForeignKey(User, on_delete =models.CASCADE, related_name = "FloodedImage")
    title = models.CharField(max_length = 500, default="")

    # coordinates = models.TextField()
    captured_image = models.ImageField(upload_to = "image")
    segmented_image = models.ImageField(upload_to = "mask",default=None)

    prediction_data = models.JSONField(default=dict)

    def __str__(self) -> str:
        return self.title
    
class FloodedImagePatch(BaseModel):
    user = models.ForeignKey(User, on_delete =models.CASCADE, related_name = "FloodedImagePatch")
    patch_code = models.CharField(max_length = 100, default="")
    image_id = models.CharField(max_length = 100, default="")

    captured_image = models.ImageField(upload_to = "image")
    segmented_image = models.ImageField(upload_to = "mask",default=None)
    prediction_data = models.JSONField(default=dict)

    def __str__(self) -> str:
        return (self.patch_code+"_"+self.image_id)