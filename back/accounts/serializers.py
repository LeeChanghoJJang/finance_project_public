from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
# from django.contrib.auth.models import User
from .models import User

class CustomRegisterSerializer(RegisterSerializer):
    like_bank = serializers.CharField(required=True, allow_blank=False, max_length=100)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['like_bank'] = self.validated_data.get('like_bank', '')
        return data

    def save(self, request):
        user = super().save(request)
        user.like_bank = self.validated_data.get('like_bank', '')
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'like_bank']

class UserPKSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username',)