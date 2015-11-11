# -*- coding: utf8 -*-

class Bitarray:

    def __init__(self, size):
        """ Create a bit array of a specific size """
        self.size = size
        self.bitarray = bytearray(size/8) #创造了这么大的位数租空间 注意要除以8 因为1byte = 8bit
 
    def set(self, n):
        """ Sets the nth element of the bitarray """

        index = n / 8
        position = n % 8
        self.bitarray[index] = self.bitarray[index] | 1 << (7 - position)

    def get(self, n):
        """ Gets the nth element of the bitarray """
        
        index = n / 8
        position = n % 8
        return (self.bitarray[index] & (1 << (7 - position))) > 0 


def BKDRHash(key,seed,m):
        hashValue = 0
        for i in range(len(key)):
            hashValue = ( hashValue * seed ) + ord(key[i])
        return hashValue % m


class MyBloomFilter(object):
    """docstring for MyBloomFilter"""
    seeds = [31,7,15,127,131,1313,131311,1313113,1311113113,1731,71,177]
    def __init__(self, size,k = 8):
        self.bitmap = Bitarray(size)
        self.m = size
        self.k = k
    def add(self,key):  #增加key到我们的位图中
        #进行k次hash
        for i in range(self.k):
            hv = BKDRHash(key,MyBloomFilter.seeds[i],self.m)
            self.bitmap.set(hv)
    def lookup(self,key):
        for i in range(self.k):
            hv = BKDRHash(key,MyBloomFilter.seeds[i],self.m)
            if(not self.bitmap.get(hv)): return False
        return True


# mbf = MyBloomFilter(32000,8)

# mbf.add('asdddd')
# mbf.add('asdsdff')
# mbf.add('avvvvsad12334242')
# mbf.add('232321vvvv3fsdasdf')
# mbf.add('klklekr3r31ee1asd')

# while True:
#     strr = raw_input("Please input your str:__")
#     # for i in range(mbf.k):
#     #     hv = BKDRHash(strr,MyBloomFilter.seeds[i],mbf.m)
#     #     print hv,
#     print mbf.lookup(strr)








# if __name__ == "__main__":
#     bitarray_obj = Bitarray(32000)
#     for i in range(5):
#         print "Setting index %d of bitarray .." % i
#         bitarray_obj.set(i)
#         print "bitarray[%d] = %d" % (i, bitarray_obj.get(i))
#
#


