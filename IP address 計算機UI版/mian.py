
from tkinter import *
import math

from tra import *

_bgcolor = '#d9d9d9'  # X11 color: 'gray85'
_fgcolor = '#000000'  # X11 color: 'black'
_compcolor = 'gray40' # X11 color: #666666
_ana1color = '#c3c3c3' # Closest X11 color: 'gray76'
_ana2color = 'beige' # X11 color: #f5f5dc

#UI介面
class MAIN:
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name
    
    def set_init_window(self):
        self.init_window_name.geometry("450x300")            # 視窗大小
        self.init_window_name.title("IP address 計算機")      # 標題名
        self.init_window_name.resizable(False, False)         # 禁止自由更遍大小
        self.init_window_name.configure(background="#d9d9d9") # 背景顏色

        #輸入位置
        self.ip1 = StringVar()
        self.ip1e = Entry(self.init_window_name, justify='right',textvariable=self.ip1)
        self.ip1e.place(relx=0.044, rely=0.133, height=20, relwidth=0.156)
        self.ip2 = StringVar()
        self.ip2e = Entry(self.init_window_name, justify='right',textvariable=self.ip2)
        self.ip2e.place(relx=0.244, rely=0.133, height=20, relwidth=0.156)
        self.ip3 = StringVar()
        self.ip3e = Entry(self.init_window_name, justify='right',textvariable=self.ip3)
        self.ip3e.place(relx=0.444, rely=0.133, height=20, relwidth=0.156)
        self.ip4 = StringVar()
        self.ip4e = Entry(self.init_window_name, justify='right',textvariable=self.ip4)
        self.ip4e.place(relx=0.644, rely=0.133, height=20, relwidth=0.156)
        self.ip5 = StringVar()
        self.ip5e = Entry(self.init_window_name, justify='right',textvariable=self.ip5)
        self.ip5e.place(relx=0.844, rely=0.133, height=20, relwidth=0.089)

        # 按鈕
        self.Enter = Button(self.init_window_name, text='Enter', command=self.transform)
        self.Enter.place(relx=0.844, rely=0.267, height=150, width=55)
        self.Enter.configure(activebackground="beige")
        self.Enter.configure(activeforeground="black")
        self.Enter.configure(background="#d9d9d9")
        self.Enter.configure(disabledforeground="#a3a3a3")
        self.Enter.configure(foreground="#000000")
        self.Enter.configure(highlightbackground="#d9d9d9")
        self.Enter.configure(highlightcolor="black")

        self.Enter = Button(self.init_window_name, text='clear', command=self.clear)
        self.Enter.place(relx=0.844, rely=0.767, height=50, width=55)
        self.Enter.configure(activebackground="beige")
        self.Enter.configure(activeforeground="black")
        self.Enter.configure(background="#d9d9d9")
        self.Enter.configure(disabledforeground="#a3a3a3")
        self.Enter.configure(foreground="#000000")
        self.Enter.configure(highlightbackground="#d9d9d9")
        self.Enter.configure(highlightcolor="black")

        # 輸出位置
        self.outside = Text(self.init_window_name)
        self.outside.place(relx=0.044, rely=0.267, relheight=0.667, relwidth=0.756)
        self.outside.configure(state="disabled") #禁止修改

        # 顯示內容
        self.Label1 = Label(self.init_window_name, background="#d9d9d9", text='請輸入IPv4 address')
        self.Label1.place(relx=0.044, rely=0.033, height=20, width=400)
        self.Label2 = Label(self.init_window_name, anchor='w', background="#d9d9d9", text='.')
        self.Label2.place(relx=0.2, rely=0.133, height=20, width=20)
        self.Label3 = Label(self.init_window_name, anchor='w', background="#d9d9d9", text='.')
        self.Label3.place(relx=0.4, rely=0.133, height=20, width=20)
        self.Label4 = Label(self.init_window_name, anchor='w', background="#d9d9d9", text='.')
        self.Label4.place(relx=0.6, rely=0.133, height=20, width=20)
        self.Label5 = Label(self.init_window_name, anchor='w', background="#d9d9d9",  text='/')
        self.Label5.place(relx=0.8, rely=0.133, height=20, width=20)

    #輸出內容
    def output_text(self,text):
        # 清光輸出內容
        self.outside.configure(state="normal") #可以修改
        self.outside.delete(1.0, "end") #清空內容
        
        #顯示輸出內容
        self.outside.insert(1.2,text)
        self.outside.configure(state="disabled") #禁止修改

    #IP網址換算
    def transform(self):
        try:    
            ip1 = int(self.ip1.get())
            ip2 = int(self.ip2.get())
            ip3 = int(self.ip3.get())
            ip4 = int(self.ip4.get())
            ip5 = int(self.ip5.get())

            if 0 <= ip1 <= 255 and 0 <= ip2 <= 255 and 0 <= ip3 <= 255 and 0 <= ip4 <= 255 and 0<= ip5 <= 32:      
                if ip5 == 32:
                    ip_adderss = "IP address： {}.{}.{}.{}".format(ip1,ip2,ip3,ip4)
                    network_id = "Network_id： {}.{}.{}.{}".format(ip1,ip2,ip3,ip4)
                    subnetmask = "SubnetMask： 255.255.255.255"
                    broadcast = "Broadcast_id：None"
                elif ip5 >= 24:
                    dec_ip = bin2dec(ip4,ip5)
                    ip_adderss = "IP address： {}.{}.{}.{}".format(ip1,ip2,ip3,ip4)
                    network_id = "Network_id： {}.{}.{}.{}".format(ip1,ip2,ip3,dec_ip[1])
                    subnetmask = "SubnetMask： 255.255.255.{}".format(dec_ip[0])
                    broadcast = "Broadcast_id：{}.{}.{}.{}".format(ip1,ip2,ip3,dec_ip[2])
                elif ip5 >= 16:
                    dec_ip = bin2dec(ip3,ip5)
                    ip_adderss = "IP address： {}.{}.{}.{}".format(ip1,ip2,ip3,ip4)
                    network_id = "Network_id： {}.{}.{}.0".format(ip1,ip2,dec_ip[1])
                    subnetmask = "SubnetMask： 255.255.{}.0".format(dec_ip[0])
                    broadcast = "Broadcast_id：{}.{}.{}.255".format(ip1,ip2,dec_ip[2])
                elif ip5 >= 8:
                    dec_ip = bin2dec(ip2,ip5)
                    ip_adderss = "IP address： {}.{}.{}.{}".format(ip1,ip2,ip3,ip4)  
                    network_id = "Network_id = {}.{}.0.0".format(ip1,dec_ip[1])
                    subnetmask = "SubnetMask： 255.{}.0.0".format(dec_ip[0])
                    broadcast = "Broadcast_id：{}.{}.255.255".format(ip1,dec_ip[2])
                else:
                    dec_ip = bin2dec(ip1,ip5)
                    ip_adderss = "IP address： {}.{}.{}.{}".format(ip1,ip2,ip3,ip4)
                    network_id = "Network_id = {}.0.0.0".format(dec_ip[1])
                    subnetmask = "SubnetMask： {}.0.0.0".format(dec_ip[0])
                    broadcast = "Broadcast_id：{}.255.255.255".format(dec_ip[2])
                
                out = ip_adderss+ "\n" + network_id + "\n" + subnetmask + "\n" + broadcast
            else:
                out = "輸入錯誤，請輸入0~255以及0~32的整數"
        except:
            out = "輸入錯誤"
        
        self.output_text(out)
    
    
    def clear(self):
        # 清空輸入欄
        #self.ip1 = set("")
        self.ip1e.delete(0,'end')
        #self.ip2 = set("")
        self.ip2e.delete(0,'end')
        #self.ip3 = set("")
        self.ip3e.delete(0,'end')
        #self.ip4 = set("")
        self.ip4e.delete(0,'end')
        #self.ip5 = set("")
        self.ip5e.delete(0,'end')
        # 清光輸出內容
        self.outside.configure(state="normal") #可以修改
        self.outside.delete(1.0, "end") #清空內容
        self.outside.configure(state="disabled") #禁止修改

        
   
def main():
    root = Tk()
    root.protocol( 'WM_DELETE_WINDOW' , root.destroy)

    win = MAIN(root)
    win.set_init_window()

    root.mainloop()

if __name__ == '__main__':
    main()