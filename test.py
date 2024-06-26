""" **************************************************************
* Course ID  : CSCI555L - Advanced Operating Systems             *
* Due Date   : TBD                                               *
* Project    : AES128-ECB Implementation                         *
* Purpose    : This file is to test AES engine in aesdecrypt.py  *
               and aesencrypt.py.                                *
                                                                 *
               Conforms to Appendix B— Cipher Example of FIPS-197*
*****************************************************************"""
import platform

import aesencrypt
import aesdecrypt
import tools
import unittest

def inv_shift_rows_test():
    KAT = [0x00, 0x44, 0x88, 0xcc], [0x11, 0x55, 0x99, 0xdd], [0x22, 0x66, 0xaa, 0xee], [0x33, 0x77, 0xbb, 0xff]  #Test vector FIPS197
    state = [0x00, 0x44, 0x88, 0xcc], [0x11, 0x55, 0x99, 0xdd], [0x22, 0x66, 0xaa, 0xee], [0x33, 0x77, 0xbb, 0xff] #Test vector FIPS197


    print(f'[START] Inv Shift Rows Test')
    aesencrypt.shift_rows(state)
    tools.debug_print_arr_2dhex(state)
    print()

    aesdecrypt.shift_rows_inv(state)
    tools.debug_print_arr_2dhex(state)

    tools.compare_2d(state, KAT, 0)
    print()


    print(f'[END] Inv Shift Rows Test')

def key_expansion_test():
    print(f'[START] Key Expansion Test')
    key = [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c]
    key = aesencrypt.key_expansion(key)
    """
    KAT = [ 0x2b7e1516,0x28aed2a6,0xabf71588,0x09cf4f3c,
            0xa0fafe17,0x88542cb1,0x23a33939,0x2a6c7605,
            0xf2c295f2,0x7a96b943,0x5935807a,0x7359f67f,
            0x3d80477d,0x4716fe3e,0x1e237e44,0x6d7a883b,
            0xef44a541,0xa8525b7f,0xb671253b,0xdb0bad00,
            0xd4d1c6f8,0x7c839d87,0xcaf2b8bc,0x11f915bc,
            0x6d88a37a,0x110b3efd,0xdbf98641,0xca0093fd,
            0x4e54f70e,0x5f5fc9f3,0x84a64fb2,0x4ea6dc4f,
            0xead27321,0xb58dbad2,0x312bf560,0x7f8d292f,
            0xac7766f3,0x19fadc21,0x28d12941,0x575c006e,
            0xd014f9a8,0xc9ee2589,0xe13f0cc8,0xb6630ca6 ]
    tools.compare_word(key, KAT)

    tools.debug_print_arr_hex(key)
"""
    tools.debug_print_arr_2dhex(key)
    print(f'[END] Key Expansion Test')

def sub_bytes_test():
    print(f'[START] Sub bytes Test')
    before0 = [[0x19, 0xa0, 0x9a, 0xe9], [0x3d, 0xf4, 0xc6, 0xf8], [0xe3, 0xe2, 0x8d, 0x48], [0xbe, 0x2b, 0x2a, 0x08]]
    state = aesencrypt.s_box_sub(before0)
    KAT0 = [[0xd4, 0xe0, 0xb8, 0x1e], [0x27, 0xbf, 0xb4, 0x41], [0x11, 0x98, 0x5d, 0x52], [0xae, 0xf1, 0xe5, 0x30]]
    tools.compare_2d(state, KAT0, 0)

    before1 = [[0xa4, 0x68, 0x6b, 0x02], [0x9c, 0x9f, 0x5b, 0x6a], [0x7f, 0x35, 0xea, 0x50], [0xf2, 0x2b, 0x43, 0x49]]
    state = aesencrypt.s_box_sub(before1)
    KAT1 = [[0x49, 0x45, 0x7f, 0x77], [0xde, 0xdb, 0x39, 0x02], [0xd2, 0x96, 0x87, 0x53], [0x89, 0xf1, 0x1a, 0x3b]]
    tools.compare_2d(state, KAT1, 1)

    before2 = [[0xaa, 0x61, 0x82, 0x68], [0x8f, 0xdd, 0xd2, 0x32], [0x5f, 0xe3, 0x4a, 0x46], [0x03, 0xef, 0xd2, 0x9a]]
    state = aesencrypt.s_box_sub(before2)
    KAT2 = [[0xac, 0xef, 0x13, 0x45], [0x73, 0xc1, 0xb5, 0x23], [0xcf, 0x11, 0xd6, 0x5a], [0x7b, 0xdf, 0xb5, 0xb8]]
    tools.compare_2d(state, KAT2, 2)

    before3 = [[0x48, 0x67, 0x4d, 0xd6], [0x6c, 0x1d, 0xe3, 0x5f], [0x4e, 0x9d, 0xb1, 0x58], [0xee, 0x0d, 0x38, 0xe7]]
    state = aesencrypt.s_box_sub(before3)
    KAT3 = [[0x52, 0x85, 0xe3, 0xf6], [0x50, 0xa4, 0x11, 0xcf], [0x2f, 0x5e, 0xc8, 0x6a], [0x28, 0xd7, 0x07, 0x94]]
    tools.compare_2d(state, KAT3, 3)

    before4 = [[0xe0, 0xc8, 0xd9, 0x85], [0x92, 0x63, 0xb1, 0xb8], [0x7f, 0x63, 0x35, 0xbe], [0xe8, 0xc0, 0x50, 0x01]]
    state = aesencrypt.s_box_sub(before4)
    KAT4 = [[0xe1, 0xe8, 0x35, 0x97], [0x4f, 0xfb, 0xc8, 0x6c], [0xd2, 0xfb, 0x96, 0xae], [0x9b, 0xba, 0x53, 0x7c]]
    tools.compare_2d(state, KAT4, 4)

    print(f'[END] Sub bytes Test')

def mix_cols_test():

    print(f'[START] Mix Columns Test:')
    before0 = [[0xd4, 0xe0, 0xb8, 0x1e], [0xbf, 0xb4, 0x41, 0x27], [0x5d, 0x52, 0x11, 0x98], [0x30, 0xae, 0xf1, 0xe5]]
    state = aesencrypt.mix_cols(before0)
    KAT0 = [[0x04, 0xe0, 0x48, 0x28], [0x66, 0xcb, 0xf8, 0x06], [0x81, 0x19, 0xd3, 0x26], [0xe5, 0x9a, 0x7a, 0x4c]]
    tools.compare_2d(state, KAT0, 0)



    before1 = [[0x49, 0x45, 0x7f, 0x77], [0xdb, 0x39, 0x02, 0xde], [0x87, 0x53, 0xd2, 0x96], [0x3b, 0x89, 0xf1, 0x1a]]
    state = aesencrypt.mix_cols(before1)
    KAT1 = [0x58, 0x1b, 0xdb, 0x1b], [0x4d, 0x4b, 0xe7, 0x6b], [0xca, 0x5a, 0xca, 0xb0], [0xf1, 0xac, 0xa8, 0xe5]
    tools.compare_2d(state, KAT1, 1)


    before2 = [[0xac, 0xef, 0x13, 0x45], [0xc1, 0xb5, 0x23, 0x73], [0xd6, 0x5a, 0xcf, 0x11], [0xb8, 0x7b, 0xdf, 0xb5]]
    state = aesencrypt.mix_cols(before2)
    KAT2 = [0x75, 0x20, 0x53, 0xbb], [0xec, 0x0b, 0xc0, 0x25], [0x09, 0x63, 0xcf, 0xd0], [0x93, 0x33, 0x7c, 0xdc]
    tools.compare_2d(state, KAT2, 2)


    before3 = [[0x52, 0x85, 0xe3, 0xf6], [0xa4, 0x11, 0xcf, 0x50], [0xc8, 0x6a, 0x2f, 0x5e], [0x94, 0x28, 0xd7, 0x07]]
    state = aesencrypt.mix_cols(before3)
    KAT3 = [0x0f, 0x60, 0x6f, 0x5e], [0xd6, 0x31, 0xc0, 0xb3], [0xda, 0x38, 0x10, 0x13], [0xa9, 0xbf, 0x6b, 0x01]
    tools.compare_2d(state, KAT3, 3)


    before4 = [[0xe1, 0xe8, 0x35, 0x97], [0xfb, 0xc8, 0x6c, 0x4f], [0x96, 0xae, 0xd2, 0xfb], [0x7c, 0x9b, 0xba, 0x53]]
    state = aesencrypt.mix_cols(before4)
    KAT4 = [0x25, 0xbd, 0xb6, 0x4c], [0xd1, 0x11, 0x3a, 0x4c], [0xa9, 0xd1, 0x33, 0xc0], [0xad, 0x68, 0x8e, 0xb0]
    tools.compare_2d(state, KAT4, 4)


    before5 = [[0xa1, 0x78, 0x10, 0x4c], [0x4f, 0xe8, 0xd5, 0x63], [0x3d, 0x03, 0xa8, 0x29], [0xfe, 0xfc, 0xdf, 0x23]]
    state = aesencrypt.mix_cols(before5)
    KAT5 = [[0x4b, 0x2c, 0x33, 0x37], [0x86, 0x4a, 0x9d, 0xd2], [0x8d, 0x89, 0xf4, 0x18], [0x6d, 0x80, 0xe8, 0xd8]]
    tools.compare_2d(state, KAT5, 5)

    print(f'[END] Mix Columns Test:\r\n')

def inv_mix_cols_test():
    print(f'[START] Inv Columns Test:')

    before0 = [[0xd4, 0xe0, 0xb8, 0x1e], [0xbf, 0xb4, 0x41, 0x27], [0x5d, 0x52, 0x11, 0x98], [0x30, 0xae, 0xf1, 0xe5]]
    state = aesencrypt.mix_cols(before0)
    state = aesdecrypt.inv_mix_cols(state)
    tools.compare_2d(state, before0, 0)
    tools.debug_print_arr_2dhex(state)
    print()

    before1 = [[0x49, 0x45, 0x7f, 0x77], [0xdb, 0x39, 0x02, 0xde], [0x87, 0x53, 0xd2, 0x96], [0x3b, 0x89, 0xf1, 0x1a]]
    state = aesencrypt.mix_cols(before1)
    state = aesdecrypt.inv_mix_cols(state)
    tools.compare_2d(state, before1, 1)
    tools.debug_print_arr_2dhex(state)
    print()

    before2 = [[0xac, 0xef, 0x13, 0x45], [0xc1, 0xb5, 0x23, 0x73], [0xd6, 0x5a, 0xcf, 0x11], [0xb8, 0x7b, 0xdf, 0xb5]]
    state = aesencrypt.mix_cols(before2)
    state = aesdecrypt.inv_mix_cols(state)
    tools.compare_2d(state, before2, 2)
    tools.debug_print_arr_2dhex(state)
    print()

    before3 = [[0x52, 0x85, 0xe3, 0xf6], [0xa4, 0x11, 0xcf, 0x50], [0xc8, 0x6a, 0x2f, 0x5e], [0x94, 0x28, 0xd7, 0x07]]
    state = aesencrypt.mix_cols(before3)
    state = aesdecrypt.inv_mix_cols(state)
    tools.compare_2d(state, before3, 3)
    tools.debug_print_arr_2dhex(state)
    print()

    before4 = [[0xe1, 0xe8, 0x35, 0x97], [0xfb, 0xc8, 0x6c, 0x4f], [0x96, 0xae, 0xd2, 0xfb], [0x7c, 0x9b, 0xba, 0x53]]
    state = aesencrypt.mix_cols(before4)
    state = aesdecrypt.inv_mix_cols(state)
    tools.compare_2d(state, before4, 4)
    tools.debug_print_arr_2dhex(state)
    print()

    before5 = [[0xa1, 0x78, 0x10, 0x4c], [0x4f, 0xe8, 0xd5, 0x63], [0x3d, 0x03, 0xa8, 0x29], [0xfe, 0xfc, 0xdf, 0x23]]
    state = aesencrypt.mix_cols(before5)
    state = aesdecrypt.inv_mix_cols(state)
    tools.compare_2d(state, before5, 5)
    tools.debug_print_arr_2dhex(state)
    print()

    print(f'[END] Inv Mix Columns Test:\r\n')




def test_aes():
    key = [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c] #Test vector FIPS 197
    #key = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f]
    #state = [[0x32, 0x88, 0x31, 0xe0], [0x43, 0x5a, 0x31, 0x37], [0xf6, 0x30, 0x98, 0x07], [0xa8, 0x8d, 0xa2, 0x34]] #Test vector FIPS197
    state = [[0x00, 0x44, 0x88, 0xcc], [0x11, 0x55, 0x99, 0xdd], [0x22, 0x66, 0xaa, 0xee], [0x33, 0x77, 0xbb, 0xff]]

    aes_keys = aesencrypt.key_expansion(key)

    round_key = aesencrypt.extract_key(aes_keys[0])
    state = aesencrypt.xor_2d(state, round_key)

    for curr_round in range(1, 11, 1):

        print(f'[ENCRYPT]: round{curr_round}: Start of Round')
        tools.debug_print_arr_2dhex_1line(state)
        print()

        print(f'[ENCRYPT]: round{curr_round}: After SubBytes')
        aesencrypt.s_box_sub(state)
        tools.debug_print_arr_2dhex_1line(state)
        print()

        print(f'[ENCRYPT]: round{curr_round}: After ShiftRows')
        aesencrypt.shift_rows(state)
        tools.debug_print_arr_2dhex_1line(state)
        print()

        if curr_round != 10:
            print(f'[ENCRYPT]: round{curr_round}: After MixColumns')
            state = aesencrypt.mix_cols(state)
            tools.debug_print_arr_2dhex_1line(state)
            print()

        print(f'[ENCRYPT]: round{curr_round}: Round key Value')
        round_key = aesencrypt.extract_key(aes_keys[curr_round])
        state = aesencrypt.xor_2d(state, round_key)
        tools.debug_print_arr_2dhex_1line(round_key)
        print()

    print(f'AES Encrypt Complete')
    tools.debug_print_arr_2dhex_1line(state)
    print()

    print(f'[START] AES Decrypt')

    round_key = aesencrypt.extract_key(aes_keys[10])

    print(f'[DECRYPT] round{0}: iinput')
    tools.debug_print_arr_2dhex_1line(state)
    print()

    print(f'[DECRYPT] round{0}: ik_sch')
    tools.debug_print_arr_2dhex_1line(round_key)
    print()

    state = aesencrypt.xor_2d(state, round_key)

    for inv_curr_round in range(9,-1,-1):

        print(f'[DECRYPT] round{10 - inv_curr_round}: istart')
        tools.debug_print_arr_2dhex_1line(state)
        print()

        print(f'[DECRYPT] round{10 - inv_curr_round}: is_row')
        aesdecrypt.shift_rows_inv(state)
        tools.debug_print_arr_2dhex_1line(state)
        print()

        print(f'[DECRYPT] round{10 - inv_curr_round}: is_box')
        aesdecrypt.s_box_inv_sub(state)
        tools.debug_print_arr_2dhex_1line(state)
        print()

        round_key = aesencrypt.extract_key(aes_keys[inv_curr_round])

        print(f'[DECRYPT] round{10 - inv_curr_round}: ik_sch')
        tools.debug_print_arr_2dhex_1line(round_key)
        print()

        print(f'[DECRYPT] round{10 - inv_curr_round}: ik_add')
        state = aesdecrypt.xor_2d(state, round_key)
        tools.debug_print_arr_2dhex_1line(state)
        print()

        if inv_curr_round != 0:
            print(f'[DECRYPT] round{10 - inv_curr_round}: i_mix_cols')
            state = aesdecrypt.inv_mix_cols(state)
            tools.debug_print_arr_2dhex_1line(state)
            print()

    print(f'AES Decrypt Complete')
    tools.debug_print_arr_2dhex_1line(state)
    print()


if __name__ == '__main__':
    print("---- AES Test Entry ----\r\n")
    # unittest.main()
    mix_cols_test()
    inv_mix_cols_test()
    sub_bytes_test()
    key_expansion_test()
    inv_shift_rows_test()
    test_aes()


