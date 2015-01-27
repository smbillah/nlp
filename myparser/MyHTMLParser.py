'''
Created on Mar 11, 2012

@author: Masum
'''
import sys
from HTMLParser import HTMLParser
from shared import term_count
from shared import parse


class MyHTMLParser(HTMLParser):
#    global term_count
    
    text, N, newline ='', 0,{'br':'\n','BR':'\n'}       
    document_id, hash_value = 0, 0
    
    
    def __init__(self, config, ht):
        HTMLParser.__init__(self)
        self.config = config
        self.ht = ht
        
    
    def handle_data(self, raw):
        self.text = self.text+ raw+ self.newline.get(self.lasttag,'')
    
    #format is (token =>value, here val)
    def feed(self,data, did):
        #extracting html text
        try:        
            HTMLParser.feed(self,data)
        except:            
            sys.exc_clear()
                                  
        #tokenizing extracted data
        for line in self.text.splitlines():                        
            tokens= parse(line, self.config)
            if not tokens: continue
            for token in tokens:
                self.ht.put_data(token, did)
                self.N +=1
        term_count[did] = self.N 
    
        #cleaning for next feed
        self.text  = ''; self.N=0
        HTMLParser.reset(self)
     
