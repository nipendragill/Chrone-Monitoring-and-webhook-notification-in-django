from django.conf.urls import url
from .views import authenticate_user, CreateUserAPIView, ListUserAPIView, UpdateUserAPIView
urlpatterns = [
    url(r'^get_token/$', authenticate_user, name='get_token'),
    url(r'^signup/$', CreateUserAPIView.as_view(), name='create_user'),
    url(r'^users/$', ListUserAPIView.as_view(), name='list_users'),
    url(r'^users/(?P<user_id>[\d-]+)/?$', UpdateUserAPIView.as_view(), name='retrieve_update_usere')
]