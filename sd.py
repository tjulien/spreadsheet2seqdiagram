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

def get_seq_diag( text, outputFile, style = 'default' ):
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

style = "qsd"
text = "alice->bob: authentication request\nbob-->alice: response"
pngFile = "out.png"

get_seq_diag( text, pngFile, style )
