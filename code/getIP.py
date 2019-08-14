def getIP():
        '''
        PURPOSE:
        get the IP address of a Raspberry Pi
        attempt to connect to a known IP address

        IMPORTS:
        import socket
        '''
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
                #s.connect(('172.20.10.9',1))   #iphone hotspot
                s.connect(('192.168.86.29',1))  #LA lab
                s.connect(('192.168.1.9',1))    #PS lab

                IP = s.getsockname()[0]
        except:
                IP = '127.0.0.1'
        finally:
                s.close()

        return IP
