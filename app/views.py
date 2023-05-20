from django.shortcuts import render
from tkinter import E
from rest_framework.views import APIView
from rest_framework.response import Response
from serializer import *

from django.urls import reverse

# Create your views here.

def home(request):
    return render(request,'home.html',{})

def download(request,uid):
    print("********************",uid)
    folder = Folder.objects.get(pk=uid)
    print("********************",folder)
    files = Files.objects.filter(folder=folder)


    return render(request,'download.html',{'folder':folder,'files':files,'uid':uid})


    

   



class HandelFileUpload(APIView):
    def post(self,request):
        try:
            data = request.data
            serializer = FileSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status':200,
                    'message':'Files Uploaded Successfully',
                    'data': serializer.data
                })
            return Response({
                'status': 400,
                'message' : 'Something went wrong',
                'data' : serializer.errors
            })
        except Exception as e:
            print(e) 