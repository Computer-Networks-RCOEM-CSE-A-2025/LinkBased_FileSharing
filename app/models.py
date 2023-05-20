from django.db import models
import uuid
from uuid import uuid4
from statistics import mode
import os
# Create your models here.
class Folder(models.Model):
    uid = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    createdAt = models.DateField(auto_now=True)

def getUploadPath(instance,filename):
    return os.path.join(str(instance.folder.uid) , filename)



class Files(models.Model):
    folder = models.ForeignKey(Folder,on_delete=models.CASCADE)
    file = models.FileField(upload_to=getUploadPath)
    createdAt = models.DateField(auto_now=True)
