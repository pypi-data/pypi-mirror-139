# Ash-file-Encryptor/Decryptor

Image and File encryptor/decryptor with Python


## Installation  

> Works perfectly on Windows 10 and Ubuntu 21.10
 
You can use this `pip3 install -U PyCryptodome` for install pycrypto


## Flags

**`e`** Encryption Mode

**`d`** Decryption Mode

**`-p`** Password

**`-f`** FileName


## Usage

**Encryption**

`ash-encrypt e -p 123321 -f picture.png`

`ash-encrypt e -p 123321 -f file.txt`


> it will encrypt picture.png to picture.ash  with  **123321**  password

> also it will encrypt file.txt to file.ash  with  **123321**  password


**Decryption**

`ash-encrypt d -p 123321 -f picture.ash`

`ash-encrypt d -p 123321 -f file.ash`

> it will decrypt picture.ash to picture.png with  **123321**  password

> also  it will decrypt file.ash to file.txt with  **123321**  password



