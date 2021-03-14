from rest_framework import serializers
from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'gender',
            'phone_number',
            'password',
            'password2'
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'password2': {'write_only': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Those passwords didn’t match. Try again.'})

        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password2')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'gender',
            'phone_number',
        )
