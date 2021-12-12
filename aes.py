import numpy as np


# method to convert text to unicode matrix
def text2Unicode(text):
  text_matrix = np.zeros((16),dtype=int)  # 16 element vector with zeros

  for i in range(16):
    text_matrix[i] = ord(text[i])     # ord converts char to unicode integer value

  text_matrix = np.reshape(text_matrix,(4,4)) # reshape the vector to a 4x4 matrix
  return text_matrix


# funtion to convert unicode matrix to text
def unicode2Text(matrix):
  text = ""
  matrix = matrix.flatten()
  for i in range(16):
    text+=chr(int(matrix[i])) # chr converts unicode integer to unicode character
  return text


# method to substitute bytes using rjindael s-box
def subBytes(A):
  s_box = np.load('Lookup Tables/s_box.npy')
  B = np.zeros((4,4),dtype=int)
  for row in range(4):
    for col in range(4):
      sub_row, sub_col = A[row,col]//16, A[row,col]%16
      B[row,col] = s_box[sub_row,sub_col]
  return B


# method to restore bytes of using inverse rjindael s-box
def invSubBytes(A):
  inv_s_box = np.load('Lookup Tables/inv_s_box.npy')
  B = np.zeros((4,4),dtype=int)
  for row in range(4):
    for col in range(4):
      sub_row, sub_col = A[row,col]//16, A[row,col]%16
      B[row,col] = inv_s_box[sub_row,sub_col]
  return B


# method to shift rows
def shiftRows(A):
  B = np.zeros((4,4),dtype=int)
  # keep 1st row intact
  B[0,:] = A[0,:]
  # shift each element of 2nd row 1 step to the left 
  B[1,0],B[1,1],B[1,2],B[1,3] = A[1,1],A[1,2],A[1,3],A[1,0] 
  # shift each element of 3rd row 2 steps to the left
  B[2,0],B[2,1],B[2,2],B[2,3] = A[2,2],A[2,3],A[2,0],A[2,1]
  # shift each element of 4th row 3 steps to the left
  B[3,0],B[3,1],B[3,2],B[3,3] = A[3,3],A[3,0],A[3,1],A[3,2]
  return B


# method to restore shifted rows
def invShiftRows(A):
  B = np.zeros((4,4),dtype=int)
  # keep 1st row intact
  B[0,:] = A[0,:]
  # shift each element of 2nd row 1 step to the left 
  B[1,1],B[1,2],B[1,3],B[1,0] = A[1,0],A[1,1],A[1,2],A[1,3] 
  # shift each element of 3rd row 2 steps to the left
  B[2,2],B[2,3],B[2,0],B[2,1] = A[2,0],A[2,1],A[2,2],A[2,3]
  # shift each element of 4th row 3 steps to the left
  B[3,3],B[3,0],B[3,1],B[3,2] = A[3,0],A[3,1],A[3,2],A[3,3]
  return B


#method to mix columns using Galois Field E Table
def mixCol(A):
  e_table = np.load('Lookup Tables/E_Table.npy')
  B = np.zeros((4,4),dtype=int)
  for row in range(4):
    for col in range(4):
      sub_row , sub_col = A[row,col]//16,A[row,col]%16
      B[row,col] = e_table[sub_row,sub_col]
  return B


#method to restore mixed columns using Galois Field L Table
def invMixCol(A):
  l_table = np.load('Lookup Tables/L_Table.npy')
  B = np.zeros((4,4),dtype=int)
  for row in range(4):
    for col in range(4):
      sub_row , sub_col = A[row,col]//16,A[row,col]%16
      B[row,col] = l_table[sub_row,sub_col]
  return B


#method to add round key to text
def addRoundKey(A,key):
  B = np.zeros((4,4),dtype=int)
  B = np.bitwise_xor(A,key)
  return B


#method to restore text after adding round key
def removeRoundKey(A,key):
  B = np.zeros((4,4),dtype=int)
  B = np.bitwise_xor(A,key)
  return B


# Rotae word by 1 byte
def rotateWord(word):
  # rotate word to the left by one
  word[0],word[1],word[2],word[3] = word[1],word[2],word[3],word[0]
  return word


# SubWord used in key expansion
def subWord(word):
  s_box = np.load('Lookup Tables/s_box.npy')
  ans = np.zeros(4,dtype=int)
  for i in range(4):
    sub_row, sub_col = word[i]//16, word[i]%16
    ans[i] = s_box[sub_row,sub_col]
  return ans


# Transform word used in expansion key
def trans(word, rcon):
  word = rotateWord(word)
  word = subWord(word)
  word = np.bitwise_xor(word, rcon)
  return word


# Expand master key to 11 round keys
def expandKey(master_key):
  rcon = np.load('Lookup Tables/rcon.npy')
  round_keys = master_key
  # Create all words in round key
  for i in range(4, 44):
    if i % 4 == 0:
      round_keys = np.append(round_keys, [np.bitwise_xor(trans(round_keys[i-1], rcon[i//4]), round_keys[i-4])], axis=0)
    else:
      round_keys = np.append(round_keys, [np.bitwise_xor(round_keys[i-1], round_keys[i-4])], axis=0)

  return round_keys


# Main AES Encrtption Method
def aesEncrypt(plain_text,key):
    key = text2Unicode(key)
    round_keys = expandKey(key)
    length = len(plain_text)
    cipher_text = "" 
    
    # splitting  plain_text into substrings of length 16 each and adding whitspaces to shorter substrings    
    plain_text_split = []
    for i in range(length//16):
        plain_text_split.append(plain_text[0+16*i:16+16*i])
    if not length%16==0:        
        plain_text_split.append(plain_text[16*(length//16):])
    if len(plain_text_split[-1])<16:
        while(len(plain_text_split[-1])<16):
            plain_text_split[-1]+=' '
    
    # encrypting each sub string
    for sub_string in plain_text_split:
      A0 = text2Unicode(sub_string)
      A0 = addRoundKey(A0, round_keys[0:4,:])
      # 9 round
      for i in range(1, 10): 
        A1 = subBytes(A0)
        A2 = shiftRows(A1)
        A3 = mixCol(A2)
        A0 = addRoundKey(A3, round_keys[i*4:(i+1)*4,:])
      A1 = subBytes(A0)
      A2 = shiftRows(A1)
      A0 = addRoundKey(A2, round_keys[40:44,:])
      cipher_text+=unicode2Text(A0)

    return cipher_text


# Main AES Decryption Method
def aesDecrypt(cipher_text,key):
    key = text2Unicode(key)
    round_keys = expandKey(key)
    decrypted_text = ""
    length = len(cipher_text)
    # splitting  cipher text into substrings of length 16 each    
    cipher_text_split = []
    for i in range(length//16):
        cipher_text_split.append(cipher_text[0+16*i:16+16*i])
    
    # decrypting each substring
    for sub_string in cipher_text_split:
        cipher_text = text2Unicode(sub_string)
        A0 = removeRoundKey(cipher_text, round_keys[40:44,:])
        for i in range(10, 1, -1):
          A3 = invShiftRows(A0)
          A2 = invSubBytes(A3)
          A1 = removeRoundKey(A2, round_keys[(i-1)*4:i*4,:])
          A0 = invMixCol(A1)
        A3 = invShiftRows(A0)
        A2 = invSubBytes(A3)
        A0 = removeRoundKey(A2,  round_keys[0:4,:])
        decrypted_text+=unicode2Text(A0)
    return decrypted_text

if __name__== '__main__':
    # driver code :
    plain_text = input("Enter a string to be encoded : ")
    print("-----------------------------------------------------")
    cipher_key = input("Enter a 16 character long key for encryption : ")
    print("-----------------------------------------------------")
    print("Encrypting : ")
    cipher_text = aesEncrypt(plain_text,cipher_key)
    print("The encrpyted text is : {}".format(cipher_text))
    print("-----------------------------------------------------")
    print("Decrypting : ")
    decrypted_text = aesDecrypt(cipher_text,cipher_key)
    print("The decrpyted text is : {}".format(decrypted_text))
