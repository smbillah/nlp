'''
Created on Mar 13, 2013

@author: Masum
'''

import re
from math import log
from collections import defaultdict
import os
import sys

def replace_tag2(line_text, tag, pseudoword, line_no, context_size=2):  # <tag "532675">    
    header = str(line_no) + ":" + pseudoword + ":" + str(tag) + "\n";
    line_text = re.sub('<tag "\d+">\s*\w+</>', pseudoword, line_text, 1)
    line_text = re.sub('[.|"|,|;|:|!|(|)|?|`|\']', '', line_text);    
    parsed = [tok.lower() for tok in line_text.split(' ') if len(tok)>2];
    contexts = []        

    index = 0;
    try:
        index = parsed.index(pseudoword);
    except:
        #print line_text+'\n'
        return None;
        
    #add left tokens
    if (index>=context_size):
        contexts.extend(parsed[index-context_size : index]) 
    #add right tokens
    if len(parsed)>(index+context_size):
        contexts.extend( parsed[index+1:index+1+context_size]) 
    #print contexts
    line_text = header + (' ').join(contexts) + "\n"        
    return line_text; 

def process_file(file_in, max_lines, file_out, pseudoword, sense, start_line, context_size):
    mode = 'w+' if (start_line==0) else 'a';
    f_train = open(file_out+".train.txt", mode);
    f_test = open(file_out+".test.txt", mode);
    curr_line = 0; 
    tokenized_line="";
    
    with open(file_in, 'r') as f:
        line_text = ""; 
        within_a_line = False
        for line in f:            
            if re.match("\n", line):            
                # if start_line>3:break;
                within_a_line = False;
                tokenized_line = replace_tag2(line_text, sense, pseudoword, start_line, context_size)                
                if tokenized_line:                     
                    if curr_line<max_lines*.8:
                        f_train.write(tokenized_line);
                    else:
                        f_test.write(tokenized_line);
                    start_line += 1;
                curr_line+=1;
                line_text = ""            
                continue;                
            
            if re.match('\d+', line):            
                within_a_line = True;
                continue;
            
            if within_a_line:
                line_text += line.strip() + " ";
    f_train.close();
    f_test.close();
    return start_line;
# end        

def build_corpus(file_in1, line_no1,file_in2, line_no2,file_out, pseudoword, contex_size):        
    # 1st file            
    line_no = process_file(file_in1, line_no1,file_out, pseudoword , 0, 0, contex_size);
    # 2nd file
    process_file(file_in2, line_no2,file_out, pseudoword , 1, line_no, contex_size);
# end;


def run_traning(file_in, pseudoword):
    hashes = [defaultdict(float), defaultdict(float)] 
    sense_types= [0,1];
    count_senses=[0.0, 0.0];
    current_sense = -1
        
    with open(file_in, 'r') as f:
        line_no=0;         
        for line in f:            
            #if line_no>3:break;                                
            m = re.match("\d+:"+pseudoword+":(\d)", line) #0:accidentwooden:0
            if m:            
                current_sense = int(m.group(1))                
                count_senses[current_sense]+=1;                
                line_no += 1;                                    
            else:
                for context in  line.strip().split(" "):
                    hashes[current_sense][context]+=1;                
        #priors
        priors = [1.0*count_senses[0]/(count_senses[0]+count_senses[1]), 1.0*count_senses[1]/(count_senses[0]+count_senses[1])];                
        
        #conditionals
        for sense in sense_types:
            for context in hashes[sense]:
                hashes[sense][context] = 1.0*hashes[sense][context]/count_senses[sense]; 
    
    #print hashes;    
    return sense_types, priors,hashes ;


def run_disambiguation(file_train, file_test, pseudoword, context_size):
    sense_types, priors, conditionals =  run_traning(file_train, pseudoword);    
    actual_sense = -1;
    predicted_sense = -1;
    scores  = [0.0, 0.0];
        
    #print "priors: ", priors;
    #print "sense types: ",sense_types;
    #print "training instances: ",count_senses
    #print conditionals[1];
    
    factor = 10000;
    count_corrects=0;
    count_wrong= 0;
    
    with open(file_test, 'r') as f:
        line_no=0;         
        for line in f:                                                        
            m = re.match("\d+:"+pseudoword+":(\d)\n", line) #0:accidentwooden:0
            if m:            
                actual_sense = int(m.group(1))                                
                line_no += 1;                                    
            else:
                contexts = line.strip().split(" ");                
                for sense in sense_types:
                    scores[sense] = log(priors[sense]); 
                    
                    for context in contexts:                        
                        if context in conditionals[sense]:
                            prob = conditionals[sense][context]
                            scores[sense] += log((prob*factor+1.0)/(factor+context_size));
                        else:
                            scores[sense] += log(1.0/factor);                                                        
                        #end inner for
                    #end sense
                #end outer for
                if scores[0]>scores[1]:
                    predicted_sense = 0;
                else:
                    predicted_sense = 1;
                
                #calculate accuracy                
                if predicted_sense==actual_sense:
                    count_corrects+=1;
                else:
                    count_wrong+=1;
            #print actual_sense, predicted_sense;
        #print 'accuracy: ', count_corrects*100.0/(count_corrects+count_wrong), '\n';
        print context_size, ' ',count_corrects*100.0/(count_corrects+count_wrong);
    

def run_pair(w1, line_no1, w2, line_no2, context_count):
    build_corpus('wsd/'+w1+'.cor', line_no1,'wsd/'+w2+'.cor', line_no2,'wsd/'+w1+w2+'.bag', w1[2:]+w2[2:], context_count)
    run_disambiguation('wsd/'+w1+w2+'.bag.train.txt', 'wsd/'+w1+w2+'.bag.test.txt',w1[2:]+w2[2:], context_count);


def hw3():
    for i in range(1,20):
        #print 'for run', i,':'; 
        run_pair('4.amaze', 319,'4.behaviour', 1003, i);    
        #run_pair('3.sack', 296,'3.sanction', 101, i);    
        #run_pair('2.knee', 477,'2.onion', 29, i);
        #run_pair('1.accident', 1303,'1.wooden', 370, i);
#end


def get_file_chars(fname):
    alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9'];
    alpha_dict = defaultdict(float);
    
    total=0
    with open(fname, 'r') as f:
        for line in f:
            for c in line.lower():
                total+=1;
                if c in alphabet:
                    alpha_dict[c] += 1.0;            
    return alpha_dict;    
#end

def entropy(alpha_dict):
    info = 0.0
    total = 0. + sum(alpha_dict.values())
    for c in alpha_dict:
        #print c, ' ', alpha_dict[c] 
        p = alpha_dict[c]/total;        
        info += -p*log(p, 2);
    print 'entropy is: ',info;

def kldiv(_s, _t):
    if (len(_s) == 0):return 1e33
    if (len(_t) == 0):return 1e33

    ssum = 0. + sum(_s.values())
    tsum = 0. + sum(_t.values())

    vocabdiff = set(_s.keys()).difference(set(_t.keys()))
    lenvocabdiff = len(vocabdiff)

    """ epsilon """
    epsilon = min(min(_s.values())/ssum, min(_t.values())/tsum) * 0.001

    """ gamma """
    gamma = 1 - lenvocabdiff * epsilon
    
    """ Check if distribution probabilities sum to 1"""
    sc = sum([v/ssum for v in _s.itervalues()])
    st = sum([v/tsum for v in _t.itervalues()])

    if sc < 9e-6:
        print "Sum P: %e, Sum Q: %e" % (sc, st)
        print "*** ERROR: sc does not sum up to 1. Bailing out .."
        sys.exit(2)
    if st < 9e-6:
        print "Sum P: %e, Sum Q: %e" % (sc, st)
        print "*** ERROR: st does not sum up to 1. Bailing out .."
        sys.exit(2)

    div = 0.
    for t, v in _s.iteritems():
        pts = v / ssum
        ptt = epsilon
        if t in _t:
            ptt = gamma * (_t[t] / tsum)
        ckl = (pts - ptt) * log(pts / ptt)
        div +=  ckl
    return div
#end of kldiv


        
def get_corpus_count(corpus_path):
    total_freq = defaultdict(float);

    for filename in os.listdir (corpus_path):                
        #print filename
        file_count = get_file_chars(os.path.abspath(corpus_path)+os.path.sep+filename);
        for k in file_count:
            total_freq[k] += file_count[k];
        #print '\n'
    #get_file_chars("kl/English1/test.txt");
    #for k in total_freq:
        #print k, ' ', total_freq[k];
    return total_freq


corpus_path1 = "kl/English1/"
corpus_path2 = "kl/English2/"
corpus_path3 = "kl/French1/"

print "KL-divergence <1,2>:", kldiv(get_corpus_count(corpus_path1),get_corpus_count(corpus_path2));
print "KL-divergence <2,1>:", kldiv(get_corpus_count(corpus_path2),get_corpus_count(corpus_path1));

print "KL-divergence <1,3>:", kldiv(get_corpus_count(corpus_path1),get_corpus_count(corpus_path3));
print "KL-divergence <3,1>:", kldiv(get_corpus_count(corpus_path3),get_corpus_count(corpus_path1));

print "KL-divergence <2,3>:", kldiv(get_corpus_count(corpus_path2),get_corpus_count(corpus_path3));
print "KL-divergence <3,2>:", kldiv(get_corpus_count(corpus_path3),get_corpus_count(corpus_path2));


    