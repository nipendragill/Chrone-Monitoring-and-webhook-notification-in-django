from rest_framework import generics
from rest_framework.response import Response
from ..db_models.check import CheckDetails
from ..error import Error
from django.db import DatabaseError
from rest_framework import status
from ..Serializers.checks_serializer import CheckSerializer
from rest_framework.permissions import IsAuthenticated


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
