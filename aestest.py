""" **************************************************************
* Course ID  : CSCI555L - Advanced Operating Systems             *
* Due Date   : TBD                                               *
* Project    : AES128-ECB Implementation                         *
* Purpose    : This project is an implementation of the Advanced *
*              Encryption Standard (AES) using a 128-bit key.    *
*****************************************************************"""
import aesencrypt
import aesdecrypt
import argparse
import os
import platform
import tools
import sys


if __name__ == '__main__':
	print("------------------------------------")
	print("CSCI-555L AES-128 ECB Implementation")
	print("------------------------------------")
	print(f'[Processor Info]: {tools.get_processor_name()}\r')
	print(f'[OS]: {platform.system()}\r')
	print(f'[Cores]: {os.cpu_count()}\r')

	parser = argparse.ArgumentParser(prog='aestest.py', description='Perform AES-128 ECB Encryption / Decryption')
	parser.add_argument('-p', action='store_true', help='[Optional] Enable parallelization flag')
	parser.add_argument('-k', action='store', help='[Optional] Key file, omit to generate key')
	parser.add_argument('infile', nargs='?', default=sys.stdin, help='[Required] input file')
	parser.add_argument('outfile', nargs='?', default=sys.stdout, help='[Required] output file')

	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument('-d', '--decrypt', action='store_true', help='[Required] Decrypt flag')
	mode.add_argument('-e', '--encrypt', action='store_true', help='[Required] Encrypt flag')

	args = parser.parse_args()

	# Sample output
	print(args)

	if args.k:
		# Key validation
		with open(args.k, 'rb') as kf:
			key = kf.read()
			tools.validate_key(key)
	else:
		# Generate new random 16-byte key upon runtime
		key = os.urandom(16)
		print(f'[INFO] Generated and saved key to AES.key:\r')
		tools.debug_print_arr_hex_1line(key)
		with open('AES.key', 'wb') as kf:
			kf.write(key)

	# Utilize AES-128 key expansion to generate round keys
	key = tools.key_expansion(key)
	tools.debug_print_arr_2dhex(key)

	if args.p:
		if args.encrypt:
			# TODO AES-128 ECB Parallelized Encrypt
			aesencrypt.AES_Encrypt_Parallelized(args, key)
		else:
			# TODO AES-128 ECB Parallelized Decrypt
			aesdecrypt.AES_Decrypt_Parallelized(args, key)
	else:
		if args.encrypt:
			aesencrypt.AES_Encrypt(args, key)
		else:
			aesdecrypt.AES_Decrypt(args, key)
