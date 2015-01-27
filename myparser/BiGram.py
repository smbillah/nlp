'''
Created on Feb 4, 2013

@author: Masum
'''
import os

from BiGramHTMLParser import BiGramHTMLParser
from collections import defaultdict

class BiGram():      
    def __init__(self, config):
        self.config = config
        self.ht = defaultdict(int)
        self.toks = defaultdict(int)        
        self.htmlparser = BiGramHTMLParser(self.config, self.ht, self.toks)        
        self.start_batch_processing()
        self.write_file_map()
        del self.ht;
        del self.toks;
                              
    def start_batch_processing(self):
        file_id=0
        
        for in_file in os.listdir(self.config['str_src_dir']):
            #if in_file not in ['medium.html','simple.html']: continue #for testing
            with open(self.config['str_src_dir']+ in_file, 'r') as f:
                self.htmlparser.feed(f.read(),file_id)                                    
                file_id += 1
        
    def write_file_map(self):
        #writing bigram file to a file named under document id
        with open(self.config['str_dst_dir']+  self.config['str_doc_id_file_name'],'wb+') as f:
            for words, count in sorted(self.ht.iteritems(), key=lambda (k,v): (v,k), reverse= True):
                f.write(words[0]+" "+words[1]+" "+str(count)+"\n")
        
        with open(self.config['str_dst_dir']+  'all_tokens.txt','wb+') as f:
            for words, count in sorted(self.toks.iteritems(), key=lambda (k,v): (v,k), reverse= True):
                f.write(words+" "+str(count)+"\n")
        
        
