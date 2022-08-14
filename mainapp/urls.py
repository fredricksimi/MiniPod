from django.urls import path
from . import views

app_name='mainapp'
urlpatterns = [
    path('',views.home_view, name='home'),
    path('podcast-details/<str:id>/', views.podcast_details, name='podcast-details'),
]