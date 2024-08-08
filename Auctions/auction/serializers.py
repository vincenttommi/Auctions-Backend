from  django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import AuctionItem



class UserSerializer(ModelSerializer):
    class Meta:
        model  = User
        fields  = ['id', 'username', 'email', 'password']
        extra_kwargs  = {'password':{'write_only':True}}



    def create(self, validated_data):
        #creating a user with create_user method to handle password hashing
        email = validated_data.get('email','')   #provides a default value if a user is missing
        user  = User.objects.create_user(
            username=validated_data['username'],
            email=email,
            password=validated_data['password']
        )
        return user
    




class AuctionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model  = AuctionItem
        fields = '__all__'