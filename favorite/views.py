from django.db.models.loading import get_model
from django.http import HttpResponse
import json
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_text
from django.utils.functional import Promise
from .models import Favorite
from django.views.generic import View

class AddOrRemoveView(View):

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            user = request.user
            target_model = get_model(*request.POST['target_model'].split('.') or None)
            target_content_type = ContentType.objects.get_for_model(target_model)
            target_object_id = request.POST['target_object_id']

            # delete it if it's already a faorite
            if user.favorite_set.filter(target_content_type=target_content_type,
                                     target_object_id=target_object_id):
                user.favorite_set.get(target_content_type=target_content_type,
                                         target_object_id=target_object_id).delete()
                status = 'deleted'

            # otherwise, create it
            else:
                user.favorite_set.create(target_content_type=target_content_type,
                                         target_object_id=target_object_id)
                status = 'added'

            response = {'status': status,
                        'fav_count': Favorite.objects.filter(target_content_type=target_content_type,
                                                             target_object_id=target_object_id).count()}

            return HttpResponse(json.dumps(response), content_type='application/json')

        return HttpResponse(status=405)


