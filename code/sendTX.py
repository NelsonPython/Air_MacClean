'''
Run using python 2.7 because PYOTA is compatible with Python 2.7 but not Python 3.7
'''
from iota import Iota
from iota import ProposedTransaction
from iota import Address
from iota import Tag
from iota import TryteString
from json import load

def sendTX(msg):
    '''
    PURPOSE:  send transaction to the Tangle

    INPUT:
        address from a seed different than the one in this script

    OUTPUT:
        TX to devnet
    '''
    seed =    'SEED99999999999999999999999999999999999999999999999999999999999999999999999999999'
    address = 'ADDRESS9FROM9DIFFERENT9SEED999999999999999999999999999999999999999999999999999999'
    api = Iota('https://nodes.devnet.iota.org:443', seed)
    tx = ProposedTransaction(
        address=Address(address),
        message=TryteString.from_unicode(msg),
        tag=Tag('YOURTAG'),
        value=0
    )
    try:
        tx = api.prepare_transfer(transfers=[tx])
    except Exception as e:
        print("Check prepare_transfer ", e)
        raise
    try:
        result = api.send_trytes(tx['trytes'],depth=3,min_weight_magnitude=9)
    except:
        print("Check send_trytes")

if __name__=="__main__":
        f = open("airquality.csv","r")
        msg = f.readlines()[-1]
        msg = msg.strip("\n")
        print(msg)
        try:
            sendTX(msg)
        except e:
            print("Check devnet",e)
        f.close()

