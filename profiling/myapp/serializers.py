from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    
    class Meta:
        model = UserProfile
        fields = ['username', 'fullname', 'email', 'password', 'profile_picture', 'email_verified']
        
    def create(self, validate_data):
        user = UserProfile(
            email=validate_data['email'],
            username=validate_data['username'],
            fullname=validate_data['fullname'],
            profile_picture=validate_data.get('profile_picture', None)
        )
        user.set_password(validate_data['password'])
        user.save()
        return user
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.fullname = validated_data.get('fullname', instance.fullname)
        instance.email = validated_data.get('email', instance.email)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.email_verified = validated_data.get('email_verified', instance.email_verified)

        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)

        instance.save()
        return instance