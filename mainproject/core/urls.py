from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('convert', ImageToTextApi.as_view(),name="convert"),
]