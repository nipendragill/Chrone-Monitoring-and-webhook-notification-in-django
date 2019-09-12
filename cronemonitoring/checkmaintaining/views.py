from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .Serializers.user_serializer import UserSerializer, UserProfileWriteSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework_jwt.settings import api_settings
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .pagination import CustomPagination
from django.db import transaction, DatabaseError
# from rest_framework import request
from .error import Error
# from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# from rest_framework.pagination import PageNumberPagination


@api_view(['POST'])
@permission_classes([AllowAny, ])
def authenticate_user(request):
    try:
        email = request.data['email']
        password = request.data['password']

        user = User.objects.get(email=email, password=password)
        if user:
            try:
                jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)

                user_details = {}
                user_details['name'] = f'{user.first_name} {user.last_name}'
                user_details['token'] = token
                user_details['email'] = user.email
                user_details['created_at'] = user.created_at
                user_details['updated_at'] = user.updated_at
                return Response(user_details, status=status.HTTP_200_OK)

            except Exception as e:
                raise e
        else:
            res = {
                'error': 'account is currently inactive, please activate your account'}
            return Response(res, status=status.HTTP_403_FORBIDDEN)
    except KeyError:
        res = {'error': 'pleasae provide email address and password'}
        return Response(res)


class CreateUserAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data
        transaction.set_autocommit(False)
        try:
            serializer = UserSerializer(data=user)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                transaction.commit()
                transaction.set_autocommit(True)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                transaction.rollback()
                transaction.set_autocommit(False)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except DatabaseError as e:
            transaction.rollback()
            transaction.set_autocommit(True)
            return Response({'detail': 'Error inserting database'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListUserAPIView(generics.ListAPIView):

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        try:
            queryset = User.objects.all().order_by('-created_at')
            queryset = self.paginate_queryset(queryset)
            return queryset, None
        except DatabaseError as e:
            return Response({'detail': 'Error getting User'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        data, error = self.get_queryset()

        if error is not None:
            return Response({'detail': error.message},
                            status=status.HTTP_400_BAD_REQUEST)
        serialized_data = UserSerializer(data, many=True).data
        return self.get_paginated_response(serialized_data)


class UpdateUserAPIView(generics.RetrieveUpdateAPIView):

    permission_classes = (IsAuthenticated, )

    def get_queryset(self, user_id = None):

        try:
            user_info = User.objects.filter(pk=user_id)
            if user_info.exists():
               return user_info, None
            else:
                error = Error({'detail':'UserId does not exists'},
                              status=status.HTTP_400_BAD_REQUEST)
                return None, error

        except DatabaseError as e:
            error = Error({"detail":'Error fetching details of the user'},
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return None, error

    def get(self, request, *args, **kwargs):

        user_id = kwargs.get('user_id')
        if user_id is None:
            return Response({'detail':'Please select a user id'},
                            status=status.HTTP_400_BAD_REQUEST)
        user_id = int(user_id)
        user, error = self.get_queryset(user_id=user_id)
        if error is not None:
            return Response({'detail': error.message},
                            status=error.status)

        serialzer_class = UserSerializer(user.first())
        if serialzer_class.is_valid(raise_exception=True):
            return Response(serialzer_class.data, status=status.HTTP_200_OK)
        else:
            return Response(serialzer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        if user_id is None:
            return Response({'detail': 'Please select a user id'},
                            status=status.HTTP_400_BAD_REQUEST)
        user_id = int(user_id)
        user, error = self.get_queryset(user_id=user_id)
        if 'email' in request.data.keys():
            return Response({'detail':'Can not update email field'},
                            status=status.HTTP_400_BAD_REQUEST)
        if error is not None:
            return Response({'detial': error.message},
                            status=status.HTTP_400_BAD_REQUEST)
        user = user.first()
        transaction.set_autocommit(False)
        try:
            context = {"request": self.request,
                       "updated_by": request.user}
            serializer = UserProfileWriteSerializer(user, data=request.data,
                                                    partial=True, context=context)
            if serializer.is_valid(raise_exception=True):
                serializer.update(user, request.data)
                transaction.commit()
                transaction.set_autocommit(True)
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                transaction.rollback()
                transaction.set_autocommit(False)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except DatabaseError as e:
            transaction.rollback()
            transaction.set_autocommit(False)
            return Response({'detail': 'Error connecting to database'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
