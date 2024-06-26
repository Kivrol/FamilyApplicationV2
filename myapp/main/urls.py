from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('profile', views.profileView, name='profile'),
    path('/', include('lightlist_auth.urls')),
    path('family/', views.FamilyView.as_view(), name='family'),
    path('add_family', views.CreateFamily.as_view(), name='add_family'),
    path('delete_family/<int:id>', views.DeleteFamily.as_view(), name='delete_family'),
    path('editprofile/', views.EditProfile.as_view(), name='editprofile'),
    path('family_request/', views.JoinFamilyRequestView.as_view(), name='join_family'),
    path('process_request/', views.ProcessRequest.as_view(), name='process_request'),
    path('accept_request/<int:id>', views.AcceptRequest.as_view(), name='accept_request'),
    path('decline_request/<int:id>', views.DeclineRequest.as_view(), name='decline_request'),
    path('productlist/', include('product_list.urls')),
    path('exit_from_group/<int:id>', views.ExitFromGroup.as_view(), name='exit_from_group'),
    path('wishlist/', include('wishlist.urls')),
    path('cloud/', include('cloud.urls')),
    path('calendar/', include('lightlist_calendar.urls')),
    path('change_password/', views.ChangePassword.as_view(), name='change_password'),
    path('kick_from_group/<int:member>', views.KickFromGroup.as_view(), name='kick_from_group'),
]
