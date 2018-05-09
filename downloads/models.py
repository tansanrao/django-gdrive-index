from django.db import models

class DirectoryManager(models.Manager):
    def create_dir(self, name):
        dir1 = self.create(name=name)
        return dir1

class FilesManager(models.Manager):
    def create_file(self, directory, fileid, filename, download_url, filesize):
        file1 = self.create(directory=directory, fileid=fileid, filename=filename, download_url=download_url, filesize=filesize)
        return file1

class Directory(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    objects = DirectoryManager()

class Files(models.Model):
    directory = models.ForeignKey('Directory', on_delete=models.CASCADE)
    fileid = models.CharField(max_length=200)
    filename = models.CharField(max_length=200)
    download_url = models.TextField()
    filesize = models.IntegerField()
    def __str__(self):
        return self.filename
    objects = FilesManager()

