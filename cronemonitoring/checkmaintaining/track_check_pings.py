from .utils import run_async
from .db_models.check_detail_user import CheckTrack
from datetime import datetime
from django.db import transaction
from .db_models.check import CheckDetails


class TrackCheckPings:

    @run_async
    def update_check_details_model(self, check_id=None, request_type=None, data=None):

        try:
            check_track_info = CheckTrack.objects.filter(check_id=check_id).order_by('-latest_hitted_at')
            if check_track_info.exist():
                latest_check = check_track_info.first()
                prev_hitted_at = latest_check
                latest_hitted_at = datetime.datetime.now()
            else:
                prev_hitted_at= datetime.datetime.now()
                latest_hitted_at = datetime.datetime.now()
            user = data.get('user')
            request_type = request_type
            if request_type in ['get', 'delete']:
                data_in_request_body = None
            else:
                data_in_request_body = data
            transaction.set_autocommit(False)
            try:
                CheckTrack.objects.create(
                    check= CheckDetails.objects.get(id=check_id),
                    request_type = request_type,
                    prev_hitted_at = prev_hitted_at,
                    latest_hitted_at = latest_hitted_at,
                    latest_hit_by = user,
                    data_in_request_body = data_in_request_body
                )
                transaction.commit()
                transaction.set_autocommit(True)
            except:
                pass
        except:
            pass


