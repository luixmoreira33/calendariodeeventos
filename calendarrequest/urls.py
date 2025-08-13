from django.urls import path
from . import views

app_name = 'calendarrequest'

urlpatterns = [
    path('user-request/', views.user_request_view, name='user_request'),
] 