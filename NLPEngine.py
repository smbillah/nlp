#!/usr/bin/env python

'''
Created on Feb 23, 2012

@author: Masum
'''

from myparser import BiGram
from myparser import src_dir, dst_dir
from mycollection import argparse
from collections import defaultdict
from mycollection import OrderedDict
from stats import chisqure, likelihood_ratio


class NLPEngine():
    config= {}
    
    def __init__(self):
        self.read_config()        
        
    def read_config(self, name="config.txt"):        
        with open(name, 'r') as f:
            for line in f:
                if not line.strip(): continue
                params = line.split(':')
                value=params[0].strip()                
                if value.startswith('str'):
                    self.config[value]= params[1].strip()
                else:
                    self.config[value]= int(params[1].strip())
                
        stop_words = self.config['str_stop_list'].split()
        self.config['str_stop_list']=stop_words
        self.config['post_block_len']= \
            self.config['file_id_encoding_len']+1+ self.config['term_wt_decimal_len']+1+ self.config['term_weight_len']+1
        self.config['doc_map_block_len']= self.config['file_id_encoding_len']+1+ self.config['file_name_len']+ 1
        self.config['dict_block_len']= \
            self.config['token_len_in_file']+ 1 + self.config['file_occurance_encoding_len']+ 1+ self.config['posting_start_len']+1
        
        if src_dir: self.config['str_src_dir'] = src_dir
        if dst_dir: self.config['str_dst_dir'] = dst_dir
     
    def build_bigram_index(self):
        _ = BiGram(self.config)
    
    def load_bigrams(self):
        biht= OrderedDict() #bigram hash-table
        tht= defaultdict(int) # token hash-table
        
        
        i=0
        with open(self.config['str_dst_dir']+self.config['str_doc_id_file_name'], 'r') as f:            
            for line in f:
                i += 1;
                parts= line.strip().split(' ')
                count = int(parts[2]);
                if count >10:
                    biht[(parts[0],parts[1])] = int(parts[2])
                                                
        with open(self.config['str_dst_dir']+'all_tokens.txt', 'r') as f:
            for line in f:
                parts= line.strip().split(' ')
                tht[parts[0]] = int(parts[1])                                                        
#        print 'bigrams loading complete!';
        return biht, tht, i;
    
    def compute_chi_square(self):
        biht, tht, n = self.load_bigrams()
        for k in biht:
            chi = chisqure(biht[k], tht[k[0]], tht[k[1]], n)
            biht[k] = chi
        self.write_file_map(biht, 'chi_colocation.txt')
        
    
    def compute_likelihood(self):
        biht, tht, n = self.load_bigrams()
        for k in biht:
            lamda = likelihood_ratio(biht[k], tht[k[0]], tht[k[1]], n);
            biht[k] = lamda
        self.write_file_map(biht, 'likelihood_colocation.txt')
    
    def write_file_map(self, ht, file_name):        
        with open(self.config['str_dst_dir']+  file_name,'wb+') as f:
            for words, count in sorted(ht.iteritems(), key=lambda (k,v): (v,k), reverse= True):
                f.write(words[0]+" "+words[1]+" "+str(count)+"\n")

    
#import argparse
if __name__=='__main__':    
    args = argparse.ArgumentParser(description="This is Syed's NLP program")
    args.add_argument("-o", "--output", dest="dst_dir",
                   help="The directory where output goes", default="")
    args.add_argument("-s", "--source", dest="src_dir",
                   help="The directory where raw files reside", default="")
    
    args.add_argument("-nlp", "--nlp", dest="bigrams",
                   help="index of all bigrams in src directory, or compute colocaiton. e.g, -nlp bigrams, -nlp colocation", default="")
           
    args = args.parse_args()
    src_dir = args.src_dir
    dst_dir = args.dst_dir
    
    if not args.bigrams:
        print 'Invalid or No arguments. Try with -h for help!!'
    else:
        nlp = NLPEngine()
        if args.bigrams:
            if args.bigrams.startswith('bigrams'): 
                nlp.build_bigram_index()
            
            if args.bigrams.startswith('colocation'):                 
                nlp.compute_chi_square()
                nlp.compute_likelihood()                            
        print 'Done!'

#    nlp = SearchEngine()
#    nlp.search_query('.8 susan .1 uark .1 edu', True )
#    print 'Done!'

