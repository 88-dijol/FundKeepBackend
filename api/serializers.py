from rest_framework import serializers

from django.contrib.auth.models import User

from api.models import Expense,Income



class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model=User
        
        fields=["id","username","email","password"]

        read_only_fields=["id"]


    #serializer.save--nn to encrypt the password we use create method with prameters(self,validated dat)---also method overriding is taking place in this create method
    def create(self,validated_data):

        return User.objects.create_user(**validated_data)    #**unpack cheyan
    


class ExpenseSerializer(serializers.ModelSerializer):

    owner=serializers.StringRelatedField(read_only=True)

    class Meta:

        model=Expense

        fields="__all__"

        read_only_fields=["id","owner","created_date","updated_date","is_active"]



class Incomeserializer(serializers.ModelSerializer):

    owner=serializers.StringRelatedField(read_only=True)  #to convert the owner_id to a string value(username)

    class Meta:

        model=Income

        fields="__all__"

        read_only_fields=["id","owner","created_date","updated_date","is_active"]