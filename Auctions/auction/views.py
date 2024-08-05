from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from  rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from django.contrib.auth  import authenticate
from rest_framework.decorators import authentication_classes,permission_classes
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated

