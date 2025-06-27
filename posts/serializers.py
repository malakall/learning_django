from rest_framework import serializers
from yatube.models import Group, Comment, User


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["post", "author", "text", "created"]
        read_only_fields = ["author", "created"] # поля будут приходить не от юзера


class GroupSerializer(serializers.ModelSerializer):
    character_quantity = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True) 
    class Meta:
        model = Group
        fields = ["id",'name', 'description', 'user_name', 'image', "comments", "character_quantity"]
    
    def get_character_quantity(self, obj): # функция для подсчета длины значения объекта модели (в нашем случае поля name)
        return len(obj.name)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "password", "email"]

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data.get("email", "")
        )