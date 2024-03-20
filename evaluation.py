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
    scalar = 10** 6

    fsize = 1 * scalar
    step  = 1 * scalar

    for i in range(3):
        print(f"Creating file of size {fsize} .......")

        subprocess.run(["python3", "randfile.py", f'{fsize}', '--to_stdout', '0'])
        
        fsize += step

def Run_Enc_Analysis( mode):

    if mode == "Enc":
        print("Running Analysis for ENCRYPTION")
        aes_seq_func = aesencrypt.aes_encrypt
        aes_par_func = aesencrypt.aes_enc_parallel
    else:
        print("Running Analysis for DECRYPTION")
        aes_seq_func = aesdecrypt.aes_decrypt
        aes_par_func = aesdecrypt.aes_dec_parallel
    # TODO: generate keys beforehand and extract them
    scalar = 10**6 #Megabyte

    fsize = 1 * scalar
    step  = 1 * scalar

    for i in range(3):
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

        print(f"[INFO]: Non-Parallel {mode}ryption")

        start = time.time_ns()
        for x in range(num_blocks):
            block = padded[x*16: (x*16)+16]
            #aesencrypt.aes_encrypt(block, key)   # do not store ciphertext for speed
            aes_seq_func(block, key)
            #print(f'[INFO]: Blocks remaining: {num_blocks - x}')

        sequential_time.append(time.time_ns() - start)
        file_sizes.append(fsize)

        ###############
        # PARALLEL AES
        ####################
        start = time.time_ns()
        #aesencrypt.aes_enc_parallel(padded, key)
        aes_par_func( padded, key)
        parallel_time.append( time.time_ns() - start)

        fsize += step

    print(f'sequential time: {sequential_time}')
    print(f'Parallel time: {parallel_time}')
    print(f'File sizes: {file_sizes}')

    
    with open(f"Megabyte_results_{mode}.txt", "w+") as f:
        f.write(f'Comparison of Parallel/Non-Parallel AES execution time\n')
        f.write(f'-------------- Sequential AES ------------\n')
        for seqtime in zip(file_sizes, sequential_time):
            f.write(f'{seqtime[0]/ (scalar)} MB {seqtime[1]}\n')

        f.write(f'\n-------------- Parallel AES ------------\n')

        for partime in zip(file_sizes, parallel_time):
            f.write(f'{partime[0]/ (scalar)} MB - {partime[1]}\n')
    
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
    #plt.title(label="Encryption Comparison - MB File sizes")
    plt.ylabel("Execution time (s)")
    plt.xlabel("File size - MB")
    plt.show()
    
# Option to examine line graph
def Plot_line():
    pass

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--gen", help="Generate new file set", type=int)

    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('-d', '--decrypt', action='store_true', help='[Required] Decrypt flag')
    mode.add_argument('-e', '--encrypt', action='store_true', help='[Required] Encrypt flag')
    args = parser.parse_args()

    if args.gen:
        GenFileSet()
        exit(0)

    if args.encrypt:
        scalar = Run_Enc_Analysis("Enc")
    elif args.decrypt:
        scalar = Run_Enc_Analysis("Dec")
    else:
        print("Please specify either encryption or decryption mode")

    '''

    sequential_time = [14693795000, 30218976000, 44778775000]
    parallel_time = [5418044000, 10291946000, 15120102000]
    file_sizes = [1000000, 2000000, 3000000]
    scalar = 10**6
    '''
    Plot_bar(file_sizes, sequential_time, parallel_time, scalar)
    #Plot(file_sizes, parallel_time)


if __name__ == "__main__":
    main()