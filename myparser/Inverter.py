'''
Created on Mar 11, 2012

@author: Masum
'''
import os
from hashtable import myhashtable
from MyHTMLParser import MyHTMLParser
from shared import term_count, doc_id

class Inverter():  
    #global doc_id, term_count
    
    def __init__(self, config):
        self.config = config
        self.ht = myhashtable(config)        
        self.htmlparser = MyHTMLParser(self.config, self.ht)        
        self.start_batch_processing()
        self.write_file_map()
        self.ht.write_posting_file(term_count)
        self.ht.write_hash_table()
               
       
    def start_batch_processing(self):
        file_id=0
        
        for in_file in os.listdir(self.config['str_src_dir']):
            #if in_file not in ['medium.html','simple.html']: continue #for testing
            with open(self.config['str_src_dir']+ in_file, 'r') as f:
                doc_id[file_id]= in_file
                term_count[file_id]= 0 
                self.htmlparser.feed(f.read(),file_id)                                    
                file_id += 1
        

    # writing doc_id <--> doc_name file
    def write_file_map(self):
        #writing document id file
        with open(self.config['str_dst_dir']+  self.config['str_doc_id_file_name'],'wb+') as f:
            for did, txt in doc_id.iteritems():
                f.write('{0:0>{1}d} {2:''<{3}s}\n'.
                        format(did, self.config['file_id_encoding_len'], 
                               txt, self.config['file_name_len']))
    

