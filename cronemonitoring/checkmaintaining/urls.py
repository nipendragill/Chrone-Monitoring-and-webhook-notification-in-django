from django.conf.urls import url
from .views import authenticate_user, CreateUserAPIView, ListUserAPIView, UpdateUserAPIView
from .view_checks import userselected_check, create_check
urlpatterns = [
    url(r'^get_token/$', authenticate_user, name='get_token'),
    url(r'^signup/$', CreateUserAPIView.as_view(), name='create_user'),
    url(r'^users/$', ListUserAPIView.as_view(), name='list_users'),
    url(r'^users/(?P<user_id>[\d-]+)/?$', UpdateUserAPIView.as_view(), name='retrieve_update_usere'),
    url(r'^users/(?P<user_id>[\d-]+)/checks/?$', userselected_check.UserSelectedCheck.as_view(), name='user_selected_checks'),
    url(r'^checks/$', create_check.CreateCheck.as_view(), name='create_check'),
    url(r'^checks/(?P<check_id>[\d-]+)/$', create_check.ModifyCheck.as_view(), name='update_delete_check'),
    url(r'^checks/(?P<check_id>[\d-]+)/pings/$', userselected_check.PingsOnCheck.as_view(),name='pings_on_check'),
    url(r'^pingsdetails/$', userselected_check.LastPingsDetails.as_view(), name='latest_ping_details')
]