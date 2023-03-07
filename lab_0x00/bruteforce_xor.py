import sys
import json

def adaptKeyLength(simpleKey, strLength):
    xorKey = ""
    while(len(xorKey) < strLength):
        xorKey = xorKey + simpleKey
    diff = len(xorKey) - strLength
    if diff != 0: 
        xorKey = xorKey[:-diff]
    return xorKey

def xor_EncryptDecrypt(inpString, xorKey):
    outStr = ""
    for i in range(len(inpString)):
        c = chr(ord(inpString[i]) ^ ord(xorKey[i]))
        outStr = outStr + c
    return outStr;

def get_word(word_chr):
    wrd = ""
    for i in range(len(word_chr)):
        wrd = wrd + word_chr[i]
    return wrd

def xor_encr_decr_char_list(word_chrs, enc_str):
    word = get_word(word_chrs)
    xor_key = adaptKeyLength(word, len(enc_str))
    out_str = xor_EncryptDecrypt(enc_str, xor_key)
    return out_str

def check_resulted_string(str):
    retval = True
    try:
        x = json.loads(str)
    except:
        retval = False
    return retval

def bruteforce_xorkey(encString, length, ascii_chars):
    bf_chars_list = []
    for i in range(len(ascii_chars)):
        for j in range(ascii_chars[i][0], ascii_chars[i][1]+1):
            bf_chars_list.append(j)

    i = int(length)
    word_chars = [chr(bf_chars_list[0])]*i
    word_chars_cnt = [0]*i
    final_chars = [chr(bf_chars_list[len(bf_chars_list)-1])]*i
    validators = [0]*i
    validators[i-1] = 1

    outString = xor_encr_decr_char_list(word_chars, encString)
    if(check_resulted_string(outString)):
        print(word_chars)
        quit()
    while word_chars != final_chars:
        j = i - 1
        while j != -1:
            if validators[j] == 1:
                if word_chars_cnt[j] == (len(bf_chars_list)-1):
                    word_chars_cnt[j] = 0
                    word_chars[j] = chr(bf_chars_list[word_chars_cnt[j]])
                    validators[j-1] = 1
                else:
                    word_chars_cnt[j] = word_chars_cnt[j] + 1
                    word_chars[j] = chr(bf_chars_list[word_chars_cnt[j]])
                if j != i-1:
                    validators[j] = 0
            j = j - 1
        outString = xor_encr_decr_char_list(word_chars, encString)
        if(check_resulted_string(outString)):
            print(word_chars)
            quit()


def main():
    f = open(sys.argv[1], "r")
    str = f.read()
    f.close()
    bruteforce_xorkey(str, sys.argv[2], [[65,90],[97,122]])

main()
