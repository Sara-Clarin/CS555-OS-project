""" **************************************************************
* Course ID  : CSCI555L - Advanced Operating Systems             *
* Due Date   : TBD                                               *
* Project    : AES128-ECB Implementation                         *
* Purpose    : This project is an implementation of the Advanced *
*              Encryption Standard (AES) using a 128-bit key.    *
*****************************************************************"""
import os
import sys

import aesencrypt
import aesdecrypt
import tools

import argparse

import tools

if __name__ == '__main__':
	print("------------------------------------")
	print("CSCI-555L AES-128 ECB Implementation")
	print("------------------------------------")

	parser = argparse.ArgumentParser(prog='aestest.py', description='Perform AES-128 ECB Encryption / Decryption')
	parser.add_argument('-p', action='store_true', help='[Optional] Enable parallelization flag')
	parser.add_argument('-k', action='store', help='[Optional] Key file, omit to generate key')
	# parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin, help='[Required] input file')
	# parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout, help='[Required] output file')
	parser.add_argument('infile', nargs='?', default=sys.stdin, help='[Required] input file')
	parser.add_argument('outfile', nargs='?', default=sys.stdout, help='[Required] output file')

	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument('-d', '--decrypt', action='store_true', help='[Required] Decrypt flag')
	mode.add_argument('-e', '--encrypt', action='store_true', help='[Required] Encrypt flag')

	args = parser.parse_args()

	# Sample output
	print(args)

	if args.k:
		# TODO Read and validate key
		key = args.k
	else:
		# Generate new random 16-byte key upon runtime
		key = os.urandom(16)
		print(f'[INFO] Generated and saved key to AES.key:\r')
		tools.debug_print_arr_hex_1line(key)
		with open('AES.key', 'wb') as kf:
			kf.write(key)

	# TODO Call AES Key Gen

	if args.p:
		if args.encrypt:
			print("[INFO]: Parallelized Encryption")
			# TODO AES-128 ECB Non-Parallelized Encrypt
		else:
			print("[INFO]: Parallelized Decryption")
			# TODO AES-128 ECB Non-Parallelized Decrypt
	else:
		if args.encrypt:
			print("[INFO]: Non-Parallelized Encryption")
			# TODO AES-128 ECB Parallelized Encrypt
		else:
			print("[INFO]: Non-Parallelized Decryption")
			# TODO AES-128 ECB Parallelized Decrypt

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
			  f'[Tip 2]: If plaintext contains quotations ("") use escape characters (\\) to include\r\n'
			  f'[Example]: python3 aestest.py <StringtoEncrypt>\r\n'
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
	
"""
