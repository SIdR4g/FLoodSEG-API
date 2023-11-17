from django.urls import path
from home.views import *

urlpatterns = [
    path('upload/', DroneView.as_view()),
    path('upload_patch/', PatchView.as_view()),
]