import os


def ename():
    dirlist = os.listdir('file_to_encrypt')
    if dirlist != []:
        filename = 'file_to_encrypt/'+(dirlist[0])
    return filename

def dname():
    dirlist = os.listdir('file_to_decrypt')
    if dirlist != []:
        filename = 'file_to_decrypt/'+(dirlist[0])
    return filename
    
def openb(filename):
    temp = []
    with open(filename, 'rb') as f:
        byte = f.read(1)
        temp.append(byte)
        while byte:
            byte = f.read(1)
            temp.append(byte)
    intlist = [ord(i) for i in temp[:-1]]
    return intlist

def ewrite(cypher):
    text = cypher
    filename = readoptions()
    filename = filename[2]
    with open('result/'+filename+'.rc4', 'wb') as f:
        for i in text:
            f.write(i)

def dwrite(plain,extension):
    text = plain
    filename = readoptions()
    filename = filename[2]
    with open('result/'+filename+'.'+extension, 'wb') as f:
        for i in text:
            f.write(i)

    
    
def readoptions():
    with open('settings.txt','r',encoding = 'utf-8') as f:
        temp = f.read()
    options = temp.split('\n')   
    options = [i.split('=')[1].strip() for i in options]
    options[1] = [ord(i) for i in options[1]]
    options[0] = int(options[0])
    if options[2] == '':
        options[2] = 'result'
    return options

def keystreamgenerator(key):                 
    k = []
    s = [i for i in range(256)]                 
    for i in range(256):                        
        k.append(key[i % len(key)])
    j = 0
    for i in range(256):
        j = (j + s[i] + k[i]) % 256
        swipe = s[i]
        s[i] = s[j]
        s[j] = swipe
        
    i = 0
    j = 0
    while True:
        i = (i+1)%256
        j = (j+ s[i]) %256
        swipe = s[j]
        s[j] = s[i]
        s[i] = swipe
        a = s[(s[i]+s[j])%256]
        yield a

def encrypt():
    option = readoptions()
    key = option[1]
    stream = keystreamgenerator(key)
    plain = openb(ename())
    
    
    n = option[0]
    
    for i in range(n):
        skip = 0^next(stream)
    
    cypher = []
    for i in plain:
        temp = i^next(stream)
        cypher.append(temp)
    cypher = [i.to_bytes(1,'big') for i in cypher]
    return cypher

def decrypt():
    option = readoptions()                  
    key = option[1]
    stream = keystreamgenerator(key)
    cypher = openb(dname())
    
    
    n = option[0]
    
    for i in range(n):
        skip = 0^next(stream)
    
    plain = []
    for i in cypher:
        temp = i^next(stream)
        plain.append(temp)
    plain = [i.to_bytes(1,'big') for i in plain]
    return plain
    
print('Check "settings" file fist!')
choose = input('Encrypt file in "file_to_encrypt" folder: [E]\nDecrypt file in "file_to_decrypt" folder: [D]\n')
if choose == 'd' or choose == 'D':
    extension = input('Enter file extension (excluding the dot): ')
    plain = decrypt()
    dwrite(plain,extension)
elif choose == 'e' or choose == 'E':
    cypher = encrypt()
    ewrite(cypher)
