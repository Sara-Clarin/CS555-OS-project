import aesencrypt
import aesdecrypt

import os
import multiprocessing
import time
import argparse
import tools

from concurrent.futures import ProcessPoolExecutor

BLOCK_NUM = 0

# Let's try calling this from evaluation.py
def AES_Parallel(key, filehandle):
    start = time.time()

    n_cpu = multiprocessing.cpu_count() - 1
    procpool = multiprocessing.Pool(processes=n_cpu)

    # map of workers to processes
    procpool.starmap(func=aesencrypt.aes_encrypt, iterable=[pt, key])

    # what does the async version of starmap do?

    procpool.close()
    end = time.time()
    print(f'Execution time: {end - start}')

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--infile", required=False, default="eval_files/250.txt", type=str)
    args = parser.parse_args()

    return args.infile

# should be faster than using python Path module
def read_data(path):
    ''' Return a list of blocks of length 16
    '''
    dsize = os.path.getsize(path)

    with open(path, "rb") as f:
        dobject = f.readlines()
        dobject = dobject[0]

    print(len(dobject))
    print(len(dobject) // 16, "nblocks")
    ll = []
    for i in range((len(dobject)//16)):
        ll.append(dobject[16*i : 16*i+ 16])
    print(ll)
    return dsize, ll

def Parallel_wrapper(block):

    print(f'block is: {block}')
    tools.iso_iec_7816_4_pad(block)

    # TODO: Remove this eventually
    #  Key gen + call encrypt with correct args
    key = os.urandom(16)
    key = tools.key_expansion(key)

    # Possible TODO: rewrite a func in aesencrypt to only do one block (avoids entering the loop at all)
    ct = aesencrypt.aes_encrypt(pt=block, key=key)
    print(f'{ct}')

    global BLOCK_NUM 
    BLOCK_NUM += 1
    print(f'Chunk num: {BLOCK_NUM}')

if __name__ == "__main__":
    #AES_Parallel()
    infile = parse_args()

    n_cpu = multiprocessing.cpu_count() - 1

    nbytes, pt_blocks = read_data(infile)
    chunksize = nbytes // 16   # this is the number of blocks of size 16 for each proc to take
    print(f'chunksize is {chunksize}')

    # TODO: pull out the key generation to generate correct num keys
    # Create secondary wrapper function? To properly feed the correct num arguments including the key

    start = time.time()

    #TODO: label the process number and print out which process did which
    with ProcessPoolExecutor(n_cpu) as executor:  # calls shutdown automatically
        plaintext = executor.map(Parallel_wrapper,pt_blocks, chunksize=chunksize )

    print(f'Runtime: {time.time() - start}')
 

