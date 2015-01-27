'''
Created on Mar 10, 2012

@author: Masum
'''
from collections import defaultdict
from literal_class import DictEntry, RawEntry
from hash_function import FNVHash
from math import log10

class myhashtable():
    used, collisions, lookups= 0, 0, 0    
    
    def __init__(self, config):
        self.buffer_dict = defaultdict(int)
        self.config= config
                    
    def find(self, key):
#        index =APHash(key) % self.config['ht_len']
        index =FNVHash(key) % self.config['ht_len']
#        index =BPHash(key) % self.config['ht_len']
#        index =DEKHash(key) % self.config['ht_len']
#        index =DJBHash(key) % self.config['ht_len']
#        index =SDBMHash(key) % self.config['ht_len']
#        index =BKDRHash(key) % self.config['ht_len']
#        index =ELFHash(key) % self.config['ht_len']
#        index =PJWHash(key) % self.config['ht_len']
#        index =JSHash(key) % self.config['ht_len']
#        index =hash_function(key) % self.config['ht_len']
#        index =RSHash(key) % self.config['ht_len']
        
        # check to see if word is in that location, if not there, 
        # do linear probing until word found or empty location found
        while self.buffer_dict[index] and self.buffer_dict[index].key != key:
            index = (index + 1) % self.config['ht_len']
            self.collisions +=1   
        return index
                
    def get_data(self,key):    
        index = self.find(key)
        
        self.lookups +=1
        return self.buffer_dict.get(index, False)
    
    def put_data(self, token, doc_id):
        index = self.find(token)
        
        if self.buffer_dict[index]:
            self.buffer_dict[index].post_dict[doc_id]+=1
        else:
            value= RawEntry(key= token, post_dict= defaultdict(int))
            value.post_dict[doc_id]=1
            self.buffer_dict[index]=value
            self.used += 1

    def write_posting_file(self, term_count):                
        file_post=open(self.config['str_dst_dir']+ self.config['str_posting_file_name'], "wb+")
        
        total_docs= len(term_count)
        start_index = 0
        for key in self.buffer_dict.keys():
            value = self.buffer_dict[key]   
            posting = value.post_dict            
            term_frequency =len (posting.keys())
            idf= log10(total_docs*1.0/term_frequency)
        
            #calculate rtf
            for did in posting.keys(): 
                #calculation of idf*rtf
                posting[did] = posting[did]*idf* 1.0/term_count[did]
                
                            
            #sort by rtf, and finally write to disk
            for did, rtf in sorted(posting.iteritems(), key=lambda (k,v): (v,k), reverse= True):
                file_post.write('{0:0>{1}d} {2:0>{3}.{4}f}\n'.
                                format(did, self.config['file_id_encoding_len'],
                                       rtf, self.config['term_wt_decimal_len'],
                                       self.config['term_weight_len']))                         
            #make dictionary concise
            dict_entry= DictEntry(key= value.key, num_docs=term_frequency, 
                                   start_index=start_index)
            self.buffer_dict[key]= dict_entry                        
            start_index +=term_frequency
        file_post.close()
    
    def write_hash_table(self):
        file_dict = open(self.config['str_dst_dir']+ self.config['str_dictionary_file_name'], "wb+")        
        template_str= ['{0:''<{1}s} {2:0>{3}} {4:0>{5}}\n', '{0:''<{1}s} {2:''>{3}s} {4:''>{5}s}\n']
        template_empty = DictEntry(key='', num_docs='', start_index='')
        is_empty= False
        
        for i in range(self.config['ht_len']):            
            if self.buffer_dict[i]: value = self.buffer_dict[i]                
            else: is_empty =True; value= template_empty  
            
            #writing dictionary file
            file_dict.write(template_str[is_empty].format(value.key[:self.config['token_len_in_file']], 
                                              self.config['token_len_in_file'],
                                              value.num_docs,self.config['file_occurance_encoding_len'],
                                              value.start_index, self.config['posting_start_len']))
            is_empty=False
        
        file_dict.close()    
        print 'collision: ', self.collisions, ' used:', self.used, ' lookups:', self.lookups
   
