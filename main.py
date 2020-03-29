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
    

