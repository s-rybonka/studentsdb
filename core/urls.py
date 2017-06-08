from django.conf.urls import url, include

from .views import HomePageView,TeamPageView

urlpatterns = [
    # Site urls
    url(r'^$', HomePageView.as_view(), name='home-page'),
    url(r'^team-page/$', TeamPageView.as_view(), name='team-page'),

]
