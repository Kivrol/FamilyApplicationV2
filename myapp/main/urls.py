from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='calendar'),
    path('profile', views.profileView, name='profile'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.view_logout, name='logout'),
    path('family/', views.FamilyView.as_view(), name='family'),
    path('add_family', views.CreateFamily.as_view(), name='add_family'),
    path('delete_family/<int:id>', views.DeleteFamily.as_view(), name='delete_family'),
    path('editprofile/', views.EditProfile.as_view(), name='editprofile'),
    path('family_request/', views.JoinFamilyRequestView.as_view(), name='join_family'),
    path('process_request/', views.ProcessRequest.as_view(), name='process_request'),
    path('accept_request/<int:id>', views.AcceptRequest.as_view(), name='accept_request'),
    path('process_request/<int:id>', views.ProcessRequest.as_view(), name='process_request'),
    path('product_list/', views.ProductList.as_view(), name='product_list'),
    path('delete_product/<int:id>', views.DeleteProduct.as_view(), name='delete_product'),
]
