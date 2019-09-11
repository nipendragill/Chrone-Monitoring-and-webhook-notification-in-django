from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import Serializer
from rest_framework import serializers
from ..db_models.check import CheckDetails
from ..db_models.check_detail_user import CheckTrack


class CheckSerializer(serializers.ModelSerializer):

    class Meta:
        model = CheckDetails
        fields = '__all__'

    def create(self, validated_data):
        validated_data['url'] = self.context.get('url')
        check = CheckDetails.objects.create(**validated_data)
        return check

class CheckTrackSerializer(serializers.ModelSerializer):

    class Meta:
        model = CheckTrack
        fields = '__all__'
