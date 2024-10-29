from django.urls import path, include

from base import views


urlpatterns = [
    path('api/', include('base.api.urls')),
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/<int:id>/', views.user_profile, name='user-profile'),
    path('room/<int:id>/', views.room, name='room'),
    path('create-room/', views.create_room, name='create-room'),
    path('update-room/<int:id>/', views.update_room, name='update-room'),
    path('delete-room/<int:id>/', views.delete_room, name='delete-room'),
    path('delete-message/<int:id>', views.delete_message, name='delete-message'),
    path('edit-message/<int:id>', views.edit_message, name='edit-message'),
    path('update-user/', views.update_user, name='update-user'),
    path('topics/', views.topics_page, name='topics'),
    path('activity/', views.activity_page, name='activity'),
]
