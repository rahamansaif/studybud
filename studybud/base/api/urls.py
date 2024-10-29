from django.urls import path

from base.api import views


urlpatterns = [
    path('', views.get_routes),
    path('rooms/', views.get_rooms),
    path('rooms/<int:id>/', views.get_room),
    path('topics/', views.get_topics),
    path('topics/create/', views.create_topic),
    path('users/<int:id>/', views.get_user),
]
