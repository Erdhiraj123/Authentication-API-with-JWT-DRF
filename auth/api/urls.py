from django.urls import path
from api.views import UserRegistration, LoginUser,UserProfile


urlpatterns = [
    path('reg/',UserRegistration.as_view() ,name='register'),
    path('login/',LoginUser.as_view() ,name='login'),
    path('profile/',UserProfile.as_view()),
  

]
