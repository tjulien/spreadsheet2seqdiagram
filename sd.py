# HTTP dependencies for calling websequencediagrams.com
import urllib
import re

# google spreadsheet API
from gdata.spreadsheet.service import *

class SSClient(object):

    def __init__(self, email, password):
        self.client = SpreadsheetsService()
        self.client.email = email
        self.client.password = password
        self.client.source = 'limewire-ss2sd-0.1'
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
        row_feed = self.client.GetListFeed(ss_key, ws_key)
        return row_feed.entry[row_start - 2:row_end - 1]

    def get_calls(self, rows):
        calls = []
        for row in rows:
            cells = row.__dict__['custom']
            row_dict = {}
            for key,value in cells.iteritems():
                row_dict[key] = value.text
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

    def get_seq_diag(self, text, outputFile, style = 'modern-blue' ):
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
    
