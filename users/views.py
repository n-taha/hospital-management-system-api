from django.shortcuts import render
from users.serializers import UserSerializer, NormalUserUpdateSerializer, UserRegisterSerializer, UserLoginSerializer, DoctorSerializerForNomalUsers, DoctorSerializer, AdminUserUpdateSerializer, PatientSerializer
from users.models import User, Doctor, Patient
from rest_framework.viewsets import ModelViewSet
from users.permissions import IsAdminCanDestroy, IsAdminOrOwnerReadOnly
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status

class UserViewSets(ModelViewSet):
    lookup_field = 'uuid'
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'patch', 'put', 'delete']

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return User.objects.all()
        else:
            return User.objects.filter(uuid=self.request.user.uuid)

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'retrieve':
            return UserSerializer
        elif self.action in ['update', 'partial_update']:
            if self.request.user.is_superuser:
                return AdminUserUpdateSerializer
            return NormalUserUpdateSerializer
        else:
            return UserSerializer

class UserRegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        return Response({
            "message": 'User Created Successfully',
            "user" : UserSerializer(user).data
        })


class UserLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        tokens = RefreshToken.for_user(user)
        return Response({
            "message": "Login Successfull",
            "access_token": str(tokens.access_token),
            "refresh_token": str(tokens),
            "user": UserSerializer(user).data
        }, status=status.HTTP_200_OK)


class DoctorViewSets(ModelViewSet):
    queryset = Doctor.objects.all()
    permission_classes = [IsAdminOrOwnerReadOnly]
    def get_serializer_class(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return DoctorSerializer
        return DoctorSerializerForNomalUsers

class PatientViewSets(ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [IsAdminCanDestroy]
    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return Patient.objects.all()
        return Patient.objects.filter(user=self.request.user)