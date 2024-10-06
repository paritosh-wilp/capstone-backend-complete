from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BusinessSignupSerializer
from rest_framework.authtoken.models import Token
from .serializers import BusinessLoginSerializer
from .serializers import CustomerSignupSerializer
from .serializers import CustomerLoginSerializer
from .models import Session, Business, Customer
from rest_framework import generics, status
from .serializers import SessionSerializer, BusinessSerializer, CustomerSerializer

class BusinessSignupView(APIView):
    def post(self, request):
        serializer = BusinessSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Business created successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BusinessLoginView(APIView):
    def post(self, request):
        serializer = BusinessLoginSerializer(data=request.data)
        if serializer.is_valid():
            business = serializer.validated_data['business']

            # # Get or create the auth token for the business #parichan : some issue here
            # token, created = Token.objects.get_or_create(user=business)

            # Return the auth token
            return Response({
                "business_name": business.business_name,
                "business_type": business.business_type,
                "business_id":business.business_id,
                "business_mail":business.business_mail
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerSignupView(APIView):
    def post(self, request):
        serializer = CustomerSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Customer created successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerLoginView(APIView):
    def post(self, request):
        serializer = CustomerLoginSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.validated_data['customer']

            # Get or create the auth token for the customer
            # token, created = Token.objects.get_or_create(user=customer)

            return Response({
                "customer_id": customer.customer_id,
                "customer_name": customer.customer_name,
                "customer_email":customer.customer_mail
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SessionListView(generics.ListAPIView):
    """View to display all sessions with business and customer details."""
    queryset = Session.objects.select_related('business', 'customer').all()
    serializer_class = SessionSerializer


class CreateSessionView(APIView):
    """View to create a new session by business email ID."""
    
    def post(self, request):
        serializer = SessionSerializer(data=request.data)
        if serializer.is_valid():
            business_email = request.data.get('business_email')
            try:
                business = Business.objects.get(business_mail=business_email)
                session = serializer.save(business=business)  # Assign the business to the session
                return Response(SessionSerializer(session).data, status=status.HTTP_201_CREATED)
            except Business.DoesNotExist:
                return Response({"error": "Business with this email does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class UpdateSessionWithCustomerView(generics.UpdateAPIView):
    """
    Update a session based on session UID where customer is null and associate it with a customer.
    """

    serializer_class = SessionSerializer
    
    def put(self, request, session_uid, *args, **kwargs):

        # Check if customer_email is provided in the request
        customer_email = request.data.get("customer_email")

        try:
            # First try to find the session where customer is null
            session = Session.objects.get(session_uid=session_uid, customer__isnull=True)
        except Session.DoesNotExist:
             # If no such session is found, try to find the session with the given customer_email
            try:
                session = Session.objects.get(session_uid=session_uid, customer__customer_mail=customer_email)
            except Session.DoesNotExist:
                 # If both attempts fail, return an error response
                return Response(
                     {"error": "Session not found / Session already mapped to another customer / Customer is not null."},
                status=status.HTTP_404_NOT_FOUND
                )


        # Check if customer_email is provided in the requests
        customer_email = request.data.get("customer_email")
        if not customer_email:
            return Response({"error": "Customer email is required to associate with the session."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve the customer by email
            customer = Customer.objects.get(customer_mail=customer_email)
        except Customer.DoesNotExist:
            return Response({"error": "Customer with this email does not exist."},
                            status=status.HTTP_404_NOT_FOUND)

        # Update the session with the customer and the validated data
        serializer = self.get_serializer(session, data=request.data)
        if serializer.is_valid():
            # Associate the customer with the session
            session.customer = customer
            serializer.save()  # Save the updated session with the associated customer
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)