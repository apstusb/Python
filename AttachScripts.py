# $language = "Python"
# $interface = "1.0"

crt.Screen.Synchronous = True

crt.Screen.IgnoreCase = True

def main():
    crt.Screen.Clear()
    #Dispaly SecureCRT's version
    crt.Dialog.MessageBox("SecureCRT's version is: " + crt.Version)  
    crt.Dialog.MessageBox( "<NB-IOT> AUTOTEST")
    crt.Screen.Send("<NB-IOT> AUTOTEST\r\n")
    crt.Screen.Send("at+ves?\r\n")
    crt.Screen.WaitForString("OK", 30)
    crt.Sleep(1000)	  #OnlyWaitTime1sec
    crt.Screen.Send("at+scfg=stat,1\r\n")
    crt.Sleep(500)
    
    crt.Screen.Send("at+cimi\r\n")
    crt.Screen.WaitForString("OK", 30)
    crt.Sleep(1000)
    crt.Screen.Send("\r\nat+sysinfo?\r\n")
    if (crt.Screen.WaitForString("+SYSINFO:2,2,0,17,1,,25", 500)):
        crt.Screen.Send('\r\nAT+CGDCONT=1,"IP",,,0,0\r\n')
        crt.Screen.WaitForString("OK", 500)
        crt.Sleep(50)          
        crt.Screen.Send("\r\nAT+CGACT=1,1\r\n")
        crt.Screen.WaitForString("OK", 500)
    else:
        crt.Screen.Send("\r\nNO SIGNAL!\r\n")
    crt.Screen.WaitForString("OK", 500)
    crt.Screen.WaitForString("+CGEV: EPS PDN ACT 1", 500)
    crt.Sleep(500)
    
    for i in range(20):
        crt.Screen.Send('at+netcards=1\r\n')
        crt.Screen.WaitForString("OK", 30)
        crt.Screen.Send("at+cgpaddr=1\r\n")
        crt.Screen.WaitForString("OK", 30)
        crt.Sleep(500)
        crt.Screen.Send('at+netcards=0\r\n')
        crt.Screen.WaitForString("OK", 30)
        crt.Screen.Send("at+cgpaddr=1\r\n")
        crt.Screen.WaitForString("OK", 30)
    
    crt.Sleep(100000)
    crt.Screen.Send("AT+CGACT=0,1\r\n")
    crt.Screen.WaitForString("+CGEV: EPS PDN DEACT 1", 60)
main()
