# Python script for bruteforcing a XOR Encryption key on a json encrypted file.

## Testing  the xor encryption-decryption algorithm

First, we can test our xor encryption-decryption algorithm using the key **mykey** on *output.txt* and check if the output will be the plain text from *input.txt*.

Change the main function from a script of your choice with the following:
```
f = open(output.txt, "r")
str = f.read()
f.close()
key = "mykey"
xor_key = adaptKeyLength(key, len(str))
out_str = xor_EncryptDecrypt(str, xor_key)
print(out_str)
```
Then just run the python script.
```
python3 bruteforce_xor_threaded.py
```

## Running the actual scripts

Example of using the script:
```
python3 bruteforce_xor_threaded.py scr.json 5
```

The keys are generated using letters from [a-z] and [A-Z]. The length of the key is only one number. If you want to check for multiple lengths you have to run the script for each length of the key.

> **Disclaimer:** The scripts are very slow (even the threaded one, more than 6 hours for 5 letter keys).

