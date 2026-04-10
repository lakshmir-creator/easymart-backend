from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from .models import User
from .serializers import UserRegistrationSerializer

class RegisterUserAPI(APIView):

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            return Response({
                "message": "Signup successful",
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginUserAPI(APIView):

    def post(self, request):
        identifier = request.data.get('identifier')  # email or mobile
        password = request.data.get('password')

        if not identifier or not password:
            return Response({
                "error": "Identifier and password are required"
            }, status=400)

        # 🔍 Check email or mobile
        if '@' in identifier:
            user = User.objects.filter(email=identifier).first()
        else:
            user = User.objects.filter(mobile=identifier).first()

        if not user:
            return Response({
                "error": "User not found"
            }, status=404)

        # 🔐 Check password
        if not check_password(password, user.password):
            return Response({
                "error": "Invalid password"
            }, status=400)

        return Response({
            "message": "Login successful",
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "mobile": user.mobile
                }
        })