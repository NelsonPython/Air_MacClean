def textStatus(msg):
        '''
        PURPOSE:  Text using IFTTT.com
                  you need your own API KEY
        '''
        try:
                r = requests.post(url="https://maker.ifttt.com/trigger/IP/with/key/YOUR-KEY=HERE", data={"value1": msg})
                print("Text status ", r.status_code, r.reason)
        except:
                print("Text status ", r.status_code, r.reason)

