from django.urls import path
from .views import index, upload_view, manual_view, test_view

urlpatterns = [
    path('', index, name='index'),
    path('upload/', upload_view, name='upload'),
    path('manual/', manual_view, name='manual'),
    path('prueba/', test_view, name='prueba'),
]