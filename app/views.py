from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from serializer import *
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import jwt
import datetime
from .models import *

# Create your views here.

def test(request):
    return render(request, 'test.html', {})

@api_view(['GET'])
def home(request):
    # Get the token from the request's cookies
    token = request.COOKIES.get('token')

    if not token:
        return Response({'status': 400, 'message': 'Authentication failed'})

    try:
        # Verify the JWT token and decode the payload
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])

        # Retrieve the user based on the user ID in the payload
        user = User.objects.filter(id=payload['id']).first()

        if user:
            return Response({'status': 200, 'message': 'home page', 'user': user.username})
        else:
            return Response({'status': 400, 'message': 'User not found'})

    except jwt.ExpiredSignatureError:
        return Response({'status': 400, 'message': 'Token has expired'})

    except jwt.DecodeError:
        return Response({'status': 400, 'message': 'Token is invalid'})

    except Exception as e:
        return Response({'status': 400, 'message': 'Token Error: ' + str(e)})


def download(request, uid):
    try:
        # print("********************", uid)
        folder = Folder.objects.get(pk=uid)
        # print("********************", folder)
        files = Files.objects.filter(folder=folder)
        return render(request, 'download.html', {'folder': folder, 'files': files, 'uid': uid})
    except:
        return render(request,'NotFound.html')

class UserAPI(APIView):
    def post(self, request):
        data = request.data
        try:
            serializer = RegisterSerializer(data=data)
            if serializer.is_valid():
                user = User.objects.create_user(username=serializer.data['username'], email=serializer.data['email'])
                user.set_password(serializer.data['password'])
                user.save()
                return Response({'status': 200, 'message': 'Registration Successful'})
            return Response({'status': 400, 'message': 'Error in Registration'})
        except Exception as e:
            return Response({'status': 400, 'message': 'Error: ' + str(e)})


@api_view(['POST'])
def HandleFileUpload(request):
    token = request.query_params.get('t[token]')
    name = request.query_params.get('t[name]') 
    # print(token)
    # print(name) 

    if not token:
        return Response({'status': 400, 'message': 'Authentication failed'})

    try:
        # Verify the JWT token and decode the payload
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])

        # Retrieve the user based on the user ID in the payload
        user = User.objects.filter(id=payload['id']).first()

        if user:
            pass
        else:
            return Response({'status': 400, 'message': 'User not found'})

    except jwt.ExpiredSignatureError:
        return Response({'status': 400, 'message': 'Token has expired'})

    except jwt.DecodeError:
        return Response({'status': 400, 'message': 'Token is invalid'})

    except Exception as e:
        print('Error')


    try:
        files = request.data.getlist('files') 
        # print(files)
        serializer = FileSerializer(data={'files': files}, context={'user': user,'name':name})
        
        if serializer.is_valid():
            serializer.save()
            
            return Response({
                        'status': 200,
                        'message': 'Files Uploaded Successfully',
                        'data': serializer.data
                    })
        return Response({
                    'status': 400,
                    'message': 'Something went wrong',
                    'data': serializer.errors
                })
    except Exception as e:
        return Response({'status': 400, 'message': 'Error: ' + str(e)})


class LoginAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            username = data.get('username')
            password = data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:

                # Create a JWT token
                payload = {
                    'id': user.id,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1440),
                    'iat': datetime.datetime.utcnow()
                }

                token = jwt.encode(payload, 'secret', algorithm='HS256')
                response = Response({'status': 200, 'token': token})

                # Set the token as a cookie in the response
                response.set_cookie(key='token', value=token)
                return response
            else:
                return Response({'status': 400, 'message': 'Invalid Credentials'})

        except Exception as e:
            return Response({'status': 400, 'message': 'Error: ' + str(e)})

@api_view(['GET'])
def Logout(request):
    try:
        response = Response({'status': 200, 'message': 'Logging-Out'})
        response.delete_cookie('token')
        return response
    except:
        return Response({'status':400,'message':'Error in Logging-Out'})

@api_view(['POST'])
def getLinks(request):
    token = request.data['token']

    if not token:
        return Response({'status': 400, 'message': 'Authentication failed'})

    try:
        # Verify the JWT token and decode the payload
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])

        # Retrieve the user based on the user ID in the payload
        user = User.objects.filter(id=payload['id']).first()

        if user:
            pass
        else:
            return Response({'status': 400, 'message': 'User not found'})

    except jwt.ExpiredSignatureError:
        return Response({'status': 400, 'message': 'Token has expired'})

    except jwt.DecodeError:
        return Response({'status': 400, 'message': 'Token is invalid'})

    except Exception as e:
        print('Error')
    
    try:
        links = Link.objects.filter(user=user)
        serializer = LinkSerializer(links,many=True)
        
        return Response({'status':200,'data':serializer.data})
    except:
        return Response({'status':400,'message':'error in links extraction'})


@api_view(['POST'])
def deleteLink(request):
    link = request.data['link']
    try:
        if link is not "":
            # linkObj = Link.objects.get(link=link)
            url_parts = link.split('/')
            last_part = url_parts[-1]

            folder = Folder.objects.get(uid=last_part)
            folder.delete()
            return Response({'status':200,'message':'Deletion Successful'})
        return Response({'status':400,'message':'Invalid String'})
    except:
        return Response({'status':400,'message':'Error in Link Deletion'})