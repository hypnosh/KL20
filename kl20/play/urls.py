from django.urls import path
from . import views

urlpatterns = [
    path('', views.main),
    path('login/', views.Login),
    path('logout/', views.Logout),
    path('level/<int:id>/', views.LevelView, name='level_id'),
    path('level/<slug:slug>/', views.LevelView, name='level_slug'),
]
