'''
Created on Mar 11, 2012

@author: Masum
'''

import re
from collections import defaultdict 

#============ global regex =============================
is_word = re.compile("[a-zA-Z_]+$")
delim = re.compile(" |\t|\.|-|:|\@|\\|/|,|;|\"|!|\*]+")

#================path ==============================
dst_dir = ''
src_dir = ''

#============ global hash variables =====================
doc_id= defaultdict(int)
term_count= defaultdict(int)

def parse(line, config):    
    line =line.strip()
    if not line: return []
    
    tokens= []
    for word in delim.split(line):                
        word = word.strip("~`$%^&()[]|<>=+-_/").lower()
        if word in config['str_stop_list']: continue
        if config['min_token_len']<= len(word) <= config['max_token_len'] and is_word.match(word):
            tokens.append(word)
    return tokens