""" **************************************************************
* Course ID  : CSCI555L - Advanced Operating Systems             *
* Due Date   : TBD                                               *
* Project    : AES128-ECB Implementation                         *
* Purpose    : This project is an implementation of the Advanced *
*              Encryption Standard (AES) using a 128-bit key.    *
*****************************************************************"""

import aesencrypt
import os
import sys

"""
Function :   read_file
Parameters : path - File Path
Output :     None
Description: Reads file path to byte array
"""
def read_file(path):
    with open(path, "rb") as f_input:
        return f_input.read()

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
Function :   debug_print_plaintext_ascii
Parameters : input - array of hexadecimal 
Output :     None
Description: Iterates through entire array, converts hexadecimal to ASCII, then prints to screen
             Used in aes_dec_main and aestest.py main
"""
def debug_print_plaintext_ascii(input):
    for x in range(len(input)):
        print(f'{input[x]:c}', end='')
    print()

"""
Function :   iso_iec_7816_4_pad
Parameters : 1D unpadded plaintext array
Output :     1D padded plaintext array
Description: Determines length of input plaintext and pads to ISO/IEC 7816-4 standards
             First byte of pad is 0x80 followed by subsequent 0x00 bytes until a block (16 bytes) has been fulfilled 
Wiki:        https://en.wikipedia.org/wiki/Padding_(cryptography)
"""
def iso_iec_7816_4_pad(pt):
    ret_pt = bytearray(pt)
    length = len(ret_pt)
    padding = 16 - (length % 16)

    if padding != 0:
        #Short first plaintext block
        if length <= 15:
            ret_pt.append(0x80)
            for i in range(16 - length -1):
                ret_pt.append(0x00)

        #subsequent short blocks
        else:
            ret_pt.append(0x80)
            for i in range(padding - 1):
                ret_pt.append(0x00)
    return ret_pt

"""
Function :   check_empty
Parameters : plaintext 1D byte array
Output :     True or False
Description: Iterates through entire array, determines if the input string is only spaces (0x20) or 32 ASCII
"""
def check_empty(pt):
    retval = True
    for i in range(len(pt)):
        if pt[i] != 0x20:
            retval = False
            break
    return retval


"""
Function :   main
Parameters : ASCII Plaintext (argv[1])
Output :     None
Description: Single-entry point for AES-128 ECB mode
Edge Cases:  1. Not Enough Command line arguments len(args[1]) < 2
             2. Too many Command line arguments len(args[1]) > 2
             3. Empty string len(args[1]) == 0
             4. String to encrypt is only a string of spaces (all characters are 0x20) i.e: python aestest.py "       " 
Usage:       python aestest.py "<StringtoEncrypt>"

"""
if __name__ == '__main__':
    print("-----------------------------------")
    print("CSCI-531 AES-128 ECB Implementation")
    print("-----------------------------------")

    args = sys.argv
    plaintext = ""

    if len(args) < 2:
        print(f'[ERROR]: Not enough command line arguments\r\n'
              f'[Usage]: python3 aestest.py "<StringtoEncrypt>"\r\n'
              f'Exiting Now..')
        sys.exit(-1)
    elif len(args) > 2:
        print(f'[ERROR]: Too many command line arguments\r\n'
              f'[Usage]: python3 aestest.py "<StringtoEncrypt>"\r\n'
              f'[Tip 1]: Ensure plaintext is encased with double quotations "<StringtoEncrypt>"\r\n'
              f'[Tip 2]: If plaintext contains quotations ("") use escape characters (\) to include\r\n'
              f'[Example]: python3 aestest.py "\\"<StringtoEncrypt>\\""\r\n'
              f'Exiting Now..')
        sys.exit(-1)
    else:
        plaintext = bytes(args[1], 'utf-8')

    if len(plaintext) == 0:
        print(f'[ERROR]: Plaintext is a NULL string - 0 bytes captured from CLI\r\n'
              f'[Usage]: python3 aestest.py "<StringtoEncrypt>"\r\n'
              f'Exiting Now..')
        sys.exit(-1)

    if check_empty(plaintext):
        print(f'[ERROR]: Plaintext only contains spaces - No data to encrypt\r\n'
              f'[Usage]: python3 aestest.py "<StringtoEncrypt>"\r\n'
              f'Exiting Now..')
        sys.exit(-1)

    #Pad to ISO/IEC 7816-4 Standards
    padded_plaintext = iso_iec_7816_4_pad(plaintext)

    #Generate new random 16-byte key upon runtime
    key = os.urandom(16)

    #User cannot see padding bytes being printed out in terminal
    #print(f'[aestest.py] AES-128 Padded Plaintext (ASCII):')
    #debug_print_plaintext_ascii(padded_plaintext)
    #print()

    print(f'[aestest.py] AES-128 Random Key (HEX):')
    debug_print_arr_hex_1line(key)
    print()

    #Calling aesencrypt.py to encrypt plaintext with random key
    aesencrypt.aes_enc_main(padded_plaintext,key)