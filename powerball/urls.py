from django.urls import path, include

from . import views
from .views import HistoryListView, PictureListView


urlpatterns = [
    path('', views.index, name='index'),
    path('prediction/', views.prediction, name='prediction'),
    path('history/', HistoryListView.as_view(), name='history'),
    path('statistic/', views.statistic, name='statistic'),
    path('pictures/', PictureListView.as_view(), name='pictures'),
    path('model/', views.powerball_model, name='model'),
]
