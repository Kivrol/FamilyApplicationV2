from django.urls import path
from . import views

urlpatterns = [
        path('', views.WishListMainPage.as_view(), name='wishlist'),
        path('<int:user>', views.WishListUser.as_view(), name='wishlistuser'),
        path('delete/<int:id>', views.WishDelete.as_view(), name='delete_wish'),
        path('change_active/<int:id>', views.WishChangeActive.as_view(), name='wish_change_active'),
        path('change_wish/<int:pk>', views.WishEdit.as_view(), name='wish_change_wish'),
]