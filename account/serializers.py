from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from rest_framework import serializers
import re
import phonenumbers
import pycountry

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=True)
    country = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile_type', 'phone_number', 'country', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        # Check if first_name and last_name fields are provided
        if not data.get('first_name'):
            raise ValidationError('First name is required.')

        if not data.get('last_name'):
            raise ValidationError('Last name is required.')

        return data

    def validate_phone_number(self, value):
        try:
            parsed_number = phonenumbers.parse(value, None)
            if not phonenumbers.is_valid_number(parsed_number):
                raise ValidationError('Invalid phone number.')
        except phonenumbers.phonenumberutil.NumberParseException:
            raise ValidationError('Invalid phone number.')

        # Check if the phone number already exists
        if User.objects.filter(phone_number=value).exists():
            raise ValidationError('Phone number already exists.')

        return value

    def validate_country(self, value):
        # Check if the provided country is a valid country name

        valid_countries = [country.name for country in pycountry.countries] # List of valid country names

        if value not in valid_countries:
            raise ValidationError('Invalid country.')
        
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise ValidationError('Password must be at least 8 characters long.')

        if value.isalpha():
            raise ValidationError('Password must contain at least one digit.')

        if not re.search(r'[a-z]', value):
            raise ValidationError('Password must contain at least one lowercase letter.')

        if not re.search(r'[A-Z]', value):
            raise ValidationError('Password must contain at least one uppercase letter.')

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValidationError('Password must contain at least one special character.')

        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user