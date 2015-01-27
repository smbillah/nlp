#!/usr/bin/env python

'''
Created on Feb 23, 2012

@author: Masum
'''

from hashtable import query_processor
from myparser import Inverter
from myparser import src_dir, dst_dir
from myparser import parse
from mycollection import argparse

class SearchEngine():
    config= {}
    
    def __init__(self):
        self.read_config()
        self.qp = query_processor(self.config)        
        
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
               

    def build_index(self):
        _ = Inverter(self.config)
            
    
    def print_not_found(self, query):        
            print  'sorry. "{0}" does not exist in our index'.format(query)
            return
        
    def search_query(self, raw_query, weighted = False):
        #query parsing and expanding
        query , qweight =[], {}
        if not weighted:
            query = parse(raw_query, self.config)
            if not query: self.print_not_found(raw_query); return        
            #assign equal weight to all terms
            qweight = dict([key_wt for key_wt in zip(query, [1.0/len(query)]*len(query))])
        else:
            raws = raw_query.split()
            weight=[]
            for i in range(0, len(raws),2):
                weight.append(float( raws[i].strip()))
                query.append(raws[i+1].strip())
            if not query: self.print_not_found(raw_query); return
            qweight = dict([key_wt for key_wt in zip(query, weight)])
                        
        
        #initialize the search bucket
        buckets= {}
        count = 0        
        for key in query:
            posts = self.qp.search(key)
            if not posts: continue            
            if count >= self.config['bucket_size']: break
            for doc_id, rtf_idf in posts.iteritems():            
                    buckets[doc_id]= buckets.get(doc_id,0.0) + qweight[key] * float(rtf_idf)
            count +=1                    
                

        if not buckets: self.print_not_found(raw_query); return
                   
        print "displaying top 10 results for '{0}':".format(' '.join(query))
        count =0 
        for doc_id, weight in sorted(buckets.iteritems(), key = lambda(k,v): (v,k), reverse = True):            
            if count< self.config['output_size']:                
                print "in '{0:s}' (id:{1:0>3d}) with weight {2:f}".format(self.qp.get_file_name(doc_id), doc_id, weight)
                count +=1
            else: break

        

#import argparse
if __name__=='__main__':
    
    args = argparse.ArgumentParser(description="This is Syed's search program for HW4")
    args.add_argument("-o", "--output", dest="dst_dir",
                   help="The directory where output goes", default="")
    args.add_argument("-s", "--source", dest="src_dir",
                   help="The directory where raw files reside", default="")
    
    args.add_argument("-i", "--index", dest="index",
                   help="Re-index of all files - and overwrite existing dict and post files, i.e. -i all", default="")
    args.add_argument("-q", "--query", dest="query",
                   help="One or more search word (space separated), i.e  -q uark  susan@uark.edu", nargs= "*", default = "")
    args.add_argument("-wq", "--wquery", dest="wquery",
                   help="Weighted one or more search word (space separated), i.e  -wq .3 cat .3 dog .4 fish", nargs= "*", default = "")
    
    args = args.parse_args()
    src_dir = args.src_dir
    dst_dir = args.dst_dir
    if not args.index and not args.query and not args.wquery:
        print 'Invalid or No arguments. Try with -h for help!!'
    else:
        nlp = SearchEngine()
        if args.index: nlp.build_index()
        if args.query: nlp.search_query(' '.join(args.query))
        if args.wquery: nlp.search_query(' '.join(args.wquery), True)
        print 'Done!'

#    nlp = SearchEngine()
#    nlp.search_query('.8 susan .1 uark .1 edu', True )
#    print 'Done!'

