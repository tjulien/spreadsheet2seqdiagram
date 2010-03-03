# HTTP dependencies for calling websequencediagrams.com
import urllib
import re

# google spreadsheet API
from gdata.spreadsheet.service import *

from django.conf import settings

class SSClient(object):

    def __init__(self, email, password):
        self.client = SpreadsheetsService()
        self.client.email = email
        self.client.password = password
        self.client.source = settings.SPREADSHEET_CLIENT
        self.client.ProgrammaticLogin()

    def get_ss_for_link(self, link):
        feed = self.client.GetSpreadsheetsFeed()
        for i, entry in enumerate(feed.entry):
            if entry.GetHtmlLink().href == link:
                return entry
        return None
    
    def get_worksheet(self, ss, ws_name):
        ss_id = ss.id.text
        ss_id_parts = ss_id.split('/')
        ss_key = ss_id_parts[len(ss_id_parts) - 1] # trailing key=value pair
        ws_feed = self.client.GetWorksheetsFeed(ss_key)
        for i, ws in enumerate(ws_feed.entry):
            if ws.title.text == ws_name:
                return ws
        return None

    def get_rows(self, ss, ws, row_start, row_end):
        ss_id = ss.id.text
        ss_id_parts = ss_id.split('/')
        ss_key = ss_id_parts[len(ss_id_parts) - 1] # trailing key=value pair

        ws_id = ws.id.text
        ws_id_parts = ws_id.split('/')
        ws_key = ws_id_parts[len(ws_id_parts) - 1] # trailing key=value pair
        query = ListQuery()
        query.start_index = row_start - 1
        query.max_results = (row_end - row_start) + 1
        row_feed = self.client.GetListFeed(ss_key, ws_key, query = query)
        return row_feed.entry

    def get_next_seq(self, ss, ws, previous_end):
        rows = self.get_rows(ss, ws, int(previous_end) + 1, int(previous_end) + 10)
        calls = self.get_calls(rows)
        start = int(previous_end) + 1
        for i, call in enumerate(calls[1:]):
            print i
            if call['jiras']:
                return start, start + i
    
    def get_calls(self, rows):
        calls = []
        for row in rows:
            cells = row.__dict__['custom']
            row_dict = {}
            for key,value in cells.iteritems():
                print key
                row_dict[key.strip()] = value.text
            calls.append(row_dict)
        return calls

    def create_seq_diag_input(self, calls):
        input = ''
        return_stack = []
        for i, call in enumerate(calls):
            input += call['caller'] + " -> " + call['callee'] + ": {" + call['input'] + '}\n'
            return_call = call['callee'] + " -> " + call['caller'] + ": {" + call['result'] + '}\n'
            if(i < len(calls) - 1):
                if calls[i + 1]['caller'] == call['callee']:
                    # save return for later
                    return_stack.append(return_call)
                else:
                    # return call immediately
                    input += return_call
            else:
                # end of the calls, now pop return_stack
                input += return_call
                return_stack.reverse()
                for return_call in return_stack:
                    input += return_call
        return input

    def call_web_seq_diag(self, text, outputFile, style = 'modern-blue' ):
        request = {}
        request["message"] = text
        request["style"] = style
        
        url = urllib.urlencode(request)
        
        f = urllib.urlopen("http://www.websequencediagrams.com/", url)
        line = f.readline()
        f.close()
        
        expr = re.compile("(\?img=[a-zA-Z0-9]+)")
        m = expr.search(line)
        
        if m == None:
            print "Invalid response from server."
            return False
        
        urllib.urlretrieve("http://www.websequencediagrams.com/" + m.group(0),
                           outputFile )
        return True

#    def get_all_jiras(self, ss, ws):
#        jiras = []
#        i = 2;
#        while rows = get_rows(ss, ws, i+=10, i + 10):
#            calls = get_calls(rows)
#            jiras_cells = [jira.strip() for jira in [jira_cell.split(',') for jira_cell in [call['jiras'] for call in calls]]]
            
                                  
        

def create_seq_diag(url, row_start, row_end, out_file):
    client = SSClient(settings.USERNAME, settings.PASSWORD)
    ss = client.get_ss_for_link(url)
    ws = client.get_worksheet(ss, settings.WORKSHEET_NAME)
    rows = client.get_rows(ss, ws, int(row_start), int(row_end))
    calls = client.get_calls(rows)
    input = client.create_seq_diag_input(calls)
    client.call_web_seq_diag(input, out_file)
    return calls[0]['jiras'], calls[0]['story']

def get_next_seq(url, previous_end):
    client = SSClient(settings.USERNAME, settings.PASSWORD)
    ss = client.get_ss_for_link(url)
    ws = client.get_worksheet(ss, settings.WORKSHEET_NAME)
    return client.get_next_seq(ss, ws, previous_end)

