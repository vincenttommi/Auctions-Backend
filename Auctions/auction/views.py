from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from django.contrib.auth import authenticate 
from rest_framework.decorators import authentication_classes,permission_classes 
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import AuctionItem
from .serializers import AuctionItemSerializer
from rest_framework.parsers import JSONParser






@api_view(['POST'])
def signup(request):
    #creating an instance of userSerializer class and assigning it request
    serializer  = UserSerializer(data=request.data)
    #checking if the serializer is valid
    if serializer.is_valid():
        #saving the serialized data
        user  = serializer.save()

        token  = Token.objects.create(user=user)
        #creating token for user who signs up 

        data = {
            "user":serializer.data,
            "token":token.key
        }

        return Response(data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    




@api_view(['POST'])
def login(request):
    data = request.data
    authenticate_user = authenticate(username=data['username'], password=data['password'])
    
    if authenticate_user is not None:
        user = User.objects.get(username=data['username'])
        serializer = UserSerializer(user)
        response_data = {
            "user": serializer.data,
        }
        
        token, created = Token.objects.get_or_create(user=user)
        response_data['token'] = token.key
        
        return Response(response_data, status=status.HTTP_200_OK)
    else:
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)



api_view(['GET'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes(['IsAuthenticated'])
def TestView(request):
    return Response({'message':'authenticated well'})



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    request.auth.delete()  # Assuming you want to delete the token
    return Response({"message": "Logged out successfully"}, status=204)




@api_view(['GET'])
def list_auction_items(request):
    items = AuctionItem.objects.all().order_by('id')
    serializer = AuctionItemSerializer(items, many=True)
    return Response(serializer.data)




@api_view(['POST'])
def create_auction_item(request):
    #allows us to convert python objects into JSON strings
    data  = JSONParser().parse(request)
    #checking if an item with same name exists
    if AuctionItem.objects.filter(name=data.get('name')).exists():
        return Response({'error': 'Item with this name already exists.'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = AuctionItemSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['PUT'])
def  update_auction_item(request,pk):
    try:
        item  = AuctionItem.objects.get(pk=pk)
    except AuctionItem.DoesNotExist:
        return Response({'error':'item not found'}, status=status.HTTP_404_NOT_FOUND)
    

    data  =  JSONParser().parse(request)
    #allows us to convert python objects into JSON strings
    serializer  = AuctionItemSerializer(item, data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
def delete_auction_item(request,pk):
    try:
        item = AuctionItem.objects.get(pk=pk)
    except AuctionItem.DoesNotExist:
        return Response({'error':'Item not found'}, status=status.HTTP_404_NOT_FOUND)   
    item.delete()
    return Response({'message':'Item deleted succcessfully'}, status=status.HTTP_204_NO_CONTENT)     