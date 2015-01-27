'''
Created on Mar 10, 2012

@author: Masum
'''

from hash_function import FNVHash
from literal_class import DictEntry 
from mycollection import OrderedDict


class query_processor():

    def __init__(self, config):
        self.config=config
        self.dict_file= self.config['str_dst_dir']+self.config['str_dictionary_file_name']
        self.post_file = self.config['str_dst_dir']+self.config['str_posting_file_name']
        self.map_file  = self.config['str_dst_dir']+self.config['str_doc_id_file_name']
        
    
    def get_posts(self, line_index, how_many=1):
        result= OrderedDict()
        with open(self.post_file, 'r') as f:
            f.seek(line_index * self.config['post_block_len'] , 0)
            raw_lines=f.read(how_many * self.config['post_block_len'])
        
        lines= raw_lines.splitlines()
        for line in lines:
            parts = line.split()
            result[int(parts[0])]=parts[1]
        return result

    def readlines(self, fname, block_size, line_index, how_many=1):
        result=''
        with open(fname, 'r') as f:
            f.seek(line_index * block_size,0)
            result += f.read(how_many * block_size)
        return result
        
    
    def search(self, key):
        hash_value = FNVHash(key) % self.config['ht_len']        
        dict_entry = None
        
        while True:
            #read 7 lines instead of 1 line, since cost is same (1 block read) but minimize further call
            received_lines= self.readlines(self.dict_file, self.config['dict_block_len'], hash_value, 7)
            lines = received_lines.splitlines()
            for line in lines:
                line = line.strip()
                
                #index is empty...so key word does not exist.
                if not line: return False
                
                if line.startswith(key[:self.config['token_len_in_file']]):
                    parts= line.split()
                    dict_entry = DictEntry(key= key, num_docs = int (parts[1].strip()), 
                               start_index= int(parts[2].strip()))
#                    print '{0} exists in {1} files \n'.format(key, dict_entry.num_docs)
                    break
            if dict_entry: break
        
        #read post file
        posts= self.get_posts(dict_entry.start_index, dict_entry.num_docs)
        
        #will be commented
#        for did in posts.keys():            
#            print 'in "{0}" (id:{1}) with weight {2}'.format(self.get_file_name(did), did, posts[did])            
        
        return posts
    
    def get_file_name(self, doc_id):       
            return self.readlines(self.map_file, self.config['doc_map_block_len'], doc_id).split()[1].strip()
            
            
        
        