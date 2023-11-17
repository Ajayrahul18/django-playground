from datetime import datetime, timedelta
from django.shortcuts import render, get_object_or_404
from .serializers import *
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
# Create your views here.
@api_view(['POST'])
def register_user(request):
    data = request.data
    serializer = SignUpSerializer(data=data)
    if serializer.is_valid():
        if not User.objects.filter(username = data['email']).exists():
            user = User.objects.create(
                first_name = data['first_name'],
                last_name = data['last_name'],
                email = data['email'],
                username = data['email'],
                password = make_password(data['password'])
            )
            return Response({'message': 'User Created Succesfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'User already Exicst'}, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def current_user(request):
    user = UserSerializer(request.user)
    return Response(user.data)

@api_view(['PUT'])
def update_user(request):
    data = request.data
    user = request.user

    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.email = data['email']
    if user.password != "":
        user.password = make_password(data['password'])
    user.save()
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

def get_current_host(request):
    protocol = request.is_secure() and 'https' or 'https'
    host = request.get_host()
    return '{protocal}://{host}'.format(protocol=protocol, host=host)

@api_view(['POST'])
def forgot_password(request):
    data = request.data
    user = get_object_or_404(User, email=data['email'])
    token = get_random_string(40)
    expire_data = datetime.now() + timedelta(minutes=30)
    user.profile.reset_password_token = token
    user.profile.reset_password_expire = expire_data
    user.profile.save()
    host = get_current_host(request)

    link = "{host}api/rest_password/{token}".format(host=host, token=token)
    body = "Your password reset line is: {link}".format(link=link)

    send_mail(
        "Password reset for ecom",
        body,
        "noreply@eshop.com",
        [data['eamil']]
    )
    return Response({"Detail":"Password reset email sent to: {email}".format(email=data['email'])})

