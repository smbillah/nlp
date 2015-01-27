'''
Created on Mar 10, 2012

@author: Masum
'''
from collections import namedtuple

RawEntry = namedtuple('RawEntry', 'key, post_dict')
DictEntry = namedtuple('DictEntry', 'key, num_docs, start_index')
