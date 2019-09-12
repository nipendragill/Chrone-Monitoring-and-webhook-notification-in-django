from rest_framework import generics
from rest_framework.response import Response
from ..db_models.check import CheckDetails
from ..error import Error
from django.db import DatabaseError
from rest_framework import status
from ..Serializers.checks_serializer import CheckSerializer, CheckTrackSerializer
from rest_framework.permissions import IsAuthenticated
from ..db_models.check_detail_user import CheckTrack


class UserSelectedCheck(generics.ListCreateAPIView):

    permission_classes = (IsAuthenticated,)

    def get_queryset(self, user_id):
        try:
            checks = CheckDetails.objects.filter(user_id=user_id)
            if not checks.exists():
                error = Error('No check is created by selected user')
                return None, error
            return checks
        except DatabaseError as e:
            return Response({'detail':'Database error occured'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        user_id = int(user_id)
        checks, error = self.get_queryset(user_id=user_id)
        if error is not None:
            return Response({'detail':error.message}, status= error.status)

        serializer_class = CheckSerializer(checks, many=True)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        else:
            return Response({'details':serializer_class.errors},
                             status=status.HTTP_400_BAD_REQUEST)


class PingsOnCheck(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        check_id = kwargs.get('check_id')

        check_id = int(check_id)
        checks_pings = CheckTrack.objects.filter(check__id=check_id)
        if checks_pings.exists():
            serializer_class = CheckTrackSerializer(data=checks_pings, many=True)
            return self.get_paginated_response(serializer_class.data)
        else:
            return Response({'detail':'No check exists with given Id'},
                            status=status.HTTP_400_BAD_REQUEST)


class LastPingsDetails(generics.ListAPIView):

    def get(self, request, *args, **kwargs):

        check_pings = CheckTrack.objects.all()
        if check_pings.exists():
            serializer_class = CheckTrackSerializer(check_pings, many=True)
            return self.get_paginated_response(serializer_class.data)
        else:
            return Response({'detail':'No pings exists till now'},
                            status=status.HTTP_200_OK)



