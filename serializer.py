from rest_framework import serializers
from rest_framework import response
from app.models import *
import shutil


class UserSerializer(serializers.Serializer):
    username = serializers.EmailField()
    password = serializers.CharField()

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

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
        user = self.context.get('user')
        name = self.context.get('name')

        # Check if the user is available in the context
        if not user:
            raise serializers.ValidationError("User not found in the context")
        
        folder = Folder.objects.create(user=user)
        files = validated_data.pop('files')
        filesObjs = []
        for file in files:
            fileobj = Files.objects.create(folder=folder,file=file)
            filesObjs.append(fileobj)

        self.zippingFile(folder.uid)
        link = Link(user = user,name = name,link = "http://localhost:8000/download/"+str(folder.uid),folder=folder)
        link.save()

        return {'files':{}, "folder" : str(folder.uid)}


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['date','link','name']