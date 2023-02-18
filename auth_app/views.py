from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import *
from rest_framework import generics, status


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    # permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


def index(request):
    return render(request, 'login_test.html')


@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def get_logged_in_user_data(request):
    if request.user.is_authenticated:
        serializer = UserSerializer(instance=request.user, many=False)
        return Response(serializer.data)


@api_view(['POST'])
def sign_up(request):
    serializer = RegisterSerializer(data=request.data, many=False)
    if serializer.is_valid(raise_exception=True):
        new_user = serializer.create(serializer.validated_data)
        return Response(data=UserSerializer(instance=new_user, many=False).data)


@api_view(['POST'])
def log_in(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response()
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)



# @csrf_exempt
@api_view(['POST'])
def log_out(request):
    if request.user.is_authenticated:
        logout(request)
    return Response()


@api_view(['GET'])
def get_version(request):
    return Response(data={'version': 1.0})