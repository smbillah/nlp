'''
Created on Feb 21, 2013

@author: Masum
'''

from math import log
from math import sqrt

# a = new; b= company
def chisqure(both_ab, a, b, n):
    # create 2x2 array 
    o11 = both_ab;
    o21 = a - both_ab;    
    o12 = b - both_ab;
    o22 = n - a - b - both_ab;    
    return 1.0*n*(o11*o22 - o12*o21)*(o11*o22 - o12*o21)/((o11+o12)*(o11+o21)*(o12+o22)*(o21+o22))

def chisqure2(both_ab, a, b, n):
    # create 2x2 array 
    o11 = both_ab;
    o21 = a - both_ab;    
    o12 = b - both_ab;
    o22 = n - a - b - both_ab;    
    return 1.0*n*(o11*o22 - o12*o21)*(o11*o22 - o12*o21)/((o11+o12)*(o11+o21)*(o12+o22)*(o21+o22))
    
def likelihood_ratio(c12, c1, c2, n):
    p = 1.0*c2/n
    p1 = 1.0*c12/c1
    p2 = 1.0*(c2-c12)/(n-c1) 
    
    if (p1 - 1.0) == 0.0: p1 = 0.999999999999999 
    if p2 == 0.0: p2 = 4.9406564584124654e-24; 
    
    lamda = -1    
    try:
        lamda = 1.0*( (c12*log(p)  + (c1-c12)*log(1-p))  + ((c2-c12)*log(p)  + (n-c1-c2+c12)*log(1-p))- (c12*log(p1) + (c1-c12)*log(1-p1)) - ((c2-c12)*log(p2) + (n-c1-c2+c12)*log(1-p2)));        
        #print p, p1, p2, 'doing my job'
    except:
        print p, p1, p2, 'not doing my job'
        
        pass
               
    return -2*lamda;


def t_test(n_ab, n_a, n_b, n):
    p_a= 1.0*n_a/n;
    print 'p(w1): ', p_a
    p_b= 1.0*n_b/n;
    print 'p(w2): ', p_b
    u = p_a*p_b;
    print 'mean: ', u
    x = 1.0*n_ab/n;
    print 'x_bar: ', x
    t = (x-u)/sqrt(x/n);
    print 't-value: ', t
    return t;  

def mutual_information(n_ab, n_a, n_b, n):
    p_a= 1.0*n_a/n;
    print 'p(x): ', p_a
    p_b= 1.0*n_b/n;
    print 'p(y): ', p_b
    p_ab = 1.0*n_ab/n;
    print 'p(x,y): ', p_ab
    
    i = log(p_ab/(p_a*p_b),2);
    print 'I(X;Y): ', i
    return i;  
    
    

#test
#mutual_information(20, 42, 20, 14307668)
#mutual_information(10, 1000, 1000, 100000)
#print '---'
#mutual_information(45, 50, 100, 100000)
#print '---'
#mutual_information(1, 1, 1, 100000)


#---
#t_test(10, 1000, 1000, 100000)
#print '---'
#t_test(45, 50, 100, 100000)
#print '---'
#t_test(1, 1, 1, 100000)
print 'bigrams'
print chisqure(8, 15828, 4675, 14307668)
#print likelihood_ratio(10, 379, 932, 14307668)