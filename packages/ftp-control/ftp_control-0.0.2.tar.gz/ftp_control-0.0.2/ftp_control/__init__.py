from ftplib import FTP_TLS
import os
import time
import winsound
import ctypes

def main(ftp_server,kul,psv,dirr,dur):
    
    bir=0
    iki=0
    ctypes.windll.kernel32.SetConsoleTitleW("Sunucuya bağlandı !! ")
    while True:
        try:
            ftps = FTP_TLS(ftp_server)
            ftps.login(kul,psv)
            ftps.prot_p() 
            ftps.cwd(dirr)
            ftps.retrlines('LIST')
            data=[]
            ftps.dir(data.append)
            bir=len(data)
            print("FİLE SAYISI : "+str(bir))
        
            if bir>iki:
                iki=bir
                winsound.Beep(2500, 2000)
                print("----   A NEW FİLE UPLOAD FTP SERVER   ----")
            elif bir<iki:
                print("none")
          
            time.sleep(dur)
            os.system("cls")
        except:
            print("BİR HATA İLE KARŞI KARŞIYAYIZ. LÜTFEN ADAM AKILLI VERİ GİR... !!!")
            break
        
"""EMİRCAN KELEŞ""" 
