# Constants
PT_BLOCK_SIZE = 16
AES_PT_PADDING = 0x00

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

"""
Function :   debug_print_arr_2dhex_1line
Parameters : hex_array - 2D hexadecimal array
Output :     None
Description: Iterates through entire array, flattens a 2D array into 1D then prints to screen.
             Printing columns out from AES using list comprehension
             https://www.w3schools.com/python/python_lists_comprehension.asp
"""
def debug_print_arr_2dhex_1line(hex_array):
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




