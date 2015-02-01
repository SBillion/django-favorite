from django.contrib.contenttypes.models import ContentType
from django.db.models.loading import get_model
from .models import Favorite


class UserFavoriteMixin(object):



    def get_favorite_set(self, target=None):
        qs = Favorite.objects.filter(user=self).prefetch_related('target')

        if target:
            model_type = ContentType.objects.get_for_model(target)
            qs = qs.filter(target_content_type=model_type)
        return [x.target for x in qs]

    def get_favorite_article_counter(self):
        model = get_model('articles','Article')
        return len(self.get_favorite_set(model))

    def favorite(self,target):
        item_type = ContentType.objects.get_for_model(target)
        Favorite.objects.get_or_create(user=self, target_content_type=item_type, target_object_id
        =target.pk)

    def unfavorite(self, target):
        item_type = ContentType.objects.get_for_model(target)
        Favorite.objects.filter(user=self, target_content_type=item_type, target_object_id
        =target.pk).delete()

    def is_favorite(self, target):
        item_type = ContentType.objects.get_for_model(target)
        return Favorite.objects.filter(user=self, target_content_type=item_type,
                                       target_object_id=target.pk).exists()


class TargetFavoriteMixin(object):
    def get_fav_users(self):
        content_type = ContentType.objects.get_for_model(self)
        favs = Favorite.objects.filter(target_content_type=content_type,
                                        target_object_id=self.pk, ).prefetch_related('user')

        return [x.user for x in favs]

    def count_fav_users(self):
        content_type = ContentType.objects.get_for_model(self)
        return Favorite.objects.filter(target_content_type=content_type, target_object_id
        =self.id).count()
