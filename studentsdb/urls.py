"""studentsdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.i18n import JavaScriptCatalog
from studentsdb.settings import MEDIA_ROOT, DEBUG, MEDIA_URL
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

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
)
# Set media files folder only for development
if DEBUG:
    urlpatterns += [] + static(MEDIA_URL, document_root=MEDIA_ROOT)
    import debug_toolbar

    urlpatterns = [
                      url(r'^__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
    urlpatterns.append(url(r'^rosetta/', include('rosetta.urls')))
