# Constants
import os
import platform
import re
import subprocess

import aesencrypt

PT_BLOCK_SIZE = 16
AES_128_KEY_SIZE = 16
AES_PT_PADDING = 0x00

# Error Codes
AES_INV_KEY_SIZE = -100

"""
Not Used

def debug_print_arr_hex(hex_array):
    for x in range(len(hex_array)):
        if x % 4 == 0 and x != 0:
            print("\r\n")
        print(f'0x{hex_array[x]:02x}', end=' ')
    print()
"""

"""
Used only in AES Encrypt Test 
"""


def debug_print_arr_2dhex(hex_array):
    for row in hex_array:
        for col in row:
            print(f'{col:#04x}', end=' ')
        print()


def debug_print_arr_2dhex_1line(hex_array):
    """
    Function :   debug_print_arr_2dhex_1line
    Parameters : hex_array - 2D hexadecimal array
    Output :     None
    Description: Iterates through entire array, flattens a 2D array into 1D then prints to screen.
                 Printing columns out from AES using list comprehension
                 https://www.w3schools.com/python/python_lists_comprehension.asp
    """
    for j in range(len(hex_array[0])):
        column = [row[j] for row in hex_array]
        for elem in column:
            print(format(elem, '02x'), end='')
    print()


"""
Not used

def debug_print_arr_ascii(hex_array):
    for x in range(len(hex_array)):
        if x % 8 == 0 and x != 0:
            print("\r\n")
        print(f'{hex_array[x]:c}', end=' ')
    print()
"""

"""
Not used

def xor(arr1, arr2):
    return [a ^ b for a, b in zip(arr1, arr2)]
"""

"""
Not used

def add(arr1, arr2):
    return [a + b for a, b in zip(arr1, arr2)]
"""

"""
not used

def read_AES_key(path):
    with open(path, "rt") as AES_Key:
        hex_arr = bytearray.fromhex(AES_Key.read())
        return hex_arr
        if len(key) != AES_KEY_SIZE:
            print(f'[ERROR]: Input AES key is {len(key)} bytes. Should be {AES_KEY_SIZE} bytes. Exiting now...')
            exit(INVALID_KEY_SIZE)
        else:
            return key
"""

"""
not used
def read_plaintext(path):
    with open(path, "rb") as pt:
        pt = pt.read()
        if len(pt) % PT_BLOCK_SIZE != 0:
            print(f'[NOTICE]: Plaintext size is {len(pt)}, padding to nearest multiple of {PT_BLOCK_SIZE}')
            for i in range(1, len(pt) % PT_BLOCK_SIZE):
                pt += AES_PT_PADDING
        return pt
"""

"""
Not used

def bin_test(hexnum):
    hexnum += 0x1
    print(f'Hex + 1 0x{hexnum:02x}')
"""

"""
Used in Tests only
"""


def compare_2d(arr1, arr2, test_num):
    status = 0
    for i in range(len(arr1)):
        for j in range(len(arr1[0])):
            if arr1[i][j] != arr2[i][j]:
                status = -1

    if status == 0:
        print(f'[Test {test_num}]: PASS')
    else:
        print(f'[Test {test_num}]: FAIL')


"""
Not used
def compare_word(arr1, arr2):
    status = 0
    index = 0
    for i in range(len(arr1)):
        if arr1[i] != arr2[i]:
            status = -1
            index = i

    if status == 0:
        print(f'[Test]: PASS')
    else:
        print(f'[Test]: FAIL iteration {index} mismatch Arr1 = 0x{arr1[index]:02x} Arr2 = 0x{arr2[index]:02x}')
"""


def read_bytes(infile: str, num_bytes: int):
    with open(infile, 'rb') as f:
        data = f.read(num_bytes)
        return data


def read_file(path):
    """
    Function :   read_file
    Parameters : path - File Path
    Output :     None
    Description: Reads file path to byte array
    """
    with open(path, "rb") as f_input:
        return f_input.read()


def debug_print_arr_hex_1line(hex_array):
    """
    Function :   debug_print_arr_hex_1line
    Parameters : hex_array - 1D hexadecimal array
    Output :     None
    Description: Iterates through entire 1D array and prints to screen.
                 used in aes_enc_main and aestest.py main
    """
    for x in range(len(hex_array)):
        print(format(hex_array[x], '#04x'), end=' ')
    print()


def debug_print_plaintext_ascii(input):
    """
    Function :   debug_print_plaintext_ascii
    Parameters : input - array of hexadecimal
    Output :     None
    Description: Iterates through entire array, converts hexadecimal to ASCII, then prints to screen
                 Used in aes_dec_main and aestest.py main
    """
    for x in range(len(input)):
        print(f'{input[x]:c}', end='')
    print()


def iso_iec_7816_4_pad(pt):
    """
    Function :   iso_iec_7816_4_pad
    Parameters : 1D un-padded plaintext array
    Output :     1D padded plaintext array
    Description: Determines length of input plaintext and pads to ISO/IEC 7816-4 standards
                 First byte of pad is 0x80 followed by subsequent 0x00 bytes until a block (16 bytes) has been fulfilled
    Wiki:        https://en.wikipedia.org/wiki/Padding_(cryptography)
    """
    ret_pt = bytearray(pt)
    length = len(ret_pt)
    padding = 16 - (length % 16)

    if length % 16 == 0:
        return ret_pt

    if padding != 0:
        # Short first plaintext block
        if length <= 15:
            ret_pt.append(0x80)
            for i in range(16 - length -1):
                ret_pt.append(0x00)

        # Subsequent short blocks
        else:
            ret_pt.append(0x80)
            for i in range(padding - 1):
                ret_pt.append(0x00)
    return ret_pt


def check_empty(pt):
    """
    Function :   check_empty
    Parameters : plaintext 1D byte array
    Output :     True or False
    Description: Iterates through entire array, determines if the input string is only spaces (0x20) or 32 ASCII
    """
    retval = True
    for i in range(len(pt)):
        if pt[i] != 0x20:
            retval = False
            break
    return retval


def validate_key(key):
    """
     Function :   validate_key
     Parameters : byte array:key
     Output :     None
     Description: Determine if key file contains 16 bytes of key data
     """
    if len(key) != AES_128_KEY_SIZE:
        print(f'Invalid Key Size: {len(key)}')
        debug_print_arr_hex_1line(key)
        exit(AES_INV_KEY_SIZE)


def key_expansion(aes_key):
    # TODO - Remove References from aesencrypt.py
    """
    Function :   key_expansion
    Parameters : AES Secret Key
    Output :     2D Array with all keys used for AES key schedule
    Description: Perform complex operations to expand (x1) 16-byte key into (x11) 16-byte keys
    """
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
            temp = aesencrypt.rot_word_L(temp, 1)
            #print(f'[Debug] After RotWord(): 0x{temp:02x}')
            temp = aesencrypt.sub_word(temp)
            #print(f'[Debug] After SubWord(): 0x{temp:02x}')
            #print(f'[Debug] Rcon: 0x{r_const[r_const_ptr]:02x}')
            temp ^= aesencrypt.r_const[r_const_ptr]
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


def iso_iec_7816_4_unpad(pt):
    """
    Function :   iso_iec_7816_4_unpad
    Parameters : 1D padded plaintext array
    Output :     1D unpadded plaintext array
    Description: Undo padding scheme from aestest.iso_iec_7816_4_pad()
                 Iterate from the back of the byte array, mark 0x80 instance, then return spliced array
    """
    ret_pt = bytearray(pt)
    found = -1
    for i in range(len(ret_pt) -1, 0, -1):
        if ret_pt[i] == 0x80:
            found = i
            break

    if found < 0:
        return ret_pt
    else:
        return pt[:found]


def get_processor_name():
    """
    Function :   get_processor_name
    Parameters : None
    Description: Get processor information - From stackoverflow
                 https://stackoverflow.com/questions/4842448/getting-processor-information-in-python
    :return: String with processor information
    """
    if platform.system() == "Windows":
        return platform.processor()
    elif platform.system() == "Darwin":
        os.environ['PATH'] = os.environ['PATH'] + os.pathsep + '/usr/sbin'
        command = "sysctl -n machdep.cpu.brand_string"
        return subprocess.check_output(command).strip()
    elif platform.system() == "Linux":
        command = "cat /proc/cpuinfo"
        all_info = subprocess.check_output(command, shell=True).decode().strip()
        for line in all_info.split("\n"):
            if "model name" in line:
                return re.sub(".*model name.*:", "", line,1)
    return ""
