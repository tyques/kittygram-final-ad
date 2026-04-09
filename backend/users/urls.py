from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('list/', views.users_list_view, name='list'),
    path('<int:user_id>/', views.user_detail_view, name='detail'),
    path('<int:user_id>/edit/', views.edit_profile_view, name='edit'),
    path('<int:user_id>/change-password/', views.change_password_view, name='change_password'),
    path('<int:user_id>/share/', views.share_profile_view, name='share'),
]
