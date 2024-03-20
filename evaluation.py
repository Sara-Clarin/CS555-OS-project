import platform

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
    scalar = 10**

    fsize = 50 * scalar
    step  = 50 * scalar

    for i in range(8):
        print(f"Creating file of size {fsize} .......")

        subprocess.run(["python3", "randfile.py", f'{fsize}', '--to_stdout', '0'])
        
        fsize += step

def Run_Enc_Analysis( ):

    # TODO: generate keys beforehand and extract them
    scalar = 10**3  #Kilobyte

    fsize = 50 * scalar
    step  = 50 * scalar

    for i in range(8):
        print(f"Testing {fsize} .......")

        k = os.urandom(16)   # TODO: fix this
        key = tools.key_expansion(k)

        #plaintext_string = check_output(["python3", "randfile.py", f'{i}'])
        if "Win" in platform.system():
            infile = open(f'eval_files\\{fsize}.txt', 'rb')
        if "Darwin" in platform.system():
            infile = open(f'eval_files/{fsize}.txt', 'rb')
        else:
            infile = open(f'eval_files/{fsize}')

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

        print("[INFO]: Non-Parallel Encryption")

        start = time.time_ns()
        for x in range(num_blocks):
            block = padded[x*16: (x*16)+16]
            aesencrypt.aes_encrypt(block, key)   # do not store ciphertext for speed
            #print(f'[INFO]: Blocks remaining: {num_blocks - x}')

        sequential_time.append(time.time_ns() - start)
        file_sizes.append(fsize)

        ###############
        #TODO: PARALLEL AES
        ####################
        start = time.time_ns()
        # call to aes_parallel
        aesencrypt.aes_enc_parallel(padded, key)
        parallel_time.append( time.time_ns() - start)
        #parallel_time.append(0)

        fsize += step

    print(f'sequential time: {sequential_time}')
    print(f'Parallel time: {parallel_time}')
    print(f'File sizes: {file_sizes}')

    
    with open("Kilobyte_results.txt", "w+") as f:
        f.write(f'Comparison of Parallel/Non-Parallel AES execution time\n')
        f.write(f'-------------- Sequential AES ------------')
        for seqtime in zip(file_sizes, sequential_time):
            f.write(f'{seqtime[0]/ (scalar)} KB - {seqtime[1]})')

        f.write(f'-------------- Parallel AES ------------')

        for partime in zip(file_sizes, parallel_time):
            f.write(f'{partime[0]/ (scalar)} KB - {partime[1]})')
    
    return scalar

# create a bar chart
# If this doesn't work, then a CSV 
def Plot_bar(xvals, yvals1, yvals2, scalar):
    
    barWidth = (xvals[1] - xvals[0]) / (10 * scalar)
    offset = barWidth/2 

    x1 = [(x / scalar)-offset for x in xvals]
    x2 = [(x / scalar)+offset for x in xvals]


    print("barWidth", barWidth)

    #file_sizes on x axis, 
    plt.bar(x1, yvals1, color='blue', width=barWidth, label="Sequential AES")
    plt.bar(x2, yvals2, color='red', width=barWidth, label="Parallelized AES")
    plt.legend(loc="upper left")
    plt.ylabel("Execution time (s)")
    plt.xlabel("File size - KB")
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
    scalar = Run_Enc_Analysis()
    Plot_bar(file_sizes, sequential_time, parallel_time, scalar)
    #Plot(file_sizes, parallel_time)


if __name__ == "__main__":
    main()