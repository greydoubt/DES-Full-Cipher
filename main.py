


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
# add this to final product


# NOTE: this says BIT not BYTE
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
test_init = Permutation(test_inputbitstr, BookInitPermOrder)
# INVERT (SHOULD BE THE SAME AS INITIAL BIT STRING)
test_inverse = Permutation(test_init, BookInvInitPermOrder)
print(test_inputbitstr == test_inverse)

print("PART THREE:")

somestring = test_init

def split(somestring):
	return somestring[:int(len(test_init)/2)],somestring[int(len(test_init)/2):]

LHS, RHS = split(somestring)
print (LHS, RHS)


# EXPANSION FUNCTION:

E_TABLE = [32,1,2,3,4,5,4,5,6,7,8,9,8,9,10,11,12,13,12,13,14,15,16,17,16,17,18,19,20,21,20,21,22,23,24,25,24,25,26,27,28,29,28,29,30,31,32,1]

def Expansion(inputbitstr32, e_table):
    # the input string is 32 bits long and the output string will be 48 bits long or
    # to be more exact, it will be as long as the e_table (which is 48 bits for DES)
 
    # create output empty string
    outputbitstr48 = ''

    for i in e_table:
      outputbitstr48 += inputbitstr32[i-1]

    # add proper elements from the inputbitstr32 according to the e_table
    
    return outputbitstr48

# test expansion function:
expanded = Expansion(RHS, E_TABLE)
print("Expanded: " + str(expanded))


# XOR FUNCTION:
def XORbits(bitstr1, bitstr2):
    # Both bit strings should be the same length
    # output will be a string with the same length
    xor_result = '' # this was None originally

    for i in range(len(bitstr1)):
      if bitstr1[i] == bitstr2[i]:
        xor_result += '0'
      else:
        xor_result += '1'
    
    return xor_result

# test XOR function:
#test_xor_result = XORbits('0001', '0000')

#print(test_xor_result)


# intermediate permutation table:
# this runs AFTER the S-Box 
MiddlePermOrder = [16,7,20,21,29,12,
                  28,17,1,15,23,26,5,
                  18,31,10,2,8,24,14,
                  32,27,3,9,19,13,30,
                  6,22,11,4,25]
#print(MiddlePermOrder)

# as per the notes, this is the same as the function already written, just using a different perm box 

test_middleperm = Permutation(expanded, MiddlePermOrder)
print(test_middleperm)

# prior to going into sbox, slice it up:


# this is in F Function as well:
boxstr = expanded
eightboxes = list(map(''.join, zip(*[iter(boxstr)]*6)))
print(eightboxes)


#blocks = [prebox[:6], prebox[6:12], prebox[12:18], prebox[18:24], prebox[24:30], prebox[30:36], prebox[36:42], prebox[42:]]

SBOX = [
# Box-1
[
[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
[0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
[4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
[15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]
],
# Box-2

[
[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
[3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
[0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
[13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]
],

# Box-3

[
[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
[13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
[13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
[1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]

],

# Box-4
[
[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
[13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
[10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
[3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]
],

# Box-5
[
[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
[14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
[4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
[11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]
],
# Box-6

[
[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
[10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
[9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
[4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]

],
# Box-7
[
[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
[13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
[1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
[6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]
],
# Box-8

[
[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
[1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
[7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
[2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]
]

]

DECtoBIN4 = {0: '0000',
            1: '0001',
            2: '0010',
            3: '0011',
            4: '0100',
            5: '0101',
            6: '0110',
            7: '0111',
            8: '1000',
            9: '1001',
            10: '1010',
            11: '1011',
            12: '1100',
            13: '1101',
            14: '1110',
            15: '1111'}

DECtoBIN2 = {0: '00',
            1: '01',
            2: '10',
            3: '11'}            


print(eightboxes[3])
print(eightboxes[3][0]+eightboxes[3][-1])
print(eightboxes[3][1:5])

# this will be called in a for loop from 0-7
def sbox_lookup(input6bitstr, sboxindex):
    # find the row index (0-3)
    # find the col index (0-7)
    
    rowbin = input6bitstr[0]+input6bitstr[-1] # this is 00 through 11; get first/last chars
    colbin = input6bitstr[1:5] # get middle 4 chars
    
    
    row = list(DECtoBIN4.keys())[list(DECtoBIN2.values()).index(rowbin)]

    col = list(DECtoBIN4.keys())[list(DECtoBIN4.values()).index(colbin)]

    sbox_value = SBOX[sboxindex][row][col]
    
    # Need to convert to 4 bits binary string    
    return DECtoBIN4.get(sbox_value)

# test case: 011011 for S5 will be [2,14] = 9
print(SBOX[4][1][13])

# to go from key to value:
#print(DECtoBIN4.get(1))

#print(eightboxes[7][])

print(sbox_lookup('011011', 4))

#to go from value to key:
#print(list(DECtoBIN4.keys())[list(DECtoBIN4.values()).index('1100')])

print("PART FOUR")
# F: the Round Function:

def functionF(bitstr32, keybitstr48):
    # basically:
    # expand > XOR > box > install NSA backdoor > permute
    expanded = Expansion(bitstr32, E_TABLE)
    xored = XORbits(expanded, keybitstr48)


    eightboxes = list(map(''.join, zip(*[iter(xored)]*6)))

    #print(expanded)
    #print(xored)

    sboxresults = []

    for i in range(len(eightboxes)):
      #print(str(i) + ' ' + eightboxes[i])
      sboxresults.append(sbox_lookup(eightboxes[i], i))

    middleperm = Permutation(''.join(sboxresults), MiddlePermOrder)

    # return the result
    outbitstr32 = middleperm
    return outbitstr32


print("Does not have active keys:")
print(functionF(RHS, '000100101010101010010100010101010010101001010010'))


print("Section 2: GENERATE KEYS")

dummykey='000100101010101010010100010101010010101001010010'

print(len(dummykey))

ROTATIONS = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]


def des_keygen(C_inp, D_inp, roundindex):
    # Implement Figure 6
    
    key48 = ''
    C_out = ''
    D_out = ''

    return key48, C_out, D_out