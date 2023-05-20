from rest_framework import serializers
from rest_framework import response
from app.models import *
import shutil

class Fileserializer(serializers.ModelSerializer):
    
    class Meta:
        model = Files
        fields = '__all__'


class FileSerializer(serializers.Serializer):
    files = serializers.ListField(
        child = serializers.FileField(max_length = 100000,allow_empty_file = False,use_url=False)
    )

    folder = serializers.CharField(required = False)

    def zippingFile(self,folder):
        shutil.make_archive(f'public/static/zip/{folder}','zip',f'public/static/{folder}')

    def create(self,validated_data):
        folder = Folder.objects.create()
        files = validated_data.pop('files')
        filesObjs = []
        for file in files:
            fileobj = Files.objects.create(folder=folder,file=file)
            filesObjs.append(fileobj)

        self.zippingFile(folder.uid)

        return {'files':{}, "folder" : str(folder.uid)}

