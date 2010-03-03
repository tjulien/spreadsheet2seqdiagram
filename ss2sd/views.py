import os
from django.template import Context, loader
from django.http import HttpRequest, HttpResponse
from django.conf import settings

from ss2sd.forms import *

from ss2sd.sd import *
from settings import MEDIA_ROOT

def ss2sd_form(request):
    if request.method == 'POST':
        start = request.POST['start']
        end = request.POST['end']
        filename = os.path.join(MEDIA_ROOT, start + '-' + end + '-' + 'outfile.png')
        if os.path.exists(filename):
            os.remove(filename)
        jiras, story = create_seq_diag(settings.SPREADSHEET_URL, start, end, filename)
        c = Context({'start' : start,
                     'end' : end,
                     'mimetype' : 'text/html',
                     'jiras' : get_jiras(jiras),
                     'story' : story,
                     'host' : settings.HOST})
        return HttpResponse(loader.get_template('ss2sd/generated_seq_diag.html').render(c), mimetype='text/html')
    else:
        form = RowInputForm()
        c = Context({})
        return HttpResponse(loader.get_template('ss2sd/row_form.html').render(c), mimetype='text/html')

def browse_next(request):
    previous = request.POST['previous_end']
    start, end = get_next_seq(settings.SPREADSHEET_URL, previous)
    request = HttpRequest()
    request.method = 'POST'
    request.POST['start'] = str(start)
    request.POST['end'] = str(end)
    print start
    print end
    return ss2sd_form(request)

def get_jiras(ids):
    jira_ids = ids.split(',')
    jiras = []
    for id in jira_ids:
        jiras.append(settings.JIRA_PREFIX + id.strip())
    return jiras
