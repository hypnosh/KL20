from django.urls import path
from . import views

urlpatterns = [
    path('', views.main),
    path('level/<int:id>/', views.Level),
]
