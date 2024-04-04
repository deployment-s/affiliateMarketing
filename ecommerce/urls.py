from django.urls import path
from . import views


urlpatterns = [
 path('', views.Homepage, name='homepage'),
 path('AboutUsPage/', views.AboutUsPage, name='AboutUsPage'),
 path('contactUs/', views.contactUsView, name='contactUs'),
 path('privacy_Policy/', views.privacy_Policy, name='privacy_Policy'),
 path('meet_the_team/', views.meet_the_team, name='meet_the_team'),
 path('about_us/', views.about_us, name='about_us'),
 path('ajax_contact_form', views.ajax_contact_form, name='ajax_contact_form'),
 path('shop/', views.Shop, name='shop'),
 path('signup/', views.SignUp, name='signUp'),
 path('my_Account/', views.My_account, name='my_Account'),
 path('edit_my-account/<int:pk>/', views.edit_my_account, name='edit_my_account'),


]