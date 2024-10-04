from rest_framework import serializers
from .models import Business, Customer, Session

from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token

class BusinessSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Business
        fields = ['business_id', 'business_name', 'business_type', 'business_mail', 'password']

    def create(self, validated_data):
        # Remove password from validated_data so we can handle it securely
        password = validated_data.pop('password')

        # Create the business instance without saving it to the DB
        business = Business(**validated_data)

        # Set the hashed password
        business.set_password(password)

        # Save the business instance to the database
        business.save()

        return business


class BusinessLoginSerializer(serializers.Serializer):
    business_mail = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        # Get the business email and password from the request data
        business_mail = data.get('business_mail')
        password = data.get('password')

        # Find the business by email
        try:
            business = Business.objects.get(business_mail=business_mail)
        except Business.DoesNotExist:
            raise serializers.ValidationError("Business with this email does not exist.")

        # Check if the password is correct
        if not business.check_password(password):
            raise serializers.ValidationError("Incorrect password.")
        
        # Everything is valid, return the business instance
        data['business'] = business
        return data



class CustomerSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Customer
        fields = ['customer_id', 'customer_name', 'customer_mail', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')

        # Create a new customer instance
        customer = Customer(**validated_data)
        customer.set_password(password)
        customer.save()

        return customer


class CustomerLoginSerializer(serializers.Serializer):
    customer_mail = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        customer_mail = data.get('customer_mail')
        password = data.get('password')

        try:
            customer = Customer.objects.get(customer_mail=customer_mail)
        except Customer.DoesNotExist:
            raise serializers.ValidationError("Customer with this email does not exist.")

        if not customer.check_password(password):
            raise serializers.ValidationError("Incorrect password.")

        data['customer'] = customer
        return data


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'business', 'session_date', 'timeslot', 'session_status', 'customer']


