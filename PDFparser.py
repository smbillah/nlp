'''
Created on Feb 22, 2013

@author: Masum

'''

import pyPdf
def getPDFContent(path):
    content = ""
    # Load PDF into pyPDF
    pdf = pyPdf.PdfFileReader(file(path, "rb"))
    # Iterate pages
    for i in range(0, pdf.getNumPages()):
        # Extract text from page and add to content
        content += pdf.getPage(i).extractText() + " \n"
    # Collapse whitespace
    content = " ".join(content.replace(u"\xa0", u" ").strip().split())
    return content

f = open('sample.txt','w+')
f.write(getPDFContent('hw1-final.pdf'))
f.close()

#print getPDFContent(sys.argv[1]).encode("ascii", "xmlcharrefreplace")
## end of http://code.activestate.com/recipes/577095/ }}}
