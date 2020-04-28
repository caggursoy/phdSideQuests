import markdown as md
import codecs
from weasyprint import HTML

def htmlHead(str, styleTag = False):
    if styleTag:
        css_input = 'generic css style'
        outStr = '<html>\n\t<head>\n\t\t<style>'+css_input+'</style>\n\t</head>\n\t<body>'+str+'</body>\n<html>'
    else:
        outStr = '<html>\n\t<body>'+str+'</body>\n<html>'
    return outStr

mdStr = htmlHead('test str here')
fileName = "test.html"
output_file = codecs.open(fileName, "w", encoding="utf-8", errors="xmlcharrefreplace")
output_file.write(mdStr)
HTML(fileName).write_pdf('test.pdf')
