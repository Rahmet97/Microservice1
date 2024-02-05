from rest_framework import serializers
from django.contrib.auth.views import get_user_model

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password', 'password2')

    def create(self, validated_data):
        if validated_data['password'] == validated_data['password2']:
            if User.objects.filter(username=validated_data['username']).exists():
                raise serializers.ValidationError('Username already exists!')
            if User.objects.filter(email=validated_data['email']).exists():
                raise serializers.ValidationError('Email already exists!')
            validated_data.pop('password2')
            user = User.objects.create_user(**validated_data)
            return user
        else:
            raise serializers.ValidationError('Passwords are not same!')


class UserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username')
