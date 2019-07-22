from django.conf.urls import include, url
from django.contrib import admin
from django.views.i18n import JavaScriptCatalog
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    url(r'', include('Evaluator.urls')),
    url(r'^admin/', admin.site.urls),
    url('^', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
