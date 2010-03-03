from django.conf.urls.defaults import *
import os

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^spreadsheet2seqdiagram/', include('spreadsheet2seqdiagram.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^ss2sd/browse_next', 'spreadsheet2seqdiagram.ss2sd.views.browse_next'),
    (r'^ss2sd/', 'spreadsheet2seqdiagram.ss2sd.views.ss2sd_form'),
    (r'^assets/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.dirname(__file__), 'assets')}),
)
