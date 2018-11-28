# Protype functions to take an S-GUIDS and 
#  extract the two components; The 40 bits of datetime data as GMT and 
#  88 bits of random data as a HEX string
# Charles Kaminski, 2018

from time import strftime, gmtime
alphabet = b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def b58decode_to_int(v):
    v = v.encode('ascii')
    decimal = 0
    for char in v:
        decimal = decimal * 58 + alphabet.index(char)
    return decimal

def b58encode_from_int(i):
    string = b""
    while i:
        i, idx = divmod(i, 58)
        string = alphabet[idx:idx+1] + string
    return string

def get_gmt_from_sguid(i):
    # i = int(hex_string, 16)
    
    # Shift right to leave only the time data
    i = i >> 88
    
    # 40 bit clock resets every 35 years.  Add back that time.
    i = i + 1099511627776
    s, ms = divmod(i, 1000)
    
    return '{}.{:03d}'.format(strftime('%Y-%m-%d %H:%M:%S', gmtime(s)), ms)

def get_rand_as_hex_from_sguid(i):
    # x = int(hex_string, 16)

    # Use a mask to get rid of the time component
    
    # int(('0' * 40) +('1' * 88), 2)
    z = 309485009821345068724781055
    rand = i & z
    
    return hex(rand)[2:-1].zfill(21)


sgid = 'DgqEUGAFoqzwVk9XE4fkeF'
i = b58decode_to_int(sgid)

print "SGUID: " + sgid
print "SGUID as int: " + str(i)
print "40 Bit DateTime component in GMT: " + get_gmt_from_sguid(i) + " GMT"
print "88 Bit Random component as Hex String: " + get_rand_as_hex_from_sguid(i)
