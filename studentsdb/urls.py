from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.views.i18n import JavaScriptCatalog

from studentsdb.settings import MEDIA_ROOT, DEBUG, MEDIA_URL

js_info_dict = {
    'packages': ('students',),
}

urlpatterns = i18n_patterns(
    url(r'^admin/', admin.site.urls),
    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'cabinet/', include('students.urls')),
    url(r'', include('core.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^manager/', include('manager.urls', 'manager', 'manager')),
    url(r'^cabinet/', include('cabinet.urls', 'cabinet', 'cabinet')),
)
# Set media files folder only for development
if DEBUG:
    urlpatterns += [] + static(MEDIA_URL, document_root=MEDIA_ROOT)
    import debug_toolbar

    urlpatterns = [
                      url(r'^__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
    urlpatterns.append(url(r'^rosetta/', include('rosetta.urls')))
