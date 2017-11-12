from django.conf.urls import url, include

urlpatterns = [
    url(r'^profile/', include('cabinet.profile_.urls', 'profile', 'profile')),
]
