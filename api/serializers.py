from rest_framework import serializers

from accounts.models import User
from blog.models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
   class Meta:
      model = Post
      fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
   class Meta:
      model = Comment
      fields = "__all__"


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'surname', 'forename', 'password']

        def validate_email(self, value):
            if not value.endswith('@example.com'):  # Example validation
                raise serializers.ValidationError("Email must be from the domain 'example.com'.")
            return value

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist.")

        if not user.check_password(password):
            raise serializers.ValidationError("Incorrect password.")

        attrs['user'] = user
        return attrs