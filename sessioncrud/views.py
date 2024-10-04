from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BusinessSignupSerializer
from rest_framework.authtoken.models import Token
from .serializers import BusinessLoginSerializer
from .serializers import CustomerSignupSerializer
from .serializers import CustomerLoginSerializer
from .models import Session
from .serializers import SessionSerializer

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



class SessionListCreateView(APIView):
    def get(self, request):
        sessions = Session.objects.all()
        serializer = SessionSerializer(sessions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SessionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SessionDetailView(APIView):
    def get(self, request, pk):
        try:
            session = Session.objects.get(pk=pk)
        except Session.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = SessionSerializer(session)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            session = Session.objects.get(pk=pk)
        except Session.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = SessionSerializer(session, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SessionByBusinessView(APIView):
    def get(self, request, business_id):
        # Get all sessions for a specific business
        sessions = Session.objects.filter(business_id=business_id)
        
        # Check if there are sessions for the provided business ID
        if not sessions.exists():
            return Response({"detail": "No sessions found for this business."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = SessionSerializer(sessions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateSessionByBusinessView(APIView):
    def put(self, request, business_id, session_id=None):
        """
        Updates session(s) by business.
        - If session_id is provided, only that session will be updated.
        - If session_id is not provided, all sessions for the business will be updated.
        """

        # If session_id is provided, update a specific session
        if session_id:
            try:
                session = Session.objects.get(business_id=business_id, id=session_id)
            except Session.DoesNotExist:
                return Response({"detail": "Session not found for this business."}, status=status.HTTP_404_NOT_FOUND)

            serializer = SessionSerializer(session, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Otherwise, update all sessions for the business
        sessions = Session.objects.filter(business_id=business_id)
        if not sessions.exists():
            return Response({"detail": "No sessions found for this business."}, status=status.HTTP_404_NOT_FOUND)

        data = request.data  # Expect the same fields for each session
        for session in sessions:
            serializer = SessionSerializer(session, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Sessions updated successfully."}, status=status.HTTP_200_OK)


class SessionByCustomerView(APIView):
    def get(self, request, customer_id):
        # Get all sessions for a specific customer
        sessions = Session.objects.filter(customer_id=customer_id)
        
        # Check if there are sessions for the provided customer ID
        if not sessions.exists():
            return Response({"detail": "No sessions found for this customer."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = SessionSerializer(sessions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateSessionByCustomerView(APIView):
    def put(self, request, customer_id, session_id):
        """
        Updates a session for a specific customer.
        """

        try:
            # Check if the session belongs to the customer
            session = Session.objects.get(customer_id=customer_id, id=session_id)
        except Session.DoesNotExist:
            return Response({"detail": "Session not found for this customer."}, status=status.HTTP_404_NOT_FOUND)

        # Perform update
        serializer = SessionSerializer(session, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




