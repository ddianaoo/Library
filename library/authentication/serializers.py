from rest_framework import serializers
from .models import CustomUser
from .signin import EmailAuthBackend


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'middle_name', 'email', 'role', 'password', 'created_at',
                  'updated_at', 'is_superuser', 'is_staff', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        role = validated_data.pop('role')
        first_name = validated_data.pop('first_name')
        middle_name = validated_data.pop('middle_name')
        last_name = validated_data.pop('last_name')
        return CustomUser.create(email=email, password=password, role=role, first_name=first_name,
                                 middle_name=middle_name, last_name=last_name)

    def update(self, instance, validated_data):
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        middle_name = self.validated_data['middle_name']
        password = self.validated_data['password']
        role = self.validated_data['role']
        instance.update(first_name=first_name,
                        last_name=last_name,
                        middle_name=middle_name,
                        password=password,
                        role=role,
                        )

        return instance

    def validate(self, attrs):
        # Take username and password from request
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            pass
        else:
            msg = 'Both "email" and "password" are required.'
            raise serializers.ValidationError(msg, code='creation')

        return attrs


class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * username
      * password.
    It will try to authenticate the user with when validated.
    """
    email = serializers.EmailField(
        label="Email",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        # Take username and password from request
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # Try to authenticate the user using Django auth framework.
            user = EmailAuthBackend().authenticate(
                                email=email, password=password)
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "email" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs