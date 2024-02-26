import aesencrypt
import os
import aesdecrypt
import time
import argparse
import tools

import matplotlib.pyplot as plt
from subprocess import check_output
import subprocess

file_sizes = []
sequential_time = []
parallel_time = []

# TODO: remove once this is put into aesencrypt
def iso_iec_7816_4_pad(pt):
    ret_pt = bytearray(pt)
    length = len(ret_pt)
    padding = 16 - (length % 16)

    if len(padding) %16 == 0: 
        return ret_pt

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

# TODO: Decouple file generation with timing + analysis

#generate a series of random file with bytes increasing
def GenFileSet():

    print("Generating test files....")
    # Could move these to globals if need be
    fsize = 32 * (10**1) #16 megabyte file
    step   = 32* (10**1)

    for i in range(8):
        print(f"Creating file of size {fsize} .......")

        subprocess.run(["python3", "randfile.py", f'{fsize}', '--to_stdout', '0'])
        fsize += step

def Run_Enc_Analysis( ):

    # TODO: generate keys beforehand and extract them

    fsize = 32 * (10**1) #16 megabyte file
    step  = 32* (10**1)

    for i in range(8):
        print(f"Testing {fsize} .......")

        k = os.urandom(16)   # TODO: fix this
        key = tools.key_expansion(k)

        #plaintext_string = check_output(["python3", "randfile.py", f'{i}'])
        infile = open(f'eval_files/{fsize}.txt', 'rb')

        data = infile.read()

        # ##############
        # SEQUENTIAL AES
        ###################
        if len(data) % 16 != 0:
            padded = tools.iso_iec_7816_4_pad(data)
            num_blocks = int(len(padded)/16)
        else:
            num_blocks = int(len(data)/16)
            padded = data

        start = time.time_ns()
        for x in range(num_blocks):
            block = padded[x*16: (x*16)+16]
            aesencrypt.aes_encrypt(block, key)   # do not store ciphertext for speed
            print(f'[INFO]: Blocks remaining: {num_blocks - x}')
            
        file_sizes.append(fsize)


        sequential_time.append(time.time_ns() - start)

        ###############
        #TODO: PARALLEL AES
        ####################
        # start = time.time_ns()
        # call to aes_parallel
        #parallel_time.append( time.time_ns() - start)
        parallel_time.append(0)

        fsize += step

    print(f'sequential time: {sequential_time}')
    print(f'File sizes: {file_sizes}')

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

    parser = argparse.ArgumentParser()
    parser.add_argument("--gen", help="Generate new file set", type=int)
    args = parser.parse_args()

    if args.gen:
        GenFileSet()
        exit(0)
    Run_Enc_Analysis()
    Plot_bar(file_sizes, sequential_time, parallel_time)
    #Plot(file_sizes, parallel_time)


if __name__ == "__main__":
    main()