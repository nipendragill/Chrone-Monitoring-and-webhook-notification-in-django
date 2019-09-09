from rest_framework import serializers
from ..models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password', 'created_at', 'updated_at')
        extra_kwargs = {'password': {'write_only': True}}


class UserProfileWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password', 'created_at', 'updated_at')

    def __init__(self, *args, **kwargs):
        super(UserProfileWriteSerializer, self).__init__(*args, **kwargs)
        fields_ = ['email', 'first_name', 'last_name', 'password']

        for field in fields_:
            self.fields[field].error_messages = {
                'required': '{0} is required.'.format(field.upper()),
                'blank': '{0} cannot be blank.'.format(field.upper()),
                'invalid_choice': 'Invalid entry for {0}'.format(field.upper())
            }

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        instance.save()
        return instance