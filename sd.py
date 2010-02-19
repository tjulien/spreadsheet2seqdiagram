import urllib
import re

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

getSequenceDiagram( text, pngFile, style ) 
