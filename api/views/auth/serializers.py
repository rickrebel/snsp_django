from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from user.models import User, InvitationToken, Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(
        required=True, style={'input_type': 'password'})
    key = serializers.CharField(required=False)


class UserDataSerializer(serializers.ModelSerializer):
    fullname = serializers.ReadOnlyField(source="full_name")
    token = serializers.ReadOnlyField(source="auth_token.key")
    # role = RoleSerializer(read_only=True)

    class Meta(object):
        model = User
        fields = [
            "id", 'email', 'username', "first_name", "last_name",
            "token", "fullname", "is_staff",
            "is_superuser", "role"
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    # role = RoleSerializer(read_only=True)

    def get_full_name(self, obj):
        return obj.get_full_name()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "is_staff",
            "is_superuser",
            "first_name",
            "last_name",
            "full_name",
            "role"
        ]


class UserSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    password = serializers.CharField(
        min_length=8,
        style={ 'input_type': 'password' })
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(
        required=False,
        validators=[UniqueValidator(queryset=User.objects.all())])
    checkCondiction = serializers.BooleanField(
        required=False)
    key = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "last_login",
            "is_superuser",
            "username",
            "first_name",
            "last_name",
            "full_name",
            "email",
            "is_staff",
            "is_active",
            "date_joined"
        ]
        # read_only_fields = [
        #     "last_login",
        #     "is_superuser",
        #     "username",
        #     "full_name",
        #     "is_staff",
        #     "is_active",
        #     "date_joined"
        # ]


class UserRegistrationSerializer(UserDataSerializer):

    class Meta:
        model = User
        fields = UserDataSerializer.Meta.fields + ["password"]
        # read_only_fields = UserDataSerializer.Meta.read_only_fields



class InvitationTokenSerializer(serializers.ModelSerializer):
    # institution_full = InstitutionSimpleSerializer(
    #     read_only=True, source='institution')

    class Meta:
        model = InvitationToken
        fields = ["email", "institution", "institution_full"]
