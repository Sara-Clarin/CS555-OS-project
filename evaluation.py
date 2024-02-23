import aesencrypt
import os
import aesdecrypt
import time

import matplotlib.pyplot as plt
from subprocess import check_output

file_sizes = []
sequential_time = []
parallel_time = []

# TODO: remove once this is put into aesencrypt
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

# TODO: generate a series of random file with bytes increasing
def GenFileSet():
    
    smallest = 32 * (10**1) #16 megabyte file
    largest  = 256 * (10*1) 
    step     = 32 * (10**1)

    for i in range(smallest, largest, step):
        print("Testing {i} .......")

        plaintext_string = check_output(["python3", "randfile.py", f'{i}'])

        #file_sizes.append( i // (10**6))   # file sizes in megabytes
        file_sizes.append(i)
        key = os.urandom(16)

        #TODO: adapt once the padding function is moved into aesencrypt
        start = time.time()
        padded_plaintext = iso_iec_7816_4_pad(plaintext_string)

        # Sequential AES
        aesencrypt.aes_encrypt(padded_plaintext,key)
        sequential_time.append(time.time() - start)

        #TODO: insert parallel AES
        # start = time.time()
        # call to aes_parallel
        #parallel_time.append( time.time() - start)
        parallel_time.append(0)

    print(f'sequential time: {sequential_time}')
    print(f'File sizes: {file_sizes}')
# Call aesencryption on a file
# Time the operation and write to a file
def Encrypt( file_p, fsize):

    #open a file
    #feed in using CORRECT FORMAT
    #Print time values to the screen
    pass

# OPTIONAL: test that ciphertext matches plaintext
# May delete, as correctness testing is largely done elsewhere
def SanityCheck():
    pass

# create a bar chart
# If this doesn't work, then a CSV 
def Plot_bar(xvals, yvals1, yvals2):

    barWidth = 100

    #file_sizes on x axis, 
    plt.bar(xvals, yvals1, color='blue', width=barWidth)
    #plt.bar(xvals, yvals2, color='red')

    plt.ylabel("Execution time ")
    plt.xlabel("File size")
    plt.show()
    
# Option to examine line graph
def Plot_line():
    pass

def main():
    GenFileSet()
    Plot_bar(file_sizes, sequential_time, parallel_time)
    #Plot(file_sizes, parallel_time)


if __name__ == "__main__":
    main()