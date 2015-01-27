'''
Created on Mar 10, 2012

@author: Masum
'''

def hash_function(key):
    index = 0
    for c in key: 
        index = 19 * index + ord(c)
    return index

def hash_function_offset(key, total_size, offset=1):
    index = 0
    for c in key: 
        index = 19 * index + ord(c)
        index %= total_size
    return (index + 1) % total_size

def RSHash(key):
    a    = 378551
    b    =  63689
    index =      0
    for i in range(len(key)):
        index = index * a + ord(key[i])
        a = a * b
    return index


def JSHash(key):
    index = 1315423911
    for i in range(len(key)):
        index ^= ((index << 5) + ord(key[i]) + (index >> 2))
    return index


def PJWHash(key):
    BitsInUnsignedInt = 4 * 8
    ThreeQuarters     = long((BitsInUnsignedInt  * 3) / 4)
    OneEighth         = long(BitsInUnsignedInt / 8)
    HighBits          = (0xFFFFFFFF) << (BitsInUnsignedInt - OneEighth)
    index              = 0
    test              = 0

    for i in range(len(key)):
        index = (index << OneEighth) + ord(key[i])
        test = index & HighBits
        if test != 0:
            index = (( index ^ (test >> ThreeQuarters)) & (~HighBits));
    return (index & 0x7FFFFFFF)


def ELFHash(key):
    index = 0
    x    = 0
    for i in range(len(key)):
        index = (index << 4) + ord(key[i])
        x = index & 0xF0000000
        if x != 0:
            index ^= (x >> 24)
            index &= ~x
    return index


def BKDRHash(key):
    seed = 131 # 31 131 1313 13131 131313 etc..
    index = 0
    for i in range(len(key)):
        index = (index * seed) + ord(key[i])
    return index


def SDBMHash(key):
    index = 0
    for i in range(len(key)):
        index = ord(key[i]) + (index << 6) + (index << 16) - index;
    return index


def DJBHash(key):
    index = 5381
    for i in range(len(key)):
        index = ((index << 5) + index) + ord(key[i])
    return index


def DEKHash(key):
    index = len(key);
    for i in range(len(key)):
        index = ((index << 5) ^ (index >> 27)) ^ ord(key[i])
    return index


def BPHash(key):
    index = 0
    for i in range(len(key)):
        index = index << 7 ^ ord(key[i])
    return index


#the winner :D
def FNVHash(key):
    fnv_prime = 0x811C9DC5
    index = 0
    for i in range(len(key)):
        index *= fnv_prime
        index ^= ord(key[i])
    return index


def APHash(key):
    index = 0xAAAAAAAA
    for i in range(len(key)):
        if ((i & 1) == 0):
            index ^= ((index <<  7) ^ ord(key[i]) * (index >> 3))
        else:
            index ^= (~((index << 11) + ord(key[i]) ^ (index >> 5)))
    return index


