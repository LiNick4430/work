import math

# Decimal to Binary 10進位轉2進位
def dec_to_bin(dec):
    bin = []
    while dec / 2 > 0:
        bin.append(str(dec % 2))
        dec = dec // 2
    bin.reverse()
    return ''.join(bin)

    # Binary to Decimal 2進位轉10進位
def bin_to_dec(bin_str):
    bin = [int(n) for n in bin_str ]
    dec = [bin[-i - 1] * math.pow(2, i) for i in range(len(bin))]
    return int(sum(dec))

def SubnetMask_bin(ip5):
    ran = ip5%8
    bin = ""
    for i in range(8):
        if i < ran:
            bin += "1"
        else:
            bin += "0"
    return bin

def Network_id_bin(ip,sm):
    bin = ""
    for i in range(8):
        if ip[i] == sm[i]:
            bin += ip[i]
        else:
            bin += "0"
    return bin
    
def Broadcast_id_bin(ni,ip5):
    ran = ip5%8
    bin = ""
    for i in range(8):
        if i < ran:
            bin += ni[i]
        else:
            bin += "1"
    return bin

def bin2dec(ip,ip5):
    ip = str(dec_to_bin(ip)).zfill(8)
    sm_bin = SubnetMask_bin(ip5)
    sm = bin_to_dec(sm_bin)

    ni_bin = Network_id_bin(ip , sm_bin)
    ni = bin_to_dec(ni_bin)

    bi_bin = Broadcast_id_bin(ni_bin , ip5)
    bi = bin_to_dec(bi_bin)

    return sm , ni ,  bi