print("PART ONE")

# Helpful byte and bit processing
# We typically read files to encode in binary format as a byte sequence and below is some of
# the many ways you can manipulate the byte values and convert between bytes, bits, lists, etc.

# Here I'm limiting the example byte sequence to one 32bits block. In reality you will
# break your original byte sequence to as many such 64bits blocks as needed and process
# them one by one
byteseq = b'\x12\xfa\xaa\x0f'

# convert to list of integers
intlist = [int(b) for b in byteseq]
print("intlist: ",intlist)

# convert the integers list to list of 8 bits
bitslist1 = [bin(i)[2:].zfill(8) for i in intlist]
print("bitslist1: ",bitslist1)
# or directly from the bytes
bitslist2 = [bin(int(b))[2:].zfill(8) for b in byteseq]
print("bitslist2: ",bitslist2)

# convert to one big binary string
allbits = ''.join(bitslist2)
print("allbits: ",allbits)

# Note: we can also convert the string of bits into a list of bits
# For cases where we need to insert some bits into a bit sequence it's
# easier to work with lists in python. This is not the most efficient
# implementation for real cipher implementations in terms of execution
# speed but is more clear for our educational purposes
allbitslist = [b for b in allbits]
print("allbitslist: ",allbitslist)

# for now, I'll use the zfill function for strings to add enough '0's to the beginning of
# allbits string to make its length 48 (i.e., Expansion)
allbits48 = allbits.zfill(48)
print("allbits48: ",allbits48)

# break into 6 bit blocks
b6list = [allbits48[i:i+6] for i in range(0,len(allbits48), 6)]
print("b6list: ", b6list)

# isolating the middle 4 bits of a 6 bit block and convert to integer
# example: 110110 should result in 1011 which is 11 decimal
bitseq6 = '110110'
midint = int(bitseq6[1:5],base=2)  # int() function converts the string to decimal and 2 means string is a binary number
print("midint: ", midint)

# isolating first and last bits of the 6 bit string and converting to decimal
outerint = int(bitseq6[0]+bitseq6[5],base=2)
print("outerint: ",outerint)


# Given the above transformations, we can define all types of transformation utility functions
# for example a function to convert a given byte sequence to a string representation of bits
def byteseq2binstr(byteseq):
    # first convert to a list string binary representations of each byte
    bitslist2 = [bin(int(b))[2:].zfill(8) for b in byteseq]
    
    # then merge all those strings
    allbitsstr = ''.join(bitslist2)
    
    return allbitsstr
    


print("PART TWO")

# Initial Permutation and inverse permutaion operatoins can be easily performed 
# using lists and proper indexing of the elements of the lists in Python 

# Let's define the order of the elements at the output of the Initial Permutation (IP) stage
# in the following list (we subtract the values in the book by 1 since we always
# index array elements from 0 upward) 
BookInitPermOrder = [58,50,42,34,26,18,10,2,
                   60,52,44,36,28,20,12,4,
                   62,54,46,38,30,22,14,6,
                   64,56,48,40,32,24,16,8,
                   57,49,41,33,25,17,9,1,
                   59,51,43,35,27,19,11,3,
                   61,53,45,37,29,21,13,5,
                   63,55,47,39,31,23,15,7]

InitPermOrder = [x-1 for x in BookInitPermOrder]

# Same can be done for Inverse Initial Permuation
BookInvInitPermOrder = [40,8,48,16,56,24,64,32,
                   39,7,47,15,55,23,63,31,
                   38,6,46,14,54,22,62,30,
                   37,5,45,13,53,21,61,29,
                   36,4,44,12,52,20,60,28,
                   35,3,43,11,51,19,59,27,
                   34,2,42,10,50,18,58,26,
                   33,1,41,9,49,17,57,25]

InvInitPermOrder = [x-1 for x in BookInvInitPermOrder]


# The permutation table basically says the first element of the output data should take the 
# value of the 32nd element of the input data or thrid element of the output data sould take the
# value of the second element of the input data. In other words, InitPerm is a function that takes
# a 64 bit byte array as input and returns another 64 but array as output

# Let's manually create an 8 byte long byte sequence (in your homework you will read the file data
# automatically as byte sequence)
inputstr = 'a string'
inputbytes = bytes(inputstr, 'utf-8')


# let's convert the input bytes block to a string representation of its bits
inputbitstr = byteseq2binstr(inputbytes)
print('inputbitstr: ',inputbitstr)

# Now we can use the InitPermData to pick which bits of this input bits string goes to which bits of 
# the permutated bits string
# We first create the permutated bits as a list since we can easily use python's list comprehensions operations
inputbitslistperm = [inputbitstr[b] for b in InitPermOrder]
inputbitstrperm = ''.join(inputbitslistperm)
print('inputbitslistperm: ',inputbitslistperm)
print('inputbitstrperm: ',inputbitstrperm)

# Now you can put the above inside this function so that it can be called to perform
# both initial and inverse initial permutations for DES
# You may need some conversion from byteseq to bitstring and reverse to use this function with your
# feistel implementation


print("TEST PART TWO:")

def Permutation(bitstr, permorderlist):
    permedbitstr = ''
    
    for i in permorderlist:
      permedbitstr += bitstr[i-1]

    return permedbitstr

# string -> bytes -> binary
test_inputstr = '0123456789ABCDEF'
test_inputbytes = bytes(test_inputstr, 'utf-8')
test_inputbitstr = byteseq2binstr(inputbytes)
print('inputbitstr: ', test_inputbitstr)

# INITIAL PERMUTATION: 
test_out = Permutation(test_inputbitstr, BookInitPermOrder)
# INVERT (SHOULD BE THE SAME AS INITIAL BIT STRING)
test_inv = Permutation(test_out, BookInvInitPermOrder)
print(test_inputbitstr == test_inv)

