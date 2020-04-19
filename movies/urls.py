from django.urls import path

from .views import MyUploadView

app_name = 'movie'

urlpatterns = [
    path('index/', MyUploadView.as_view(), name='main'),
]
