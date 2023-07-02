from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView

from .serializers import UserSerializer

User = get_user_model()


class SignupAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        return super().post(request, *args, **kwargs)
