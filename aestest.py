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
import randfile
import statistics
import numpy as np
import logging
from datetime import datetime

# Coefficient of Variance
cv = lambda x: np.std(x, ddof=1) / np.mean(x) * 100

logger: logging = None

TIME_TRIALS = []
TOTAL_BYTES = 0

def arg_printer(args):
	logger.info(args)
	print(args)


def arg_checker(args):
	if args.outf is None:
		logger.error('[ERROR] Please provide an output file path to continue')
		print('[ERROR] Please provide an output file path to continue')
		exit(-101)

	if args.g is not None:
		logger.info(f'Generating File of size {args.g}\n')
		print(f'Generating File of size {args.g}\n')
		f_name = randfile.main_wrapper(int(args.g))
		args.inf = f_name
	else:
		if args.inf:
			if not os.access(args.inf, os.R_OK):
				logger.error('[ERROR] Cannot open file for reading')
				print('[ERROR] Cannot open file for reading')
				exit(-100)
		else:
			logger.error('[ERROR] Cannot open file for reading')
			print('[ERROR] Please provide an input file path to continue')
			exit(-101)


def key_check(args):
	if args.k:
		# Key validation
		with open(args.k, 'rb') as kf:
			key = kf.read()
			tools.validate_key(key)
	else:
		# Generate new random 16-byte key upon runtime
		key = os.urandom(16)
		logger.info(f'[INFO] Generated and saved key to AES.key:\r')
		print(f'[INFO] Generated and saved key to AES.key:\r')
		tools.debug_print_arr_hex_1line(key)
		with open('AES.key', 'wb') as kf:
			kf.write(key)

	return key


def set_log(a):
	global logger
	now = datetime.now()
	dt_string = now.strftime("%m%d%Y_%H%M%S")
	logger = logging.getLogger(__name__)

	# Create a log file in eval_files with MMDDYY_HHMMSS_outf.log
	if "Win" in platform.system():
		index = a.outf.rfind('/')
		logging.basicConfig(filename=f'{a.outf}_{dt_string}.log', encoding='utf-8', level=logging.DEBUG)
	if "Darwin" in platform.system():
		index = a.outf.rfind('/')
		logging.basicConfig(filename=f'{a.outf}_{dt_string}.log', encoding='utf-8', level=logging.DEBUG)


if __name__ == '__main__':
	print("------------------------------------")
	print("CSCI-555L AES-128 ECB Implementation")
	print("------------------------------------")
	# print(f'[Processor Info]: {tools.get_processor_name()}\r')
	print(f'[OS]: {platform.system()}\r')
	print(f'[Cores]: {os.cpu_count()}\r')


	parser = argparse.ArgumentParser(prog='aestest.py', description='Perform AES-128 ECB Encryption / Decryption')
	parser.add_argument('-p', action='store_true', help='[Optional] Enable parallelization flag')
	parser.add_argument('-k', action='store', help='[Optional] Key file, omit to generate key')
	parser.add_argument('-w', type=int, default=-1, action='store', help='[Optional] Override MAX Workers')
	parser.add_argument('-i', type=int, default=1, action='store', help='[Optional] Iterations. Default is 1')

	# input file OR generate flags must be set first before defining output
	gen = parser.add_mutually_exclusive_group(required=True)
	gen.add_argument('-g', type=int, action='store', help='[Mutual Exclusive Required] Generate input file of <n> bytes')
	gen.add_argument('-inf', action='store', type=str, default=None, help='[Mutual Exclusive Required] input file')

	parser.add_argument('-outf', action='store', type=str, default=None, help='[Required] output file')

	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument('-d', '--decrypt', action='store_true', help='[Mutual Exclusive Required] Decrypt flag')
	mode.add_argument('-e', '--encrypt', action='store_true', help='[Mutual Exclusive Required] Encrypt flag')

	args = parser.parse_args()

	# Set logger
	set_log(args)

	# Sample output
	arg_printer(args)

	# Argument checker
	arg_checker(args)

	# AES Key Check
	pre_key = key_check(args)

	# Utilize AES-128 key expansion to generate round keys
	tools.print_key_hex(pre_key)
	key = tools.key_expansion(pre_key)

	# TODO : All AES Encrypt/Decrypt should return back times
	# TODO : Merge @sara's evaluation code to wrap time calculation
	for _ in range(args.i):
		if args.p:
			if args.encrypt:
				time, num_bytes = aesencrypt.AES_Encrypt_Parallelized(args, key)
			else:
				time, num_bytes = aesdecrypt.AES_Decrypt_Parallelized(args, key)
		else:
			if args.encrypt:
				time, num_bytes = aesencrypt.AES_Encrypt(args, key)
			else:
				time, num_bytes = aesdecrypt.AES_Decrypt(args, key)

		# Obtain times from individual runs
		TIME_TRIALS.append(time)

		TOTAL_BYTES += num_bytes

	Coefficient_of_Variation = cv(TIME_TRIALS)

	print()
	logger.info("           AES Statistics           ")
	logger.info("------------------------------------")
	logger.info(f'Number of Trials: {len(TIME_TRIALS)}')
	logger.info(f'Time Splits: {TIME_TRIALS}')
	logger.info(f'Average Time: {sum(TIME_TRIALS) / len(TIME_TRIALS)}')
	logger.info(f'Average Throughput: {TOTAL_BYTES / sum(TIME_TRIALS)} Bytes/s')
	logger.info(f'Variance: {statistics.variance(TIME_TRIALS)}')  # NOTE: REQUIRES > 1 ITERATIONS
	logger.info(f'Coefficient of Variation: {Coefficient_of_Variation}')
	logger.info("------------------------------------")
