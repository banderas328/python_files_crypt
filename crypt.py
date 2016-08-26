import os, random, struct
from Crypto.Cipher import AES

def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    if not out_filename:
        out_filename = in_filename + '.enc'

    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))
def decrypt_file(key, in_filename, out_filename=None, chunksize=24*1024):
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(origsize)


key  = raw_input("Insert password : ")
key2 = raw_input("Repeat password : ")
if key != key2:
    print 'password must be equal'
    exit()

use_salt = raw_input("use salt file ? y/n :")
if use_salt == "y":
    salt_file_name = raw_input("enter salt file name:")
    salt_number = raw_input("enter salt number : ")
    salt_number = int(salt_number)
    if salt_number < 1:
        print "salt number cant be less than 1"
    i = 0
    salt_number = salt_number - 1

    with open(salt_file_name) as f:
        for line in f:
            if salt_number == i:
                print line
                salt_code = line
                break
            i = i + 1

if len(key) < 16:
    print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    print "!!!!!!!Bad password, can be hacked!!!!!!!!"
    print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    while len(key) < 16:
        key = key + "1"
elif len(key) > 16:
    print "Bad password, to long"
    exit()
if use_salt == "y":
    key = key + salt_code
key = key.strip()
command = raw_input("instert command encrypt/decrypt : ");

if command == "encrypt":
    file_old = raw_input("insert file name : ")
    file_new  = raw_input("insert new file name : ")

    encrypt_file(key, file_old, file_new, 32)
    print "file encrypted"

elif command == "decrypt":
    file_old = raw_input("insert file name : ")
    file_new = raw_input("insert new file name : ")
    decrypt_file(key, file_old, file_new, 32)
    print "file decrypted"
else:
    print "unknown command"

