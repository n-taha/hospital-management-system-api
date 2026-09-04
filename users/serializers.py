from rest_framework import serializers
from users.models import User
from django.contrib.auth import authenticate
from users.models import Doctor, Patient




# This is For See User List
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "uuid",
            "email",
            "first_name",
            "last_name",
            "role",
            "phone_number",
            "address",
            "created_at",
        ]
        read_only_fields = ["uuid", "created_at", "role"]


class NormalUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "address", "phone_number"]


class AdminUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "address", "phone_number", "role"]


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        Patient.objects.create(user=user)
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs["email"]
        password = attrs["password"]

        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError("invalid email or password")

        if not user.is_active:
            raise serializers.ValidationError("Your Account is inactive")

        attrs["user"] = user

        return attrs


class UserDoctorSerializerForNormalUser(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["full_name"]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()


# this serializer is only for normal users
class DoctorSerializerForNomalUsers(serializers.ModelSerializer):
    user = UserDoctorSerializerForNormalUser(read_only=True)

    class Meta:
        model = Doctor
        fields = [
            "user",
            "id",
            "department",
            "specialization",
            "consultation_fee",
            "is_available",
            "updated_at",
        ]
        read_only_fields = ["user", "department", "updated_at"]


# this is for admin
class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="user", write_only=True
    )

    class Meta:
        model = Doctor
        fields = [
            "user",
            "user_id",
            "id",
            "department",
            "specialization",
            "lisence_no",
            "consultation_fee",
            "is_available",
            "updated_at",
        ]

    def validate_user_id(self, user_id):
        if Doctor.objects.filter(user=user_id).exists():
            raise serializers.ValidationError({"message": "User is already a doctor"})
        return user_id

    def create(self, validated_data):
        user = validated_data["user"]
        user.role = User.Role.DOCTOR
        user.save()
        doctor = Doctor.objects.create(
            **validated_data
        )
        return doctor


class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Patient
        fields = [
            "user",
            "id",
            "date_of_birth",
            "blood_group",
            "emergency_contact",
            "updated_at",
        ]
