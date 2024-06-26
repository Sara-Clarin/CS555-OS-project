""" **************************************************************
* Course ID  : CSCI555L - Advanced Operating Systems             *
* Due Date   : TBD                                               *
* Project    : AES128-ECB Implementation                         *
* Purpose    : This project is an implementation of the Advanced *
*              Encryption Standard (AES) using a 128-bit key.    *
*****************************************************************"""
import concurrent
import os
from concurrent.futures import ProcessPoolExecutor

import aesdecrypt
import tools
import time
from multiprocessing import Pool, TimeoutError
import math

MAX_WORKERS = 8

mix_col_matrix = [[0x02, 0x03, 0x01, 0x01],
                   [0x01, 0x02, 0x03, 0x01],
                   [0x01, 0x01, 0x02, 0x03],
                   [0x03, 0x01, 0x01, 0x02]]

r_const = [0x01000000, 0x02000000, 0x04000000, 0x08000000, 0x10000000, 0x20000000, 0x40000000, 0x80000000, 0x1B000000, 0x36000000]

# 
#  LOOKUP TABLE SEGMENT
#
s_box = [[0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
        [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
        [0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],
        [0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],
        [0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],
        [0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],
        [0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],
        [0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],
        [0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73],
        [0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb],
        [0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],
        [0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08],
        [0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a],
        [0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e],
        [0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf],
        [0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]]

table_2 = [0x00,0x02,0x04,0x06,0x08,0x0a,0x0c,0x0e,0x10,0x12,0x14,0x16,0x18,0x1a,0x1c,0x1e,
    0x20,0x22,0x24,0x26,0x28,0x2a,0x2c,0x2e,0x30,0x32,0x34,0x36,0x38,0x3a,0x3c,0x3e,
    0x40,0x42,0x44,0x46,0x48,0x4a,0x4c,0x4e,0x50,0x52,0x54,0x56,0x58,0x5a,0x5c,0x5e,
    0x60,0x62,0x64,0x66,0x68,0x6a,0x6c,0x6e,0x70,0x72,0x74,0x76,0x78,0x7a,0x7c,0x7e,	
    0x80,0x82,0x84,0x86,0x88,0x8a,0x8c,0x8e,0x90,0x92,0x94,0x96,0x98,0x9a,0x9c,0x9e,
    0xa0,0xa2,0xa4,0xa6,0xa8,0xaa,0xac,0xae,0xb0,0xb2,0xb4,0xb6,0xb8,0xba,0xbc,0xbe,
    0xc0,0xc2,0xc4,0xc6,0xc8,0xca,0xcc,0xce,0xd0,0xd2,0xd4,0xd6,0xd8,0xda,0xdc,0xde,
    0xe0,0xe2,0xe4,0xe6,0xe8,0xea,0xec,0xee,0xf0,0xf2,0xf4,0xf6,0xf8,0xfa,0xfc,0xfe,
    0x1b,0x19,0x1f,0x1d,0x13,0x11,0x17,0x15,0x0b,0x09,0x0f,0x0d,0x03,0x01,0x07,0x05,
    0x3b,0x39,0x3f,0x3d,0x33,0x31,0x37,0x35,0x2b,0x29,0x2f,0x2d,0x23,0x21,0x27,0x25,
    0x5b,0x59,0x5f,0x5d,0x53,0x51,0x57,0x55,0x4b,0x49,0x4f,0x4d,0x43,0x41,0x47,0x45,
    0x7b,0x79,0x7f,0x7d,0x73,0x71,0x77,0x75,0x6b,0x69,0x6f,0x6d,0x63,0x61,0x67,0x65,
    0x9b,0x99,0x9f,0x9d,0x93,0x91,0x97,0x95,0x8b,0x89,0x8f,0x8d,0x83,0x81,0x87,0x85,
    0xbb,0xb9,0xbf,0xbd,0xb3,0xb1,0xb7,0xb5,0xab,0xa9,0xaf,0xad,0xa3,0xa1,0xa7,0xa5,
    0xdb,0xd9,0xdf,0xdd,0xd3,0xd1,0xd7,0xd5,0xcb,0xc9,0xcf,0xcd,0xc3,0xc1,0xc7,0xc5,
    0xfb,0xf9,0xff,0xfd,0xf3,0xf1,0xf7,0xf5,0xeb,0xe9,0xef,0xed,0xe3,0xe1,0xe7,0xe5
    ]
table_3 = [
    0x00,0x03,0x06,0x05,0x0c,0x0f,0x0a,0x09,0x18,0x1b,0x1e,0x1d,0x14,0x17,0x12,0x11,
    0x30,0x33,0x36,0x35,0x3c,0x3f,0x3a,0x39,0x28,0x2b,0x2e,0x2d,0x24,0x27,0x22,0x21,
    0x60,0x63,0x66,0x65,0x6c,0x6f,0x6a,0x69,0x78,0x7b,0x7e,0x7d,0x74,0x77,0x72,0x71,
    0x50,0x53,0x56,0x55,0x5c,0x5f,0x5a,0x59,0x48,0x4b,0x4e,0x4d,0x44,0x47,0x42,0x41,
    0xc0,0xc3,0xc6,0xc5,0xcc,0xcf,0xca,0xc9,0xd8,0xdb,0xde,0xdd,0xd4,0xd7,0xd2,0xd1,
    0xf0,0xf3,0xf6,0xf5,0xfc,0xff,0xfa,0xf9,0xe8,0xeb,0xee,0xed,0xe4,0xe7,0xe2,0xe1,
    0xa0,0xa3,0xa6,0xa5,0xac,0xaf,0xaa,0xa9,0xb8,0xbb,0xbe,0xbd,0xb4,0xb7,0xb2,0xb1,
    0x90,0x93,0x96,0x95,0x9c,0x9f,0x9a,0x99,0x88,0x8b,0x8e,0x8d,0x84,0x87,0x82,0x81,	
    0x9b,0x98,0x9d,0x9e,0x97,0x94,0x91,0x92,0x83,0x80,0x85,0x86,0x8f,0x8c,0x89,0x8a,
    0xab,0xa8,0xad,0xae,0xa7,0xa4,0xa1,0xa2,0xb3,0xb0,0xb5,0xb6,0xbf,0xbc,0xb9,0xba,
    0xfb,0xf8,0xfd,0xfe,0xf7,0xf4,0xf1,0xf2,0xe3,0xe0,0xe5,0xe6,0xef,0xec,0xe9,0xea,	
    0xcb,0xc8,0xcd,0xce,0xc7,0xc4,0xc1,0xc2,0xd3,0xd0,0xd5,0xd6,0xdf,0xdc,0xd9,0xda,	
    0x5b,0x58,0x5d,0x5e,0x57,0x54,0x51,0x52,0x43,0x40,0x45,0x46,0x4f,0x4c,0x49,0x4a,
    0x6b,0x68,0x6d,0x6e,0x67,0x64,0x61,0x62,0x73,0x70,0x75,0x76,0x7f,0x7c,0x79,0x7a,	
    0x3b,0x38,0x3d,0x3e,0x37,0x34,0x31,0x32,0x23,0x20,0x25,0x26,0x2f,0x2c,0x29,0x2a,
    0x0b,0x08,0x0d,0x0e,0x07,0x04,0x01,0x02,0x13,0x10,0x15,0x16,0x1f,0x1c,0x19,0x1a
    ]

table_9 = [0x00,0x09,0x12,0x1b,0x24,0x2d,0x36,0x3f,0x48,0x41,0x5a,0x53,0x6c,0x65,0x7e,0x77,
    0x90,0x99,0x82,0x8b,0xb4,0xbd,0xa6,0xaf,0xd8,0xd1,0xca,0xc3,0xfc,0xf5,0xee,0xe7,
    0x3b,0x32,0x29,0x20,0x1f,0x16,0x0d,0x04,0x73,0x7a,0x61,0x68,0x57,0x5e,0x45,0x4c,
    0xab,0xa2,0xb9,0xb0,0x8f,0x86,0x9d,0x94,0xe3,0xea,0xf1,0xf8,0xc7,0xce,0xd5,0xdc,
    0x76,0x7f,0x64,0x6d,0x52,0x5b,0x40,0x49,0x3e,0x37,0x2c,0x25,0x1a,0x13,0x08,0x01,
    0xe6,0xef,0xf4,0xfd,0xc2,0xcb,0xd0,0xd9,0xae,0xa7,0xbc,0xb5,0x8a,0x83,0x98,0x91,
    0x4d,0x44,0x5f,0x56,0x69,0x60,0x7b,0x72,0x05,0x0c,0x17,0x1e,0x21,0x28,0x33,0x3a,
    0xdd,0xd4,0xcf,0xc6,0xf9,0xf0,0xeb,0xe2,0x95,0x9c,0x87,0x8e,0xb1,0xb8,0xa3,0xaa,	
    0xec,0xe5,0xfe,0xf7,0xc8,0xc1,0xda,0xd3,0xa4,0xad,0xb6,0xbf,0x80,0x89,0x92,0x9b,	
    0x7c,0x75,0x6e,0x67,0x58,0x51,0x4a,0x43,0x34,0x3d,0x26,0x2f,0x10,0x19,0x02,0x0b,
    0xd7,0xde,0xc5,0xcc,0xf3,0xfa,0xe1,0xe8,0x9f,0x96,0x8d,0x84,0xbb,0xb2,0xa9,0xa0,
    0x47,0x4e,0x55,0x5c,0x63,0x6a,0x71,0x78,0x0f,0x06,0x1d,0x14,0x2b,0x22,0x39,0x30,
    0x9a,0x93,0x88,0x81,0xbe,0xb7,0xac,0xa5,0xd2,0xdb,0xc0,0xc9,0xf6,0xff,0xe4,0xed,
    0x0a,0x03,0x18,0x11,0x2e,0x27,0x3c,0x35,0x42,0x4b,0x50,0x59,0x66,0x6f,0x74,0x7d,	
    0xa1,0xa8,0xb3,0xba,0x85,0x8c,0x97,0x9e,0xe9,0xe0,0xfb,0xf2,0xcd,0xc4,0xdf,0xd6,
    0x31,0x38,0x23,0x2a,0x15,0x1c,0x07,0x0e,0x79,0x70,0x6b,0x62,0x5d,0x54,0x4f,0x46
    ]

table_11 = [0x00,0x0b,0x16,0x1d,0x2c,0x27,0x3a,0x31,0x58,0x53,0x4e,0x45,0x74,0x7f,0x62,0x69,
    0xb0,0xbb,0xa6,0xad,0x9c,0x97,0x8a,0x81,0xe8,0xe3,0xfe,0xf5,0xc4,0xcf,0xd2,0xd9,
    0x7b,0x70,0x6d,0x66,0x57,0x5c,0x41,0x4a,0x23,0x28,0x35,0x3e,0x0f,0x04,0x19,0x12,
    0xcb,0xc0,0xdd,0xd6,0xe7,0xec,0xf1,0xfa,0x93,0x98,0x85,0x8e,0xbf,0xb4,0xa9,0xa2,
    0xf6,0xfd,0xe0,0xeb,0xda,0xd1,0xcc,0xc7,0xae,0xa5,0xb8,0xb3,0x82,0x89,0x94,0x9f,
    0x46,0x4d,0x50,0x5b,0x6a,0x61,0x7c,0x77,0x1e,0x15,0x08,0x03,0x32,0x39,0x24,0x2f,
    0x8d,0x86,0x9b,0x90,0xa1,0xaa,0xb7,0xbc,0xd5,0xde,0xc3,0xc8,0xf9,0xf2,0xef,0xe4,
    0x3d,0x36,0x2b,0x20,0x11,0x1a,0x07,0x0c,0x65,0x6e,0x73,0x78,0x49,0x42,0x5f,0x54,
    0xf7,0xfc,0xe1,0xea,0xdb,0xd0,0xcd,0xc6,0xaf,0xa4,0xb9,0xb2,0x83,0x88,0x95,0x9e,
    0x47,0x4c,0x51,0x5a,0x6b,0x60,0x7d,0x76,0x1f,0x14,0x09,0x02,0x33,0x38,0x25,0x2e,
    0x8c,0x87,0x9a,0x91,0xa0,0xab,0xb6,0xbd,0xd4,0xdf,0xc2,0xc9,0xf8,0xf3,0xee,0xe5,
    0x3c,0x37,0x2a,0x21,0x10,0x1b,0x06,0x0d,0x64,0x6f,0x72,0x79,0x48,0x43,0x5e,0x55,
    0x01,0x0a,0x17,0x1c,0x2d,0x26,0x3b,0x30,0x59,0x52,0x4f,0x44,0x75,0x7e,0x63,0x68,
    0xb1,0xba,0xa7,0xac,0x9d,0x96,0x8b,0x80,0xe9,0xe2,0xff,0xf4,0xc5,0xce,0xd3,0xd8,
    0x7a,0x71,0x6c,0x67,0x56,0x5d,0x40,0x4b,0x22,0x29,0x34,0x3f,0x0e,0x05,0x18,0x13,
    0xca,0xc1,0xdc,0xd7,0xe6,0xed,0xf0,0xfb,0x92,0x99,0x84,0x8f,0xbe,0xb5,0xa8,0xa3
]
table_13 = [
    0x00,0x0d,0x1a,0x17,0x34,0x39,0x2e,0x23,0x68,0x65,0x72,0x7f,0x5c,0x51,0x46,0x4b,
    0xd0,0xdd,0xca,0xc7,0xe4,0xe9,0xfe,0xf3,0xb8,0xb5,0xa2,0xaf,0x8c,0x81,0x96,0x9b,
    0xbb,0xb6,0xa1,0xac,0x8f,0x82,0x95,0x98,0xd3,0xde,0xc9,0xc4,0xe7,0xea,0xfd,0xf0,
    0x6b,0x66,0x71,0x7c,0x5f,0x52,0x45,0x48,0x03,0x0e,0x19,0x14,0x37,0x3a,0x2d,0x20,
    0x6d,0x60,0x77,0x7a,0x59,0x54,0x43,0x4e,0x05,0x08,0x1f,0x12,0x31,0x3c,0x2b,0x26,
    0xbd,0xb0,0xa7,0xaa,0x89,0x84,0x93,0x9e,0xd5,0xd8,0xcf,0xc2,0xe1,0xec,0xfb,0xf6,
    0xd6,0xdb,0xcc,0xc1,0xe2,0xef,0xf8,0xf5,0xbe,0xb3,0xa4,0xa9,0x8a,0x87,0x90,0x9d,
    0x06,0x0b,0x1c,0x11,0x32,0x3f,0x28,0x25,0x6e,0x63,0x74,0x79,0x5a,0x57,0x40,0x4d,
    0xda,0xd7,0xc0,0xcd,0xee,0xe3,0xf4,0xf9,0xb2,0xbf,0xa8,0xa5,0x86,0x8b,0x9c,0x91,
    0x0a,0x07,0x10,0x1d,0x3e,0x33,0x24,0x29,0x62,0x6f,0x78,0x75,0x56,0x5b,0x4c,0x41,
    0x61,0x6c,0x7b,0x76,0x55,0x58,0x4f,0x42,0x09,0x04,0x13,0x1e,0x3d,0x30,0x27,0x2a,
    0xb1,0xbc,0xab,0xa6,0x85,0x88,0x9f,0x92,0xd9,0xd4,0xc3,0xce,0xed,0xe0,0xf7,0xfa,
    0xb7,0xba,0xad,0xa0,0x83,0x8e,0x99,0x94,0xdf,0xd2,0xc5,0xc8,0xeb,0xe6,0xf1,0xfc,
    0x67,0x6a,0x7d,0x70,0x53,0x5e,0x49,0x44,0x0f,0x02,0x15,0x18,0x3b,0x36,0x21,0x2c,
    0x0c,0x01,0x16,0x1b,0x38,0x35,0x22,0x2f,0x64,0x69,0x7e,0x73,0x50,0x5d,0x4a,0x47,
    0xdc,0xd1,0xc6,0xcb,0xe8,0xe5,0xf2,0xff,0xb4,0xb9,0xae,0xa3,0x80,0x8d,0x9a,0x97
]
table_14 = [
    0x00,0x0e,0x1c,0x12,0x38,0x36,0x24,0x2a,0x70,0x7e,0x6c,0x62,0x48,0x46,0x54,0x5a,
    0xe0,0xee,0xfc,0xf2,0xd8,0xd6,0xc4,0xca,0x90,0x9e,0x8c,0x82,0xa8,0xa6,0xb4,0xba,
    0xdb,0xd5,0xc7,0xc9,0xe3,0xed,0xff,0xf1,0xab,0xa5,0xb7,0xb9,0x93,0x9d,0x8f,0x81,
    0x3b,0x35,0x27,0x29,0x03,0x0d,0x1f,0x11,0x4b,0x45,0x57,0x59,0x73,0x7d,0x6f,0x61,
    0xad,0xa3,0xb1,0xbf,0x95,0x9b,0x89,0x87,0xdd,0xd3,0xc1,0xcf,0xe5,0xeb,0xf9,0xf7,
    0x4d,0x43,0x51,0x5f,0x75,0x7b,0x69,0x67,0x3d,0x33,0x21,0x2f,0x05,0x0b,0x19,0x17,
    0x76,0x78,0x6a,0x64,0x4e,0x40,0x52,0x5c,0x06,0x08,0x1a,0x14,0x3e,0x30,0x22,0x2c,
    0x96,0x98,0x8a,0x84,0xae,0xa0,0xb2,0xbc,0xe6,0xe8,0xfa,0xf4,0xde,0xd0,0xc2,0xcc,
    0x41,0x4f,0x5d,0x53,0x79,0x77,0x65,0x6b,0x31,0x3f,0x2d,0x23,0x09,0x07,0x15,0x1b,
    0xa1,0xaf,0xbd,0xb3,0x99,0x97,0x85,0x8b,0xd1,0xdf,0xcd,0xc3,0xe9,0xe7,0xf5,0xfb,
    0x9a,0x94,0x86,0x88,0xa2,0xac,0xbe,0xb0,0xea,0xe4,0xf6,0xf8,0xd2,0xdc,0xce,0xc0,
    0x7a,0x74,0x66,0x68,0x42,0x4c,0x5e,0x50,0x0a,0x04,0x16,0x18,0x32,0x3c,0x2e,0x20,
    0xec,0xe2,0xf0,0xfe,0xd4,0xda,0xc8,0xc6,0x9c,0x92,0x80,0x8e,0xa4,0xaa,0xb8,0xb6,
    0x0c,0x02,0x10,0x1e,0x34,0x3a,0x28,0x26,0x7c,0x72,0x60,0x6e,0x44,0x4a,0x58,0x56,
    0x37,0x39,0x2b,0x25,0x0f,0x01,0x13,0x1d,0x47,0x49,0x5b,0x55,0x7f,0x71,0x63,0x6d,
    0xd7,0xd9,0xcb,0xc5,0xef,0xe1,0xf3,0xfd,0xa7,0xa9,0xbb,0xb5,0x9f,0x91,0x83,0x8d
]
#
# END LOOKUP TABLE SEGMENT
#



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


def xor_2d(arr1, arr2):
    """
    Function :   xor_2d
    Parameters : arr1 - 2D hexadecimal array
                 arr2 - 2D hexadecimal array
    Output :     arr1 - 2D hexadecimal array that has been XOR'ed by arr2
    Description: Iterates through every element of both 2D arrays and XOR's arr1[row][col] ^ arr2[row][col].
                 arr1 used as storage and returned back to caller.
                 Used in key addition
    """
    for i in range(len(arr1)):
        arr1[i] = [ arr1[i][j]^arr2[i][j] for j in range(len(arr1[0]))]
        
        #for j in range(len(arr1[0])):
        #    val = arr1[i][j] ^ arr2[i][j]
        #    arr1[i][j] = val
        
    return arr1


def rot_word_L(word, amt):
    """
    Function :   rot_word_L
    Parameters : word - current 32 bit unsigned word
                 amt - requested rotate left amount
    Output :     32-bit unsigned word
    Description: Rotates a 32-bit word by requested amount using bit shifts, then returning new value back to caller
                 Needed for Key Expansion and Shift Rows
    """
    if amt == 1:
        return ((word << 8) & 0xFFFFFF00) | ((word >> 24) & 0x000000FF)
    elif amt == 2:
        return ((word << 16) & 0xFFFF0000) | ((word >> 16) & 0x0000FFFF)
    elif amt == 3:
        return ((word << 24) & 0xFF000000) | ((word >> 8) & 0x00FFFFFF)


def s_box_sub(state):
    """
    Function :   s_box_sub
    Parameters : state array
    Output :     updated state array
    Description: Perform S-Box substitution on the entire 16-byte state array
    """
    for i, row in enumerate(state):
        for j, col in enumerate(row):
            ms_nibble = (state[i][j] & 0xF0) >> 4
            ls_nibble = (state[i][j] & 0x0F)
            state[i][j] = s_box[ms_nibble][ls_nibble]

    return state


def sub_word(input_word):
    """
    Function :   sub_word
    Parameters : (x1) 32-bit word
    Output :     (x1) 32-bit word that has been substituted by S-Box
    Description: Perform S-Box substitution on (x1) 32-bit word
    """
    byte_arr = input_word.to_bytes(4, 'big')
    ret_word = [0,0,0,0]
    for i, byte in enumerate(byte_arr):
        ms_nibble = (byte & 0xF0) >> 4
        ls_nibble = (byte & 0x0F)
        ret_word[i] = s_box[ms_nibble][ls_nibble]

    return int.from_bytes(ret_word, 'big')


def shift_rows(state):
    """
    Function :   shift_rows
    Parameters : state array
    Output :     update state array
    Description: shift all rows by set amount
    """
    for i in range(1,4,1):
        word = rot_word_L(state[i][0] << 24 | state[i][1] << 16 | state[i][2] << 8 | state[i][3], i)
        converter = word.to_bytes(4, byteorder='big', signed=False)
        state[i][:] = converter

def mix_cols(state):
    """
    Function :   mix_cols
    Parameters : state array
    Output :     updated state array
    Description: Mix Columns driver
    """
    temp = [[0x00, 0x00, 0x00, 0x00],
            [0x00, 0x00, 0x00, 0x00],
            [0x00, 0x00, 0x00, 0x00],
            [0x00, 0x00, 0x00, 0x00]]

    for i in range(4):
        for j in range(4):
            #curr_col = [state[0][j], state[1][j], state[2][j], state[3][j]]
            curr_col = [state[x][j] for x in range(4)]
            temp[i][j] = mix_columns_transform(i, curr_col)
            #temp[i][j] = mix_cols_fast(i, curr_col)

    return temp

def fast_m_cols(state):
    '''
    mix columns function, improved over mix_cols to have fewer functions cols
    goal: increase performance over previous method
    '''
    tempstate = [[0x00 for _ in range(4)] for _ in range(4)]
    temp = 0x00

    for i in range(4):
        for j in range(4):
            temp = 0x00

            #for k, stateval in enumerate()
            curr_col = [state[x][j] for x in range(4)]

            for k, stateval in enumerate(curr_col):
                GF_elem = mix_col_matrix[i][k]

                if GF_elem == 0x01:
                    temp ^= stateval

                elif GF_elem == 0x02:
                    temp ^= table_2[int(stateval)]

                else: # GF_elem == 3
                    temp ^= table_3[int(stateval)]

            tempstate[i][j] = temp
    return tempstate

def mix_cols_fast(I_row, S_col):
    '''
    Lookup-table version of mix_columns transform
    '''
    temp = 0x00 
    
    for i, stateval in enumerate(S_col):
        GF_elem = mix_col_matrix[I_row][i]

        if GF_elem == 0x01:
            temp ^= stateval

        elif GF_elem == 0x02:
            temp ^= table_2[int(stateval)]

        else: # GF_elem == 3
            temp ^= table_3[int(stateval)]
    
    return temp


def mix_columns_transform(I_row, S_Col):
    """
    Function :   mix_columns_transform
    Parameters : Current index row, state column
    Output :     1 Byte
    Description: Performs Mix Columns using polynomials over GF(2^8)
    """
    temp = 0x00

    """Iterates over current Mix Col row and state array column to perform matrix multiplication"""
    for i in range(len(mix_col_matrix[I_row])):  # maybe can hardcode this to 4

        element = mix_col_matrix[I_row][i]


        """
        Determine if you are multiplying either by 0x02, 0x03, or 0x01
        If MS bit is set before multiplying temp by 2, XOR temp using polynomial x^4 + x^3 + x^2 + 1 (0x1B)
        """
        if element == 0x02:    # could store S_Col[i] as a variable so no lookups
            temp ^= (S_Col[i] << 1)
            if S_Col[i] >= 0x80:    # try "if x && y != z" instead of comparator
                temp ^= 0x1B

        elif element == 0x03:
            temp ^= S_Col[i] ^ (S_Col[i] << 1)

            if S_Col[i] >= 0x80:  # if hi_bit_set
                temp ^= 0x1B

        else:
            temp ^= S_Col[i]

    return temp & 0xFF           # How is this different than return temp?

def key_expansion(aes_key):
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
            temp = rot_word_L(temp, 1)
            temp = sub_word(temp)
            temp ^= r_const[r_const_ptr]
            r_const_ptr += 1

        temp ^= w[x - 4]
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


def extract_key(key):
    """
    Function :   extract_key
    Parameters : Key List
    Output :     Returns key from 1D space into 2D space
    Description: Turn 1D byte array into 2D for easy XOR operations
    """
    byte_arr = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

    #print(f'Key in extract_key: {key}')

    for i in range(4):
        converter = key[i].to_bytes(4, byteorder='big', signed=False)
        byte_arr[0][i] = int(converter[0])
        byte_arr[1][i] = int(converter[1])
        byte_arr[2][i] = int(converter[2])
        byte_arr[3][i] = int(converter[3])

    return byte_arr


def populate_state(state, pt, curr_round):
    """
    Function :   populate_state
    Parameters : empty state array, plaintext, current encryption round
    Output :     Returns state array with populated plaintext
    Description: Turn 1D byte array into 2D state array using respective indexing
    """
    for col in range(len(state[0])):
        state[0][col] = pt[(col * 4) + (curr_round * 16)]
        state[1][col] = pt[(col * 4 + 1) + (curr_round * 16)]
        state[2][col] = pt[(col * 4 + 2) + (curr_round * 16)]
        state[3][col] = pt[(col * 4 + 3) + (curr_round * 16)]


def state_store(state, ct):
    """
    Function :   state_store
    Parameters : encrypted state array, ciphertext byte array
    Output :     Returns ciphertext byte array with 16 extra bytes
    Description: Used to correctly store bytes in order from AES state array
                 Loop through all column elements and store in 1d array using list comprehension
    Website:     https://www.w3schools.com/python/python_lists_comprehension.asp
    """
    for j in range(len(state[0])):
        column = [row[j] for row in state]
        for elem in column:
            ct.append(elem)


def aes_encrypt(pt, key):
    """
    Function :   aes_encrypt
    Parameters : 1D Plaintext Byte array, 1D key array (16 bytes)
    Output :     1D ciphertext array
    Description: AES-128 Encryption Algorithm
    """
    ciphertext = bytearray([])
    num_blocks = int(len(pt) / 16)
    curr_round = 0

    """generate key schedule for all 10 rounds"""
    key_schedule = key

    """for-loop to iterate over all 16-byte plaintext blocks"""
    for i in range(num_blocks):
        state = [[0x00, 0x00, 0x00, 0x00], [0x00, 0x00, 0x00, 0x00], [0x00, 0x00, 0x00, 0x00], [0x00, 0x00, 0x00, 0x00]]

        """This function will turn the 1D plaintext into multiple 2D state arrays"""
        populate_state(state, pt, curr_round)

        round_key = extract_key(key_schedule[0])

        state = xor_2d(state, round_key)

        """Perform necessary shifting, mixing, and substitution on 2D state array"""
        for aes_round in range(1, 11, 1):

            s_box_sub(state)

            shift_rows(state)

            """Mix Columns skipped for only round 10"""
            if aes_round != 10:
                state = fast_m_cols(state)

            round_key = extract_key(key_schedule[aes_round])

            state = xor_2d(state, round_key)
        
        """Store 16 extra bytes into ciphertext"""
        state_store(state, ciphertext)

        """Update current cipher round for indexing"""
        curr_round += 1

    return ciphertext

def aes_enc_parallel( padded, key, chunksize):
    """
    Function :   AES_Encrypt_Parallelized
    Parameters : padded plaintext string, bytestring key
    Output :     None
    Description: Perform Parallelized AES Encryption
    """
    print("[INFO]: Parallelized Encryption")
    ciphertext = b''
    encrypted_blocks = []
    futures = []

    parts = []
    max_workers = 8
    # Loop to create parts
    part_size = len(padded) // max_workers

    if (remainder := (part_size % 16)) != 0:  # take chunks that are multiples of 16
        print(f'Our remainder is: {remainder}')
        part_size -= remainder

    full_parts = math.floor( len(padded) // part_size)
    remaining_blocks = len(padded) - full_parts*part_size

    ind = 0
    for i in range(0, full_parts):
        parts.append(padded[ind:ind+part_size])
        ind += part_size

    if remaining_blocks > 0:
        parts.append(padded[ind::])
    
    start = time.time_ns()
    # map(): Apply a function to an iterable of elements.
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures.extend(executor.submit(aes_encrypt, part, key) for part in parts)

        for future in futures:
            encrypted_blocks.append(future.result())

    # Concatenate the encrypted blocks in the original order
    ciphertext = b''.join(encrypted_blocks)
    end = time.time_ns()

    print(f'[INFO]: Parallelized AES Encryption took {(end - start) / 1e9} s')
    #return ciphertext

def aes_encrypt_single_block(pt, key):
    """
    Function :   aes_encrypt
    Parameters : 1D Plaintext Byte array, 1D key array (16 bytes)
    Output :     1D ciphertext array
    Description: AES-128 Encryption Algorithm
    """
    ciphertext = bytearray([])
    curr_round = 0

    key_schedule = key

    """for-loop to iterate over all 16-byte plaintext blocks"""
    state = [[0x00, 0x00, 0x00, 0x00], [0x00, 0x00, 0x00, 0x00], [0x00, 0x00, 0x00, 0x00], [0x00, 0x00, 0x00, 0x00]]

    """This function will turn the 1D plaintext into multiple 2D state arrays"""
    populate_state(state, pt, curr_round)

    round_key = extract_key(key_schedule[0])

    state = xor_2d(state, round_key)

    """Perform necessary shifting, mixing, and substitution on 2D state array"""
    for aes_round in range(1, 11, 1):

        s_box_sub(state)

        shift_rows(state)

        """Mix Columns skipped for only round 10"""
        if aes_round != 10:
            state = mix_cols(state)

        round_key = extract_key(key_schedule[aes_round])

        state = xor_2d(state, round_key)

    """Store 16 extra bytes into ciphertext"""
    state_store(state, ciphertext)

    """Update current cipher round for indexing"""
    #curr_round += 1
    return ciphertext


def aes_enc_main(pt, key):
    """
    Function :   main
    Parameters : 1D Plaintext Byte array, 1D key array (16 bytes)
    Output :     None
    Description: AES Encrypt driver - must be called from aestest.py
    Usage:       python aestest.py "<StringtoEncrypt>"
    """
    # generate n-byte ciphertext
    ciphertext = aes_encrypt(pt, key)

    print('[aesencrypt.py] Ciphertext:')
    debug_print_arr_hex_1line(ciphertext)
    print()

    # Calling aesdecrypt.py to handle decryption
    aesdecrypt.aes_dec_main(ciphertext, key)


def AES_Encrypt(args, key):
    """
    Function :   AES_Encrypt
    Parameters : program arguments, key schedule array
    Output :     None
    Description: Perform Non-Parallelized AES Encryption
    """
    #print("[INFO]: Non-Parallelized Encryption")
    ciphertext = b''
    encrypted_blocks = []
    with open(args.inf, 'rb') as infile:
        data = infile.read()

        if len(data) % 16 != 0:
            padded = tools.iso_iec_7816_4_pad(data)
            num_blocks = int(len(padded)/16)
        else:
            num_blocks = int(len(data)/16)
            padded = data

        start = time.time_ns()
        for x in range(num_blocks):
            block = padded[x*16: (x*16)+16]
            encrypted_blocks.append(aes_encrypt(block, key))
            #print(f'[INFO]: Blocks remaining: {num_blocks - x}')
        end = time.time_ns()
        total_time = (end - start) / 1e9
        #print(f'[INFO]: Non-Parallelized AES Encryption took {total_time} s')

    # combine into single bytestream
    ciphertext = b''.join(encrypted_blocks)
    
    with open(args.outf, 'wb+') as outfile:
        outfile.write(ciphertext)

    return total_time, len(ciphertext)


def AES_Encrypt_Parallelized(args, key):
    """
    Function :   AES_Encrypt_Parallelized
    Parameters : program arguments, key schedule array
    Output :     None
    Description: Perform Parallelized AES Encryption
    """
    #print("[INFO]: Parallelized Encryption")
    ciphertext = b''
    encrypted_blocks = []
    futures = []
    parts = []
    global MAX_WORKERS
    with open(args.inf, 'rb') as infile:
        data = infile.read()

        if len(data) % 16 != 0:
            padded = tools.iso_iec_7816_4_pad(data)
            num_blocks = int(len(padded)/16)
        else:
            num_blocks = int(len(data)/16)
            padded = data

        # Check if user has override MAX_WORKERS
        if args.w != -1:
            workers = args.w
        else:
            workers = MAX_WORKERS

        print(f'[INFO]: Max workers: {workers}\r')

        # Loop to create parts
        split = 6500

        #part_size = len(padded) // workers
        part_size = len(padded) // split

        if (remainder := (part_size % 16)) != 0:  # take chunks that are multiples of 16
            part_size -= remainder

        if part_size <= 0:
            full_parts = 1
        else:
            full_parts = math.floor(len(padded) // part_size)
        remaining_blocks = len(padded) - full_parts*part_size

        ind = 0
        for i in range(0, full_parts):
            parts.append(padded[ind:ind+part_size])
            ind += part_size

        if remaining_blocks > 0:
            parts.append(padded[ind::])
        
        print(f'Number of blocks fed to each process: {part_size / 16}')
        print(f'Ways that we split the pool{split}')

        start = time.time_ns()
        # map(): Apply a function to an iterable of elements.
        with ProcessPoolExecutor(max_workers=workers) as executor:
            futures.extend(executor.submit(aes_encrypt, part, key) for part in parts)

            for future in futures:
                encrypted_blocks.append(future.result())

        # Concatenate the encrypted blocks in the original order
        ciphertext = b''.join(encrypted_blocks)
        end = time.time_ns()

        total_time = (end - start) / 1e9
        #print(f'[INFO]: Parallelized AES Encryption took {total_time} s')
        with open(args.outf, 'wb+') as outfile:
            outfile.write(ciphertext)

        return total_time, len(ciphertext)

    
def encryptor(arguments):
    return aes_encrypt(*arguments)

def AES_Enc_Parallel_chunksize(args, key):
    """
    Function :   AES_Encrypt_Parallelized
    Parameters : program arguments, key schedule array
    Output :     None
    Description: Perform Parallelized AES Encryption
    """
    ciphertext = b''
    encrypted_blocks = []

    global MAX_WORKERS
    with open(args.inf, 'rb') as infile:
        data = infile.read()

        if len(data) % 16 != 0:
            padded = tools.iso_iec_7816_4_pad(data)
            num_blocks = int(len(padded)/16)
        else:
            num_blocks = int(len(data)/16)
            padded = data

        # Check if user has override MAX_WORKERS
        if args.w != -1:
            workers = args.w
        else:
            workers = MAX_WORKERS

        # SET CHUNKSIZE (number of blocks per process at a time)
        chunkSize = args.c

        blocks = []
        for x in range(num_blocks):
            block = padded[x*16: (x*16)+16]
            blocks.append(block)

        
        print(f'Chunksize: is {chunkSize} blocks per process')
        arguments = [(block, key) for block in blocks]

        start = time.time_ns()
        # map(): Apply a function to an iterable of elements.
        with ProcessPoolExecutor(max_workers=workers) as executor:
            for result in executor.map(encryptor, arguments, chunksize=chunkSize ):
                encrypted_blocks.append(result) 
            

        # Concatenate the encrypted blocks in the original order
        ciphertext = b''.join(encrypted_blocks)
        end = time.time_ns()

        total_time = (end - start) / 1e9
        with open(args.outf, 'wb+') as outfile:
            outfile.write(ciphertext)

        return total_time

