from django.conf.urls import url, include

from cabinet.profile_ import views as profile_views

urlpatterns = [

    url(r'^personal-data/', profile_views.UserProfileView.as_view(), name='personal-data'),

    url(r'^session-settings/', profile_views.SessionSettingsView.as_view(), name='session-settings'),

]
