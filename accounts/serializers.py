from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.fields import EmailField
from rest_framework.serializers import ModelSerializer, CharField, Serializer
from rest_framework_simplejwt import serializers
from .models import Profile


class LoginSerializer(Serializer):
    email = EmailField()
    password = CharField(style={'input_type': 'password'}, write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                username=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid email or password')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Must include email and password')


class UserRegistrationSerializer(ModelSerializer):
    password = CharField(write_only=True, validators=[validate_password])
    password_confirm = CharField(write_only=True)
    phone_number = CharField(write_only=True, required=False)
    about = CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'password_confirm', 'phone_number', 'about')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        email = validated_data.get('email')
        phone = validated_data.pop('phone_number', None)
        about = validated_data.pop('about', None)

        username = email.split('@')[0]

        user = User.objects.create_user(username=username, **validated_data)
        Profile.objects.create(user=user, phone_number=phone, about=about)
        return user
