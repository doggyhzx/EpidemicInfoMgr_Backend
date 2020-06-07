from django.urls import path
from . import views

urlpatterns = [
    path('News/', views.news_list)
    path('News/<int:newsid>/',views.view_news)
]
