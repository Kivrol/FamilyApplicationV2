from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_exempt

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
    path('decline_request/<int:id>', views.DeclineRequest.as_view(), name='decline_request'),
    path('product_list/', views.ProductList.as_view(), name='product_list'),
    path('delete_product/<int:id>', views.DeleteProduct.as_view(), name='delete_product'),
    path('exit_from_group/<int:id>', views.ExitFromGroup.as_view(), name='exit_from_group'),
    path('wishlist/<int:user>', views.WishListUser.as_view(), name='wishlistuser'),
    path('wishlist/', views.WishListMainPage.as_view(), name='wishlist'),
    path('wishlist/delete/<int:id>', views.WishDelete.as_view(), name='delete_wish'),
    path('wishlist/change_active/<int:id>', views.WishChangeActive.as_view(), name='wish_change_active'),
    path('wishlist/change_wish/<int:pk>', views.WishEdit.as_view(), name='wish_change_wish'),
    path('cloud/', views.Cloud.as_view(), name='cloud'),
    path('cloud/video/', views.CloudVideo.as_view(), name='cloud_video'),
    path('cloud/delete/<int:id>', views.DeleteFile.as_view(), name='delete_cloud'),
    path('cloud/delete/', csrf_exempt(views.DeleteFile.as_view()), name='delete_cloud_batch'),

]
