import json

from django.shortcuts import render, redirect
from django.views.generic import View

from .models import CloudFile
from .forms import UploadVideoFile, UploadPhotoFile, UploadDocFile, UploadArchiveFile
from main.models import UserProfile


class Cloud(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'main/cloud.html')


class CloudVideo(View):
    def get(self, request, *args, **kwargs):
        files = CloudFile.objects.filter(category='video', family=UserProfile.objects.get(user=request.user).family)
        form = UploadVideoFile()
        return render(request, 'main/cloud_video.html', {'files': files, 'form': form})

    def post(self, request, *args, **kwargs):
        form = UploadVideoFile(request.POST, request.FILES)
        files = CloudFile.objects.filter(category='video', family=UserProfile.objects.get(user=request.user).family)
        if form.is_valid():
            new_file = form.save(commit=False)
            new_file.family = UserProfile.objects.get(user=request.user).family
            new_file.owner = request.user
            new_file.category = 'video'
            new_file.save()
        else:
            return render(request, 'main/cloud_video.html', {'files': files, 'form': form})
        return redirect('cloud_video')


class DeleteVideoFile(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_anonymous:
            CloudFile.objects.get(id=kwargs['id']).delete()
        print(request)
        return redirect('cloud_video')

    def post(self, request, *args, **kwargs):
        if not request.user.is_anonymous:
            todel = json.loads(request.POST['data'])
            for i, v in todel.items():
                if v:
                    CloudFile.objects.get(id=i).delete()
        return redirect('cloud_video')


class CloudPhoto(View):
    def get(self, request, *args, **kwargs):
        files = CloudFile.objects.filter(category='photo', family=UserProfile.objects.get(user=request.user).family)
        form = UploadPhotoFile()
        return render(request, 'main/cloud_photo.html', {'files': files, 'form': form})

    def post(self, request, *args, **kwargs):
        form = UploadPhotoFile(request.POST, request.FILES)
        files = CloudFile.objects.filter(category='photo', family=UserProfile.objects.get(user=request.user).family)
        if form.is_valid():
            new_file = form.save(commit=False)
            new_file.family = UserProfile.objects.get(user=request.user).family
            new_file.owner = request.user
            new_file.category = 'photo'
            new_file.save()
        else:
            return render(request, 'main/cloud_photo.html', {'files': files, 'form': form})
        return redirect('cloud_photo')


class DeletePhotoFile(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_anonymous:
            CloudFile.objects.get(id=kwargs['id']).delete()
        print(request)
        return redirect('cloud_photo')

    def post(self, request, *args, **kwargs):
        if not request.user.is_anonymous:
            todel = json.loads(request.POST['data'])
            for i, v in todel.items():
                if v:
                    CloudFile.objects.get(id=i).delete()
        return redirect('cloud_photo')


class CloudDoc(View):
    def get(self, request, *args, **kwargs):
        files = CloudFile.objects.filter(category='doc', family=UserProfile.objects.get(user=request.user).family)
        form = UploadDocFile()
        return render(request, 'main/cloud_doc.html', {'files': files, 'form': form})

    def post(self, request, *args, **kwargs):
        form = UploadDocFile(request.POST, request.FILES)
        files = CloudFile.objects.filter(category='doc', family=UserProfile.objects.get(user=request.user).family)
        if form.is_valid():
            new_file = form.save(commit=False)
            new_file.family = UserProfile.objects.get(user=request.user).family
            new_file.owner = request.user
            new_file.category = 'doc'
            new_file.save()
        else:
            return render(request, 'main/cloud_doc.html', {'files': files, 'form': form})
        return redirect('cloud_doc')


class DeleteDocFile(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_anonymous:
            CloudFile.objects.get(id=kwargs['id']).delete()
        print(request)
        return redirect('cloud_doc')

    def post(self, request, *args, **kwargs):
        if not request.user.is_anonymous:
            todel = json.loads(request.POST['data'])
            for i, v in todel.items():
                if v:
                    CloudFile.objects.get(id=i).delete()
        return redirect('cloud_doc')


class CloudArchive(View):
    def get(self, request, *args, **kwargs):
        files = CloudFile.objects.filter(category='archive', family=UserProfile.objects.get(user=request.user).family)
        form = UploadArchiveFile()
        return render(request, 'main/cloud_archive.html', {'files': files, 'form': form})

    def post(self, request, *args, **kwargs):
        form = UploadArchiveFile(request.POST, request.FILES)
        files = CloudFile.objects.filter(category='archive', family=UserProfile.objects.get(user=request.user).family)
        if form.is_valid():
            new_file = form.save(commit=False)
            new_file.family = UserProfile.objects.get(user=request.user).family
            new_file.owner = request.user
            new_file.category = 'archive'
            new_file.save()
        else:
            return render(request, 'main/cloud_archive.html', {'files': files, 'form': form})
        return redirect('cloud_archive')


class DeleteArchiveFile(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_anonymous:
            CloudFile.objects.get(id=kwargs['id']).delete()
        return redirect('cloud_archive')

    def post(self, request, *args, **kwargs):
        if not request.user.is_anonymous:
            todel = json.loads(request.POST['data'])
            for i, v in todel.items():
                if v:
                    CloudFile.objects.get(id=i).delete()
        return redirect('cloud_archive')
