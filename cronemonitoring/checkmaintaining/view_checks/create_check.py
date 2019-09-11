from rest_framework import generics
from ..Serializers.checks_serializer import CheckSerializer
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from django.db.transaction import DatabaseError
from ..track_check_pings import TrackCheckPings


class CreateCheck(generics.ListCreateAPIView):

    def post(self, request, *args, **kwargs):

        url = request.build_absolute_uri()
        context = {'url':url}
        transaction.set_autocommit(False)
        try:
            serializer_class  = CheckSerializer(data=request.data, context=context)
            if serializer_class.is_valid(raise_exception=True):
                serializer_class.save()
                transaction.commit()
                transaction.set_autocommit(True)
                check_id = serializer_class.data.id
                TrackCheckPings.update_check_details_model(check_id=check_id,
                                                           request_type = 'post',
                                                           data=request.data)
                return Response(serializer_class.data, status=status.HTTP_201_CREATED)
            else:
                transaction.rollback()
                transaction.set_autocommit(False)
                return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
        except DatabaseError as e:
            return Response({'detail':'Database error occured'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

