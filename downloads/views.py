from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, FileResponse
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from downloads.models import Directory, Files
import re
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
            FileStore = Files.objects.create_file(Directory.objects.get(name=codename), file['id'], file['title'])

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
    auth_url=gauth.GetAuthUrl()
    return HttpResponse(auth_url)

def downloadprovider(request, pk):
    drive=GoogleDrive(gauth)
    fileobj = get_object_or_404(Files, pk=pk)
    download = drive.CreateFile({'id': str(fileobj.fileid)})
    download.GetContentFile(str(fileobj.filename))
    return FileResponse(open(str(fileobj.filename), 'rb'))