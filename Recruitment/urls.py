from django.conf.urls import include, url
from django.contrib import admin
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    url(r'', include('Evaluator.urls')),
    url(r'^admin/', admin.site.urls),
]
