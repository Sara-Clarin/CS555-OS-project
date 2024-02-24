""" **************************************************************
* Course ID  : CSCI555L - Advanced Operating Systems             *
* Due Date   : TBD                                               *
* Project    : AES128-ECB Implementation                         *
* Purpose    : This project is an implementation of the Advanced *
*              Encryption Standard (AES) using a 128-bit key.    *
*****************************************************************"""
import aesdecrypt

mix_col_matrix = [ [0x02, 0x03, 0x01, 0x01],
                   [0x01, 0x02, 0x03, 0x01],
                   [0x01, 0x01, 0x02, 0x03],
                   [0x03, 0x01, 0x01, 0x02] ]

r_const = [0x01000000,0x02000000,0x04000000,0x08000000,0x10000000,0x20000000,0x40000000,0x80000000,0x1B000000,0x36000000]

s_box = [[0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
        [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
        [0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],
        [0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],
        [0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],
        [0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],
        [0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],
        [0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],
        [0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73],
        [0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb],
        [0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],
        [0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08],
        [0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a],
        [0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e],
        [0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf],
        [0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]]

"""
Function :   debug_print_arr_hex_1line
Parameters : hex_array - 1D hexadecimal array
Output :     None
Description: Iterates through entire 1D array and prints to screen.
             used in aes_enc_main and aestest.py main
"""
def debug_print_arr_hex_1line(hex_array):
    for x in range(len(hex_array)):
        print(format(hex_array[x], '#04x'), end=' ')
    print()

"""
Function :   xor_2d
Parameters : arr1 - 2D hexadecimal array
             arr2 - 2D hexadecimal array
Output :     arr1 - 2D hexadecimal array that has been XOR'ed by arr2
Description: Iterates through every element of both 2D arrays and XOR's arr1[row][col] ^ arr2[row][col].
             arr1 used as storage and returned back to caller. 
             Used in key addition
"""
def xor_2d(arr1, arr2):
    for i in range(len(arr1)):
        for j in range(len(arr1[0])):
            val = arr1[i][j] ^ arr2[i][j]
            arr1[i][j] = val

    return arr1

"""
Function :   rot_word_L
Parameters : word - current 32 bit unsigned word
             amt - requested rotate left amount
Output :     32-bit unsigned word
Description: Rotates a 32-bit word by requested amount using bit shifts, then returning new value back to caller
             Needed for Key Expansion and Shift Rows
"""
def rot_word_L(word, amt):
    if amt == 1:
        return ((word << 8) & 0xFFFFFF00) | ((word >> 24) & 0x000000FF)
    elif amt == 2:
        return ((word << 16) & 0xFFFF0000) | ((word >> 16) & 0x0000FFFF)
    elif amt == 3:
        return ((word << 24) & 0xFF000000) | ((word >> 8) & 0x00FFFFFF)

"""
Function :   s_box_sub
Parameters : state array
Output :     updated state array
Description: Perform S-Box substitution on the entire 16-byte state array
"""
def s_box_sub(state):
    for i, row in enumerate(state):
        for j, col in enumerate(row):
            ms_nibble = (state[i][j] & 0xF0) >> 4
            ls_nibble = (state[i][j] & 0x0F)
            state[i][j] = s_box[ms_nibble][ls_nibble]

    return state

"""
Function :   sub_word
Parameters : (x1) 32-bit word
Output :     (x1) 32-bit word that has been substituted by S-Box
Description: Perform S-Box substitution on (x1) 32-bit word
"""
def sub_word(input_word):
    byte_arr = input_word.to_bytes(4, 'big')
    ret_word = [0,0,0,0]
    for i, byte in enumerate(byte_arr):
        ms_nibble = (byte & 0xF0) >> 4
        ls_nibble = (byte & 0x0F)
        ret_word[i] = s_box[ms_nibble][ls_nibble]

    return int.from_bytes(ret_word, 'big')

"""
Function :   shift_rows
Parameters : state array
Output :     update state array
Description: shift all rows by set amount
"""
def shift_rows(state):
    for i in range(1,4,1):
        word = rot_word_L(state[i][0] << 24 | state[i][1] << 16 | state[i][2] << 8 | state[i][3], i)
        converter = word.to_bytes(4, byteorder='big', signed=False)
        state[i][0] = int(converter[0])
        state[i][1] = int(converter[1])
        state[i][2] = int(converter[2])
        state[i][3] = int(converter[3])

"""
Function :   mix_cols
Parameters : state array
Output :     updated state array
Description: Mix Columns driver
"""
def mix_cols(state):
    temp = [[0x00, 0x00, 0x00, 0x00],
            [0x00, 0x00, 0x00, 0x00],
            [0x00, 0x00, 0x00, 0x00],
            [0x00, 0x00, 0x00, 0x00]]

    for i, row in enumerate(temp):
        for j, col in enumerate(row):
            curr_col = [state[0][j], state[1][j], state[2][j], state[3][j]]
            temp[i][j] = mix_columns_transform(i, curr_col)

    return temp

"""
Function :   mix_columns_transform
Parameters : Current index row, state column
Output :     1 Byte
Description: Performs Mix Columns using polynomials over GF(2^8)
"""
def mix_columns_transform(I_row, S_Col):
    temp = 0x00

    """Iterates over current Mix Col row and state array column to perform matrix multiplication"""
    for i in range(len(mix_col_matrix[I_row])):
        element = mix_col_matrix[I_row][i]

        """
        Determine if you are multiplying either by 0x02, 0x03, or 0x01
        If MS bit is set before multiplying temp by 2, XOR temp using polynomial x^4 + x^3 + x^2 + 1 (0x1B)
        """
        if element == 0x02:
            temp ^= (S_Col[i] << 1)
            if S_Col[i] >= 0x80:
                temp ^= 0x1B

        elif element == 0x03:
            temp ^= S_Col[i] ^ (S_Col[i] << 1)

            if S_Col[i] >= 0x80:
                temp ^= 0x1B

        else:
            temp ^= S_Col[i]

    return temp & 0xFF

"""
Function :   key_expansion
Parameters : AES Secret Key
Output :     2D Array with all keys used for AES key schedule
Description: Perform complex operations to expand (x1) 16-byte key into (x11) 16-byte keys
"""
def key_expansion(aes_key):
    """Since aes_key is a byte array, manually create 32-bit words"""
    w = [aes_key[0] << 24 | aes_key[1] << 16 | aes_key[2] << 8 | aes_key[3],
         aes_key[4] << 24 | aes_key[5] << 16 | aes_key[6] << 8 | aes_key[7],
         aes_key[8] << 24 | aes_key[9] << 16 | aes_key[10] << 8 | aes_key[11],
         aes_key[12] << 24 | aes_key[13] << 16 | aes_key[14] << 8 | aes_key[15]]
    temp = w[3]
    r_const_ptr = 0

    """Iterate through all keys and perform necessary rotations and XOR'ing from previous bytes"""
    for x in range(4, 44, 1):

        """If a words has been made - rotate, substitute, and use round constant for XOR"""
        if x % 4 == 0:
            temp = rot_word_L(temp, 1)
            #print(f'[Debug] After RotWord(): 0x{temp:02x}')
            temp = sub_word(temp)
            #print(f'[Debug] After SubWord(): 0x{temp:02x}')
            #print(f'[Debug] Rcon: 0x{r_const[r_const_ptr]:02x}')
            temp ^= r_const[r_const_ptr]
            r_const_ptr += 1

            #print(f'[Debug] After XOR with Rcon: 0x{temp:02x}')

        temp ^= w[x - 4]
        #print(f'[Debug] After XOR with w[i-Nk]: 0x{temp:02x}')
        w.append(temp)

    key_out = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]

    """
    Iterate through the key_out 2D array to store all 11 keys in this array, iterate 1 word at a time
    Each row represents the round key for AES enc/dec
    """
    for i in range(len(key_out)):
        for j in range(len(key_out[0])):
            key_out[i][j] = w[i * len(key_out[0]) + j]

    return key_out

"""
Function :   extract_key
Parameters : Key List
Output :     Returns key from 1D space into 2D space 
Description: Turn 1D byte array into 2D for easy XOR operations
"""
def extract_key(key):
    byte_arr = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

    for i in range(4):
        converter = key[i].to_bytes(4, byteorder='big', signed=False)
        byte_arr[0][i] = int(converter[0])
        byte_arr[1][i] = int(converter[1])
        byte_arr[2][i] = int(converter[2])
        byte_arr[3][i] = int(converter[3])

    return byte_arr

"""
Function :   populate_state
Parameters : empty state array, plaintext, current encryption round
Output :     Returns state array with populated plaintext
Description: Turn 1D byte array into 2D state array using respective indexing
"""
def populate_state(state, pt, curr_round):
    for col in range(len(state[0])):
        state[0][col] = pt[(col * 4) + (curr_round * 16)]
        state[1][col] = pt[(col * 4 + 1) + (curr_round * 16)]
        state[2][col] = pt[(col * 4 + 2) + (curr_round * 16)]
        state[3][col] = pt[(col * 4 + 3) + (curr_round * 16)]

"""
Function :   state_store
Parameters : encrypted state array, ciphertext byte array
Output :     Returns ciphertext byte array with 16 extra bytes
Description: Used to correctly store bytes in order from AES state array
             Loop through all column elements and store in 1d array using list comprehension
Website:     https://www.w3schools.com/python/python_lists_comprehension.asp
"""
def state_store(state, ct):
    for j in range(len(state[0])):
        column = [row[j] for row in state]
        for elem in column:
            ct.append(elem)

"""
Function :   aes_encrypt
Parameters : 1D Plaintext Byte array, 1D key array (16 bytes)
Output :     1D ciphertext array
Description: AES-128 Encryption Algorithm
"""
def aes_encrypt(pt,key):
    ciphertext = bytearray([])
    num_blocks = int(len(pt) / 16)
    curr_round = 0

    """generate key schedule for all 10 rounds"""
    #key_schedule = key_expansion(key)

    """for-loop to iterate over all 16-byte plaintext blocks"""
    for i in range(num_blocks):
        state = [[0x00, 0x00, 0x00, 0x00], [0x00, 0x00, 0x00, 0x00], [0x00, 0x00, 0x00, 0x00], [0x00, 0x00, 0x00, 0x00]]

        """This function will turn the 1D plaintext into multiple 2D state arrays"""
        populate_state(state, pt, curr_round)

        round_key = extract_key(key_schedule[0])

        state = xor_2d(state, round_key)

        """Perform necessary shifting, mixing, and substitution on 2D state array"""
        for aes_round in range(1, 11, 1):
            #print(f'[ENCRYPT]: round{aes_round}: Start of Round')
            #tools.debug_print_arr_2dhex_1line(state)
            #print()

            #print(f'[ENCRYPT]: round{aes_round}: After SubBytes')
            s_box_sub(state)
            #tools.debug_print_arr_2dhex_1line(state)
            #print()

            #print(f'[ENCRYPT]: round{aes_round}: After ShiftRows')
            shift_rows(state)
            #tools.debug_print_arr_2dhex_1line(state)
            #print()

            """Mix Columns skipped for only round 10"""
            if aes_round != 10:
                #print(f'[ENCRYPT]: round{aes_round}: After MixColumns')
                state = mix_cols(state)
                #tools.debug_print_arr_2dhex_1line(state)
                #print()

            #print(f'[ENCRYPT]: round{aes_round}: Round key Value')
            round_key = extract_key(key_schedule[aes_round])

            state = xor_2d(state, round_key)
            #tools.debug_print_arr_2dhex_1line(round_key)
            #print()

        #print(f'AES Encrypt Complete')
        #tools.debug_print_arr_2dhex(state)

        """Store 16 extra bytes into ciphertext"""
        state_store(state, ciphertext)

        """Update current cipher round for indexing"""
        curr_round += 1


    return ciphertext

"""
Function :   main
Parameters : 1D Plaintext Byte array, 1D key array (16 bytes)
Output :     None
Description: AES Encrypt driver - must be called from aestest.py
Usage:       python aestest.py "<StringtoEncrypt>"

"""
def aes_enc_main(pt, key):

    #generate n-byte ciphertext
    ciphertext = aes_encrypt(pt, key)

    print('[aesencrypt.py] Ciphertext:')
    debug_print_arr_hex_1line(ciphertext)
    print()

    #Calling aesdecrypt.py to handle decryption
    aesdecrypt.aes_dec_main(ciphertext, key)



























