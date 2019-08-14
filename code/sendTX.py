def sendTX(msg):
    '''
    PURPOSE:  send transaction to the Tangle

    IMPORTS:
    from typing import Optional, Text
    import requests
    from iota import Iota
    from iota import ProposedTransaction
    from iota import Address
    from iota import Tag
    from iota import TryteString
    from json import load

    INPUT:
        address from a seed different than the one in this script

    OUTPUT:
        TX to devnet
    '''
    seed =    'AUTOGARDENERSEED99999999999999999999999999999999999999999999999999999999999999999999999999'
    address = 'ZNJWDJBGQVLCNJIRXPDUKHESBYXGFADCKAUCXFZFCWEOUJOJIDZHDCMVQQTEMZIMPOXFCTM9QSNNUZVBXMHVKFPSF9'
    api = Iota('https://nodes.devnet.iota.org:443', seed)
    tx = ProposedTransaction(
        address=Address(address),
        message=TryteString.from_unicode(msg),
        tag=Tag('LAUTOGARDENER'),
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
