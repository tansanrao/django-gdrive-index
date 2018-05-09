from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from downloads.models import Directory, Files
import re
import io
import json
from wsgiref.util import FileWrapper

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
            fetcher = drive.CreateFile({'id': file['id']})
            fetcher.FetchMetadata()
            download_url = fetcher.metadata.get('downloadUrl')
            FileStore = Files.objects.create_file(Directory.objects.get(name=codename), file['id'], file['title'], download_url[:-8], file['fileSize'])

def index(request):
    UpdateDB()
    list = Directory.objects.all()
    return render(request, 'downloads/index.html', {'list': list})

def device(request, pk):
    UpdateDB()
    codename=Directory.objects.get(pk=pk)
    list = Files.objects.filter(directory = codename)
    print(codename)
    return render(request, 'downloads/deviceindex.html', {'list': list, 'directory': codename})

def authservice(request):
    ClearDB()
    auth_url=gauth.GetAuthUrl()
    gauth.LocalWebserverAuth()
    return HttpResponse(auth_url)

def api(request):
    UpdateDB()
    directories = Directory.objects.all()
    jsonobject = []
    for dir in directories:
        files = Files.objects.filter(directory = dir)
        filelist = []
        for file in files:
            filelist.append({
                'filename' : str(file.filename),
                'size' : int(file.filesize),
                'download_url': str(file.download_url),
            })
        
        jsonobject.append({
            'codename': str(dir.name),
            'files': filelist,
        })
    return JsonResponse(jsonobject, safe=False)

def ClearDB():
    Files.objects.all().delete()
    Directory.objects.all().delete()