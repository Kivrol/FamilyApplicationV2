from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('', views.Cloud.as_view(), name='cloud'),
    path('video/', views.CloudVideo.as_view(), name='cloud_video'),
    path('delete/video/<int:id>', views.DeleteVideoFile.as_view(), name='delete_cloud_video'),
    path('delete/video/', csrf_exempt(views.DeleteVideoFile.as_view()), name='delete_cloud_batch_video'),
    path('photo/', views.CloudPhoto.as_view(), name='cloud_photo'),
    path('delete/photo/<int:id>', views.DeletePhotoFile.as_view(), name='delete_cloud_photo'),
    path('delete/photo/', csrf_exempt(views.DeletePhotoFile.as_view()), name='delete_cloud_batch_photo'),
    path('doc/', views.CloudDoc.as_view(), name='cloud_doc'),
    path('delete/doc/<int:id>', views.DeleteDocFile.as_view(), name='delete_cloud_doc'),
    path('delete/doc/', csrf_exempt(views.DeleteDocFile.as_view()), name='delete_cloud_batch_doc'),
    path('archive/', views.CloudArchive.as_view(), name='cloud_archive'),
    path('delete/archive/<int:id>', views.DeleteArchiveFile.as_view(), name='delete_cloud_archive'),
    path('delete/archive/', csrf_exempt(views.DeleteArchiveFile.as_view()), name='delete_cloud_batch_archive'),
    path('storage/', login_required(views.CloudStorage.as_view()), name='cloud_storage'),
    path('thumbnails/', login_required(views.Thumbnailer.as_view()), name='thumbnails'),
]