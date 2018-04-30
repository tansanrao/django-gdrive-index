from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from downloads.models import Directory, Files
import re

gauth=GoogleAuth()
drive = None
codename_re = re.compile(r"OFFICIAL-\d{8}-(.*).zip")

def UpdateDB():
    drive=GoogleDrive(gauth)
    file_list = drive.ListFile({'q': "'1eX22TXEwCO9fcNsVuGSzcuG5C3yZbe0C' in parents"}).GetList()
    for file in file_list:
        try:
            codename=codename_re.search(file['title']).group(1)
        except AttributeError:
            continue
        try:
            DirStore = Directory.objects.get(name=codename)
        except Directory.DoesNotExist:
            DirStore = Directory.objects.create_dir(codename)
        try:
            FilesStore = Files.objects.get(fileid=file['id'])
        except Files.DoesNotExist:
            FileStore = Files.objects.create_file(Directory.objects.get(name=codename), file['id'], file['title'])

def index(request):
    UpdateDB()
    list = Directory.objects.all()
    return render(request, 'downloads/index.html', {'list': list})

def device(request):
    UpdateDB()
    list = get_object_or_404(Directory, pk=pk)
    return render(request, 'home/device.html', {'list': list})

def authservice(request):
    gauth.LocalWebserverAuth()
    return HttpResponse("This is the oauth2 page")

