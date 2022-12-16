################################
### import 套件
import re
import math
import copy

################################
### 各種功能套件

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

# 分割輸入資訊
def Split_IPv4(ip_add_sm):
  x = ip_add_sm.split(".",3)
  y = x[3].split("/",1)
  z = x[:3] + y
  return z[:4] , z[4]

def Split(ip_add_sm):
  x = ip_add_sm.split(".",3)
  return x

# 把IP位置轉成二進位
def IP_address_to_bin(list4):
  list4_dec = [str(dec_to_bin(int(i))).zfill(8) for i in list4] # 取出來 變成2進位 補0
  list32 =[int(j) for i in list4_dec for j in i]
  return list32

# 生成2進位SubnetMask
def SubnetMask_bin(num):
  bin = []
  for i in range(32):
    if i < int(num):
      bin.append(1)
    else:
      bin.append(0)
  return bin

# 生成2進位Network_id
def Network_id_bin(list32_1,list32_2):
  bin = []
  for i in range(32):
    if list32_1[i] == list32_2[i]:
      bin.append(list32_1[i])
    else:
      bin.append(0)
  return bin

# 生成2進位Broadcast_id
def Broadcast_id_bin(network_id_bin,num):
  bin = []

  num = 32 - int(num)
  numlist =[1 for i in range(num)]

  bin = network_id_bin.copy()
  bin[-num:] = numlist
  return bin

# 字元遮罩計算
def Wildcard_Mask(list32a ,list32b):
  for i in range(32):
    if list32b[i] == 1:
      list32a[i] = "x"  
  return list32a

# Wildcard_Mask計算全部可能性
def Xto10(list32):
  list32 = [list32]
  num = 2**(list32[0].count("x")) #計算總數
  for i in range(num):
    while list32[i].count("x") != 0: #計算"x"的數量 當不為0時   
        b = list32[i].index("x") #尋找第一個"x"位置
        c = copy.copy(list32[i]) #複製
        list32.append(c) #放入最後
        list32[i][b] = "1" # 替換成1
        list32[-1][b] = "0" # 替換成0
  list32.sort() #排序
  return list32

#比較各個list32，生成WildcardMask
def GetWildcardMask(all_list32): 
  total = [0 for i in range(32)]

  for i in range(32):            # 比較list中第i個數字
    for j in range(len(all_list32)):       # 看共輸入幾個ip
      if j+1 == len(all_list32):        
        break
      elif all_list32[0][i] != all_list32[j+1][i]:   # 比較 第0個 和其他list中第i個數字
        total[i] = '*'
        break
  return total

# 將2進位bit 轉換成可視化的10進位
def tra_bin_to_dec(list32): 
  tostr = ""
  for i in list32: #合併成單一字串
    tostr +=  str(i)

  tostrdec = [tostr[i:i+8] for i in range(0,32,8)] # 以每8個分割成陣列
  dec = [bin_to_dec(i) for i in tostrdec] # 2進位轉成10進位
  dec2str = [str(i) for i in dec] # int轉換成str
  result = ".".join(dec2str) # 印出
  return result

#顯示範圍
def Show_ran(ran):
  show = input("\n是否顯示範圍內的數值，輸入1顯示，1以外不顯示：")
  if show == "1":
    if len(ran) > 1025:
      print("範圍過多，請輸入要前後各顯示幾個 MAX = 512 \n大於512或其他數值，以512計算")
      maxnum = input("請輸入：")
      try:
        if int(maxnum) > 512:
          maxnum = 512
        else:
          maxnum = int(maxnum)      
      except:
        maxnum = 512

      print("\nACL範圍有：")
      if maxnum%4 == 0:
        for i in range(0,maxnum,4):
          print("{}\t\t{}\t\t{}\t\t{}".format(ran[i],ran[i+1],ran[i+2],ran[i+3]))
        print("\n\t\t\t\t\t~~略過~~\n")
        for i in range(len(ran)-maxnum,len(ran),4):
          print("{}\t\t{}\t\t{}\t\t{}".format(ran[i],ran[i+1],ran[i+2],ran[i+3]))
        print("\n")
      elif maxnum%4 == 1:
        for i in range(0,maxnum-1,4):
          print("{}\t\t{}\t\t{}\t\t{}".format(ran[i],ran[i+1],ran[i+2],ran[i+3]))
        print("{}".format(ran[maxnum-1]))
        print("\n\t\t\t\t\t~~略過~~\n")
        for i in range(len(ran)-maxnum,len(ran)-1,4):
          print("{}\t\t{}\t\t{}\t\t{}".format(ran[i],ran[i+1],ran[i+2],ran[i+3]))
        print("{}".format(ran[len(ran)-1]))
        print("\n")
      elif maxnum%4 == 2:
        for i in range(0,maxnum-2,4):
          print("{}\t\t{}\t\t{}\t\t{}".format(ran[i],ran[i+1],ran[i+2],ran[i+3]))
        print("{}\t\t{}".format(ran[maxnum-2],ran[maxnum-1]))
        print("\n\t\t\t\t\t~~略過~~\n")
        for i in range(len(ran)-maxnum,len(ran)-2,4):
          print("{}\t\t{}\t\t{}\t\t{}".format(ran[i],ran[i+1],ran[i+2],ran[i+3]))
        print("{}\t\t{}".format(ran[len(ran)-2],ran[len(ran)-1]))
        print("\n")
      else:
        for i in range(0,maxnum-3,4):
          print("{}\t\t{}\t\t{}\t\t{}".format(ran[i],ran[i+1],ran[i+2],ran[i+3]))
        print("{}\t\t{}\t\t{}".format(ran[maxnum-3],ran[maxnum-2],ran[maxnum-1]))
        print("\n\t\t\t\t\t~~略過~~\n")
        for i in range(len(ran)-maxnum,len(ran)-3,4):
          print("{}\t\t{}\t\t{}\t\t{}".format(ran[i],ran[i+1],ran[i+2],ran[i+3]))
        print("{}\t\t{}\t\t{}".format(ran[len(ran)-3],ran[len(ran)-2],ran[len(ran)-1]))
        print("\n")
    
    elif len(ran) == 1:
      print("\nACL範圍有：")
      print("{}".format(ran[0]))
      print("\n")
    
    elif len(ran) == 2:
      print("\nACL範圍有：")
      print("{}\t\t{}".format(ran[0],ran[1]))
      print("\n")
    
    else :
      print("\nACL範圍有：")
      for i in range(0,len(ran),4):
        print("{}\t\t{}\t\t{}\t\t{}".format(ran[i],ran[i+1],ran[i+2],ran[i+3]))
      print("\n")

#輸入程序
def Input_Ipv4():
  running_ipv4 = True
  print("IP位置範例：192.168.100.1/24")
  print("前四位為0~255的整數，第五位為0~32的整數")
  while running_ipv4:
    ip = input("請輸入IP位置：")
    try:
      spilted_ip = Split_IPv4(ip)    
      if len(spilted_ip[0]) != 4:
        print("輸入錯誤，/前，請輸入4個數值用.隔開\n")
      elif type(int(spilted_ip[1])) != int :
        print("輸入錯誤，/後，請輸入1個數值\n")
      elif 0 <= int(spilted_ip[0][0]) <= 255 and \
            0 <= int(spilted_ip[0][1]) <= 255 and \
            0 <= int(spilted_ip[0][2]) <= 255 and \
            0 <= int(spilted_ip[0][3]) <= 255 and \
            0 <= int(spilted_ip[1]) <= 32:
        running_ipv4 = False
      else:
          print("輸入錯誤，前四位為0~255的整數，第五位為0~32的整數\n")
    except:
      print("格式輸入錯誤\n")

  return spilted_ip

def Input_one2ran():
  running_ip = True
  running_wm = True
  print("請輸入IP address，範例：192.168.100.1")
  while running_ip:    
    ip = input("IP address：")
    try:
      spilted_ip = Split(ip)    
      if len(spilted_ip) != 4:
        print("輸入錯誤，請輸入4個數值用.隔開\n")
      elif 0 <= int(spilted_ip[0]) <= 255 and \
            0 <= int(spilted_ip[1]) <= 255 and \
            0 <= int(spilted_ip[2]) <= 255 and \
            0 <= int(spilted_ip[3]) <= 255 :
        running_ip = False
      else:
          print("輸入錯誤，數值請輸入0~255整數\n")
    except:
      print("格式輸入錯誤\n")
  
  print("請輸入WildcardMask，範例：0.0.0.255")
  while running_wm:
    wm = input("WildcardMask：")
    try:
      spilted_wm = Split(wm)    
      if len(spilted_wm) != 4:
        print("輸入錯誤，請輸入4個數值用.隔開\n")
      elif 0 <= int(spilted_wm[0]) <= 255 and \
            0 <= int(spilted_wm[1]) <= 255 and \
            0 <= int(spilted_wm[2]) <= 255 and \
            0 <= int(spilted_wm[3]) <= 255 :
        running_wm = False
      else:
          print("輸入錯誤，數值請輸入0~255整數\n")
    except:
      print("格式輸入錯誤\n")
  
  return spilted_ip , spilted_wm

def Input_multiple2ran(): 
  running_mul = True
  show_total = []
  total = []
  number = 1
  print("請輸入IP address，範例：192.168.100.1")
  while running_mul :
    print("請輸入第{}個IP address，當輸入* ，開始計算".format(number))
    newip = input("IP address： ")

    if newip == "*":
      if total == []:
        print("請至少輸入1個IP address\n")
        continue
      else:
        break
    
    try:
      spilted_ip = Split(newip)
      if len(spilted_ip) != 4:
        print("輸入錯誤，請輸入4個數值用.隔開\n")
      elif 0 <= int(spilted_ip[0]) <= 255 and \
            0 <= int(spilted_ip[1]) <= 255 and \
            0 <= int(spilted_ip[2]) <= 255 and \
            0 <= int(spilted_ip[3]) <= 255:
        show_total.append(newip)
        total.append(spilted_ip)

        print("\n已經輸入的IP address位置有{}個，有：".format(len(show_total)))
        for i in show_total:
          print(i)
        print("")
        number += 1
      else:
        print("輸入錯誤，數值請輸入0~255整數\n")
    except:
      print("格式輸入錯誤\n")

  return total

#循環執行程序
def Loop(num):
  running_inside = True
  while running_inside:
    if num == "1":
      Main_Ipv4()
    elif num == "2":
      Main_one2ran()
    elif num == "3":
      Main_multiple2ran()
    print("\n繼續使用，請輸入 1 \
          \n離開功能，請輸入 不是1 的任意值")
    inputnum_inside = input("輸入位置：")
    if inputnum_inside != "1":
      running_inside = False
    print("\n")

################################
# 3種功能主程序
def Main_Ipv4():
  try:
    ip = Input_Ipv4()

    ip_bin = IP_address_to_bin(ip[0])  #ipbin 2進位IP address
    sm_bin = SubnetMask_bin(ip[1])   #smbin 2進位SubnetMask
    nw_bin = Network_id_bin(ip_bin,sm_bin) #nwbin 2進位Network_id
    bc_bin = Broadcast_id_bin(nw_bin,ip[1]) #bdbin 2進位Broadcast_id


    ip_dec = tra_bin_to_dec(ip_bin)
    sm_dec = tra_bin_to_dec(sm_bin)
    nw_dec = tra_bin_to_dec(nw_bin)
    bc_dec = tra_bin_to_dec(bc_bin)

    print("\nIP address  ：",ip_dec)
    print("SubnetMask  ：",sm_dec)
    print("Network_id  ：",nw_dec)
    print("Broadcast_id：",bc_dec,"\n")
  
  except Exception as ex:
    print(ex)

def Main_one2ran():

  ip , wm = Input_one2ran()

  try:
    # 分割並轉換成二進位
    ip_bin = IP_address_to_bin(ip) 
    wm_bin = IP_address_to_bin(wm)

    # 互相比對後 產生所有範圍
    ran_bin = Wildcard_Mask(ip_bin, wm_bin) 
    ran_all_bin = Xto10(ran_bin)
    
    # 範圍內的二進位轉換成十進位
    ran_all_dec = []
    for i in ran_all_bin:
      ran_all_dec.append(tra_bin_to_dec(i))

    print("\nACL範圍內有{}個IP address".format(len(ran_all_dec)))
    
    Show_ran(ran_all_dec)
  
  except Exception as ex:
    print(ex)

def Main_multiple2ran():
    all_ip = Input_multiple2ran()
    print("\n輸入結束，開始計算\n")

    try:
        all_ip_bin = [IP_address_to_bin(i) for i in all_ip] 

        wm_bin_no1 = GetWildcardMask(all_ip_bin) # 只有 0 和 "*" 的WildcardMask list

        wm_bin = [ 1 if i == '*' else i for i in wm_bin_no1] # 有 0 和 1 的WildcardMask

        wm_dec = tra_bin_to_dec(wm_bin) # 把WildcardMask 2進位轉成10進位
        
        ip_add_bin = IP_address_to_bin(all_ip[0]) #取出ip 並轉換成2進位

        all_wm_x = Wildcard_Mask(ip_add_bin, wm_bin) #互相比對
        all_wm_bin = Xto10(all_wm_x) #產生所有範圍

        # 範圍內的二進位轉換成十進位
        all_wm_dec = [tra_bin_to_dec(i) for i in all_wm_bin]

        print("生成結果：")
        print("IP address：" , all_wm_dec[0])
        print("WildcardMask：" , wm_dec)
        print("\n範圍內有{}個IP address".format(len(all_wm_dec)))

        Show_ran(all_wm_dec)

    except Exception as ex:
      print(ex)

################################
# 總主程序
def main():
  running = True
  while running:
    print("數字\t說明\n")
    print("1\t輸入IPv4 與 子網路遮罩，計算網域ID與廣播ID")
    print("2\t輸入IPv4 與 WildcardMask，計算ACL範圍")
    print("3\t輸入數個IPv4，計算WildcardMask與ACL範圍")
    print("0\t結束程式")

    inputnum = input("\n請輸入數字選擇功能：")
    print("\n")
    if inputnum == "1":
      Loop(inputnum)
    elif inputnum == "2":
      Loop(inputnum)
    elif inputnum == "3":
      Loop(inputnum)
    elif inputnum == "0":
      running = False
    else:
      print("請輸入 0 1 2 3 任一數字\n")

if __name__ == "__main__":
    main() 