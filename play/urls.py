from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ContentView, {'slug': 'main-page'}, name='main_page'),
    path('play/', views.Play),
    path('login/', views.Login),
    path('oauth/', views.GmailLogin),
    path('logout/', views.Logout),
    path('accounts/', include('allauth.urls')),
    path('level/<int:id>/', views.LevelView, name='level_id'),
    path('level/<slug:slug>/', views.LevelView, name='level_slug'),
    path('content/<slug:slug>/', views.ContentView, name='CMS_Content'),
]
