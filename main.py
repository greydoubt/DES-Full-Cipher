# File-based implementation of DES
# based on: 
# https://csrc.nist.gov/csrc/media/publications/fips/46/3/archive/1999-10-25/documents/fips46-3.pdf

# utility functions for byte and binary manipulation:
def byteseq2binstr(byteseq):
    # first convert to a list string binary representations of each byte
    bitslist2 = [bin(int(b))[2:].zfill(8) for b in byteseq]
    
    # then merge all those strings
    allbitsstr = ''.join(bitslist2)
    
    return allbitsstr

def binstr2byteseq(binstr):
    return int(binstr, 2).to_bytes((len(binstr) + 7) // 8, 'big')
    #return b''.join([chr(int(x, 2)) for x in binstr])
    #return chr(int(binstr, 2))
    '''v = int(binstr, 2)
    b = bytearray()
    while v:
        b.append(v & 0xff)
        v >>= 8
    return bytes(b[::-1])'''

def split(somestring):
    return somestring[:int(len(somestring)/2)], somestring[int(len(somestring)/2):]



# permutation tables: 
BookInitPermOrder = [58,50,42,34,26,18,10,2,
                   60,52,44,36,28,20,12,4,
                   62,54,46,38,30,22,14,6,
                   64,56,48,40,32,24,16,8,
                   57,49,41,33,25,17,9,1,
                   59,51,43,35,27,19,11,3,
                   61,53,45,37,29,21,13,5,
                   63,55,47,39,31,23,15,7]

InitPermOrder = [x-1 for x in BookInitPermOrder]

BookInvInitPermOrder = [40,8,48,16,56,24,64,32,
                   39,7,47,15,55,23,63,31,
                   38,6,46,14,54,22,62,30,
                   37,5,45,13,53,21,61,29,
                   36,4,44,12,52,20,60,28,
                   35,3,43,11,51,19,59,27,
                   34,2,42,10,50,18,58,26,
                   33,1,41,9,49,17,57,25]

InvInitPermOrder = [x-1 for x in BookInvInitPermOrder]



#inputbitslistperm = [inputbitstr[b] for b in InitPermOrder]
#inputbitstrperm = ''.join(inputbitslistperm)
#print('inputbitslistperm: ',inputbitslistperm)
#print('inputbitstrperm: ',inputbitstrperm)


def Permutation(bitstr, permorderlist):
    permedbitstr = ''
    
    for i in permorderlist:
      permedbitstr += bitstr[i-1]
    #inputbitslistperm = []
    #inputbitslistperm = [bitstr[b-1] for b in permorderlist]
    #inputbitstrperm = ''.join(inputbitslistperm)  

    return permedbitstr


# EXPANSION FUNCTION:

E_TABLE = [32,1,2,3,4,5,4,5,6,7,8,9,8,9,10,11,12,13,12,13,14,15,16,17,16,17,18,19,20,21,20,21,22,23,24,25,24,25,26,27,28,29,28,29,30,31,32,1]

def Expansion(inputbitstr32, e_table):
    # the input string is 32 bits long and the output string will be 48 bits long or
    # to be more exact, it will be as long as the e_table (which is 48 bits for DES)
 

    #print("calling expansion on: ")
    #print(len(inputbitstr32))
    #print(type(inputbitstr32))
    # create output empty string
    outputbitstr48 = ''

    for i in e_table:
      outputbitstr48 += inputbitstr32[i-1]

    # add proper elements from the inputbitstr32 according to the e_table
    
    return outputbitstr48


# XOR FUNCTION:
def XORbits(bitstr1, bitstr2):

    xor_result = ''

    for i in range(len(bitstr1)):
      if bitstr1[i] == bitstr2[i]:
        xor_result += '0'
      else:
        xor_result += '1'
    
    return xor_result


# intermediate permutation table:
# this runs AFTER the S-Box 
MiddlePermOrder = [16,7,20,21,29,12,
                  28,17,1,15,23,26,5,
                  18,31,10,2,8,24,14,
                  32,27,3,9,19,13,30,
                  6,22,11,4,25]


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
# end of s-boxes

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


# this will be called in a for loop from 0-7
def sbox_lookup(input6bitstr, sboxindex):
    # find the row index (0-3)
    # find the col index (0-7)
    
    rowbin = input6bitstr[0]+input6bitstr[-1] # this is 00 through 11; get first/last chars
    colbin = input6bitstr[1:5] # get middle 4 chars
    
    row = list(DECtoBIN2.keys())[list(DECtoBIN2.values()).index(rowbin)]

    col = list(DECtoBIN4.keys())[list(DECtoBIN4.values()).index(colbin)]

    sbox_value = SBOX[sboxindex][row][col]
    
    # Need to convert to 4 bits binary string    
    return DECtoBIN4.get(sbox_value)

#print("PART FOUR")
# F: the Round Function:

def functionF(bitstr32, keybitstr48):
    # basically:
    # expand > XOR > box > install NSA backdoor > permute

    expanded = Expansion(bitstr32, E_TABLE)
    xored = XORbits(expanded, keybitstr48)


    eightboxes = list(map(''.join, zip(*[iter(xored)]*6)))

    sboxresults = []

    for i in range(len(eightboxes)):
      sboxresults.append(sbox_lookup(eightboxes[i], i))

    outbitstr32 = Permutation(''.join(sboxresults), MiddlePermOrder)


    return outbitstr32



ROTATIONS = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

PC1=[57,49,41,33,25,17,9,1,58,50,42,34,26,18,10,2,59,51,43,35,27,19,11,3,60,52,44,36,63,55,47,39,31,23,15,7,62,54,46,38,30,22,14,6,61,53,45,37,29,21,13,5,28,20,12,4]

PC2=[14,17,11,24,1,5,3,28,15,6,21,10,23,19,12,4,26,8,16,7,27,20,13,2,41,52,31,37,47,55,30,40,51,45,33,48,44,49,39,56,34,53,46,42,50,36,29,32]

def des_keygen(C_inp, D_inp, roundindex):
    # Implement NIST key schedule diagram

    i = 0
    while i < ROTATIONS[roundindex]:
      #print("rotating: " + str(ROTATIONS[roundindex]))
      C_inp += C_inp[0]
      D_inp += D_inp[0]
      C_inp = C_inp[1:]
      D_inp = D_inp[1:]
      i += 1

    # PC2 to key
    key48 = Permutation(C_inp + D_inp, PC2)

    C_out = C_inp
    D_out = D_inp

    return key48, C_out, D_out

# getting into the sad waters bracing for the <FileNotFoundError>
# CIPHER

def des_round(LE_inp32, RE_inp32, key48):
    # LEinp and REinp are the outputs of the previous round
    # k is the key for this round which usually has a different 
    # value for different rounds

    # wiring diagram:
    # SWAP: LHS[i] = RHS[i-1], ie LE_out32 = RE_inp32
    # DROP: F(RHS[i-1])
    # XLOP:


    f_output = functionF(RE_inp32, key48)
    x_output = XORbits(f_output, LE_inp32)

    LE_out32 = RE_inp32 # = RE_inp32
    RE_out32 = x_output # XOR(LHS)

    return LE_out32, RE_out32


def des_enc(inputblock, num_rounds, inputkey64):
    # This is the function that accepts one bloc of plaintext
    # and applies all rounds of the DES cipher and returns the
    # cipher text block. 
    # Inputs:
    # inputblock: byte sequence representing input block
    # num_rounds: integer representing number of rounds in the feistel 
    # key: byte sequence (8 bytes)
    # Output:
    # cipherblock: byte sequence    


    # generate keylist using 64bit input key
    key64to56 = Permutation(inputkey64, PC1)

    C_Orig, D_Orig = split(key64to56)

    keylist = []

    roundindex = 0
    while roundindex < num_rounds:
      #print("Round: " + str(roundindex))

      # using key48, C_out, D_out = des_keygen(C_inp, D_inp, roundindex):
      temp_key48, C_Orig, D_Orig = des_keygen(C_Orig, D_Orig, roundindex)

      keylist.append(temp_key48)
      # to put in front: insert(0, temp_key48)
      roundindex += 1
      #print("numkeys = " + str(roundindex))

    #print("enc keylist: ")
    ##print(keylist)

    # perform initial permutation 
    #print("initial perm: " +str(inputblock))
    initpermstr = Permutation(inputblock, BookInitPermOrder)


    LE_inp = [""] * (num_rounds+1)
    RE_inp = [""] * (num_rounds+1)

    #blocksize = len(inputblock)


    LE_inp[0], RE_inp[0] = split(initpermstr)

    for round in range(1, num_rounds+1):
      #print("Round: " + str(round))

      LE_inp[round], RE_inp[round] = des_round(LE_inp[round-1], RE_inp[round-1], keylist[round-1])
      #print("LHS: " + LE_inp[round])
      #print("RHS: " + RE_inp[round])
      
    pre_cipherblock = RE_inp[num_rounds] + LE_inp[num_rounds]
    #print(len(pre_cipherblock))

    cipherblock = Permutation(pre_cipherblock, BookInvInitPermOrder)

    return cipherblock


    
def des_enc_test(input_fname, inputkey64, num_rounds=16, output_fname='output.txt'):
    

    finp = open(input_fname, 'rb')
    inpbyteseq = finp.read()
    finp.close()
    
    blocksize = 8

    print(inpbyteseq)


    # IN CASE THE QUOTATION MARKS BREAK
    #inpbyteseq = inpbyteseq.replace(b"""'""", b'')
    #inpbyteseq = inpbyteseq.replace(b'''"''', b'')
    # .count('a') to count, if it is odd/unbalanced, add to the end, then delete on decipher?
    
    print('\n')
    print(inpbyteseq)
    #inpbyteseq.replace("'",'\'')

    inputkey64 = byteseq2binstr(inputkey64)

    blocklist = [inpbyteseq[i: i + blocksize] for i in range(0, len(inpbyteseq), blocksize)]


    # Pad the last element with spaces b'\x20' until it is 8 bytes long
    if len(blocklist[-1])%8 > 0:
      blocklist[-1] = blocklist[-1] + b'\x20'*(8 - len(blocklist[-1])%8)

    encodedlist = []

    for inputblock in blocklist:
      #print("Encoding: " + str(inputblock))
      
      
      result = des_enc(byteseq2binstr(inputblock), num_rounds, inputkey64)
      encodedlist.append(binstr2byteseq(result))

    cipherbyteseq = b''.join(encodedlist)

    fout = open(output_fname, 'wb')
    fout.write(cipherbyteseq)
    fout.close()
    
### DECIPHER

def des_dec(inputblock, num_rounds, inputkey64):
    # This is the function that accepts one bloc of ciphertext
    # and applies all rounds of the DES cipher and returns the
    # plaintext text block. 
    # Inputs:
    # inputblock: byte sequence representing ciphertext block
    # num_rounds: integer representing number of rounds in the feistel 
    # key: byte sequence (8 bytes)
    # Output:
    # plainblock: byte sequence    
    
    # try:
    # do the same as enc, but use the keys in reverse order


    plainblock = ''

    # generate keylist using 64bit input key
    #print("turning 64b key into 56")
    key64to56 = Permutation(inputkey64, PC1)
    #print("Splitting 56b key")
    C_Orig, D_Orig = split(key64to56)

    keylist = []

    for roundindex in range(0,num_rounds):
      #print("Round: " + str(roundindex))

      temp_key48, C_Orig, D_Orig = des_keygen(C_Orig, D_Orig, roundindex)

      keylist.append(temp_key48)


    # perform initial permutation 
    initpermstr = Permutation(inputblock, BookInitPermOrder)

    LE_inp = [""] * (num_rounds+1)
    RE_inp = [""] * (num_rounds+1)

    blocksize = len(inputblock)

    LE_inp[0] = initpermstr[:int(blocksize/2)]
    RE_inp[0] = initpermstr[int(blocksize/2):int(blocksize)]

    for round in range(1, num_rounds+1):

      LE_inp[round], RE_inp[round] = des_round(LE_inp[round-1], RE_inp[round-1], keylist[num_rounds-round])
      #print("LHS: " + LE_inp[round])
      #print("RHS: " + RE_inp[round])
      
    pre_cipherblock = RE_inp[num_rounds] + LE_inp[num_rounds]

    # do inverse initial perm
    plainblock = Permutation(pre_cipherblock, BookInvInitPermOrder)

    #plainblock = binstr2byteseq(post_cipherblock)

    return plainblock
    
def des_dec_test(input_fname, inputkey64, num_rounds, output_fname):
    
    # inputkey64: byte sequence (8 bytes)
    # numrounds: asked since your feistel already has it but we always use 16 for DES
        
    # First read the contents of the input file as a byte sequence

    
    finp = open(input_fname, 'rb')
    cipherbyteseq = finp.read()
    finp.close()
    
    inputkey64 = byteseq2binstr(inputkey64)

    blocksize = 8

    blocklist = [cipherbyteseq[i: i + blocksize] for i in range(0, len(cipherbyteseq), blocksize)]

    # Pad the last element with spaces b'\x20' until it is 8 bytes long
    #print(len(blocklist[-1]))
    if len(blocklist[-1])%8 > 0:
      blocklist[-1] = blocklist[-1] + b'\x20'*(8 - len(blocklist[-1])%8)


    decodedlist = []

    for inputblock in blocklist:
      #print("Decoding: " + str(inputblock))
      result = des_dec(byteseq2binstr(inputblock), num_rounds, inputkey64)
      #print("Decoding: " + str(binstr2byteseq(result)))
      #print("result: " + str(result))
      decodedlist.append(binstr2byteseq(result))
      #decodedlist.append(binstr2byteseq(result))

    #print('done')
    plainbyteseq = b''.join(decodedlist).strip()

    fout = open(output_fname, 'wb')
    fout.write(plainbyteseq)
    fout.close()
    



### END OF DECIPHER



### test section
def testfunction():
  

  rounds = 16
  #inputkey64 = '1111111111111011111111111111111111111101111111111111111111111000'

  inputkey64 = b'1G3456ac' # this is 64 bit (8 bytes)
  
  #print(len(inputkey64))
  #print("\n\nENCODING NOW")
  des_enc_test("default.txt", inputkey64, rounds, "output.txt")


  #print("\n\nATTEMPTING TO DECODE")

  des_dec_test("output.txt", inputkey64, rounds, "output2.txt")



if __name__ == "__main__":
    testfunction()