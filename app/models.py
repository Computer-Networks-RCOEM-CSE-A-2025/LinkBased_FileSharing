from django.db import models
import uuid
from uuid import uuid4
from statistics import mode
import os
from django.contrib.auth.models import User

# Create your models here.

class Folder(models.Model):
    user = models.ForeignKey(User,null=False,on_delete=models.CASCADE)
    uid = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    createdAt = models.DateField(auto_now=True)

def getUploadPath(instance,filename):
    return os.path.join(str(instance.folder.uid) , filename)



class Files(models.Model):
    folder = models.ForeignKey(Folder,on_delete=models.CASCADE)
    file = models.FileField(upload_to=getUploadPath)
    createdAt = models.DateField(auto_now=True)

class Link(models.Model):
    user = models.ForeignKey(User,null=False,on_delete=models.CASCADE)
    link = models.TextField()
    folder = models.OneToOneField(Folder,null=False,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
