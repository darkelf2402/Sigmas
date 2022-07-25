from django.urls import path
from . import views #as views.py is present in the same file

urlpatterns = [
    path('login/',views.loginPage,name="login"),
    path('logout/',views.logoutPage,name="logout"),
    path('register/',views.registeruser,name="register"),

    path('',views.home,name="home"),
    path('room/<int:pk>',views.room,name="room"),#<str:pk> for for acessing each dictionery element individually
    path('create-room/',views.createroom,name="create-room"),
    path('update-room/<int:pk>/',views.updateroom,name="update-room"),
    path('delete-room/<int:pk>/',views.deleteroom,name="delete-room"),
    path('delete-message/<int:pk>/',views.deletemessage,name="delete-message"),
    path('profile/<int:pk>/',views.userProfile,name="user-profile"),
    path('update-user/',views.updateUser,name="update-user"),
    path('topics/',views.topicsPage,name="topics"),
    path('activity/',views.activityPage,name="activity"),



]
