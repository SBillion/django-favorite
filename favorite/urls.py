from django.conf.urls import patterns, url
from .views import AddOrRemoveView


urlpatterns = patterns('favorite.views',
    url(r'^add-or-remove$', AddOrRemoveView.as_view(),name='favit'),
)
