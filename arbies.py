import requests
import time
from datetime import datetime

RPC_URL = 'https://eth-mainnet.g.alchemy.com/v2/<REDACTED>'

token0 = '0x6b175474e89094c44da98b954eedeac495271d0f'
token1 = '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
uniswap = '0xa478c2975ab1ea89e8196811f51a7b7ade33eb11'
sushiswap = '0xc3d03e4f041fd4cd388c549ee2a29a9e5075882f'
shibaswap = '0x8faf958e36c6970497386118030e6297fff8d275'
croswap = '0x60a26d69263ef43e9a68964ba141263f19d71d51'

recon_code = '''
0x
608060405234801561000f575f80fd5b506370a0823160e01b5f5273a478c2
975ab1ea89e8196811f51a7b7ade33eb1160045260206024805f736b175474
e89094c44da98b954eedeac495271d0f5afa506020604460245f73c02aaa39
b223fe8d0a0e5c4f27ead9083c756cc25afa5073c3d03e4f041fd4cd388c54
9ee2a29a9e5075882f6004526020606460245f736b175474e89094c44da98b
954eedeac495271d0f5afa506020608460245f73c02aaa39b223fe8d0a0e5c
4f27ead9083c756cc25afa50738faf958e36c6970497386118030e6297fff8
d275600452602060a460245f736b175474e89094c44da98b954eedeac49527
1d0f5afa50602060c460245f73c02aaa39b223fe8d0a0e5c4f27ead9083c75
6cc25afa507360a26d69263ef43e9a68964ba141263f19d71d516004526020
60e460245f736b175474e89094c44da98b954eedeac495271d0f5afa506020
61010460245f73c02aaa39b223fe8d0a0e5c4f27ead9083c756cc25afa5063
0240bc6b60e21b5f52604061012460045f73a478c2975ab1ea89e8196811f5
1a7b7ade33eb115afa50604061016460045f73c3d03e4f041fd4cd388c549e
e2a29a9e5075882f5afa5060406101a460045f738faf958e36c69704973861
18030e6297fff8d2755afa5060406101e460045f7360a26d69263ef43e9a68
964ba141263f19d71d515afa6102006024f3fe
'''.replace('\n', '')


def recon():
    encoded_recon = requests\
        .post(RPC_URL, json={"id":1,"jsonrpc": "2.0","method":"eth_call","params":[{"data":recon_code},]})\
        .json()\
        .get('result')\
        .replace('0x', '')
    return [
        {
            'address': uniswap,
            'token0_balance': int(encoded_recon[0:64], 16),
            'token1_balance': int(encoded_recon[64:128], 16),
            'reserve0': int(encoded_recon[512:576], 16),
            'reserve1': int(encoded_recon[576:640], 16),
            'fee': 3
        },
        {
            'address': sushiswap,
            'token0_balance': int(encoded_recon[128:192], 16),
            'token1_balance': int(encoded_recon[192:256], 16),
            'reserve0': int(encoded_recon[640:704], 16),
            'reserve1': int(encoded_recon[704:768], 16),
            'fee': 3
        },
        {
            'address': shibaswap,
            'token0_balance': int(encoded_recon[256:320], 16),
            'token1_balance': int(encoded_recon[320:384], 16),
            'reserve0': int(encoded_recon[768:832], 16),
            'reserve1': int(encoded_recon[832:896], 16),
            'fee': 3
        },
        {
            'address': croswap,
            'token0_balance': int(encoded_recon[384:448], 16),
            'token1_balance': int(encoded_recon[448:512], 16),
            'reserve0': int(encoded_recon[896:960], 16),
            'reserve1': int(encoded_recon[960:1024], 16),
            'fee': 3
        }
    ]


def amm_name(amm):
    return {
        uniswap: 'uniswap  ',
        sushiswap: 'sushiswap',
        shibaswap: 'shibaswap',
        croswap: 'croswap  '
    }.get(amm.get('address'))


def get_amount_out(amount_in, reserve_in, reserve_out, fee):
    amount_in_with_fee = int(amount_in - amount_in * fee // 1000)
    return amount_in_with_fee * reserve_out // (reserve_in + amount_in_with_fee)


def simswap(amm, zero_for_one, amount_in):
    reserve0, reserve1 = (amm.get('reserve0'), amm.get('reserve1')) if zero_for_one else (amm.get('reserve1'), amm.get('reserve0'))
    return get_amount_out(amount_in, reserve0, reserve1, amm.get('fee'))


def simarb(primary, secondary, zero_for_one, amount_in):
    return simswap(secondary, not zero_for_one, simswap(primary, zero_for_one, amount_in))


def find_arb(amm, other_amms, amount_in):
    for other_amm in other_amms:
        amount_out = simarb(amm, other_amm, True, amount_in)
        if amount_out > amount_in:
            with open('arbs.txt', 'a') as f:
                f.write(f'arb: {amm_name(amm)} -> {amm_name(other_amm)} , (dai -> eth -> dai) , profit {(amount_out - amount_in) / 1e18:.18f} dai , {datetime.now().strftime("%m/%d/%Y:%H:%M:%S")}\n')
        amount_out = simarb(amm, other_amm, False, amount_in)
        if amount_out > amount_in:
            with open('arbs.txt', 'a') as f:
                f.write(f'arb: {amm_name(amm)} -> {amm_name(other_amm)} , (eth -> dai -> eth) , profit {(amount_out - amount_in) / 1e18:.18f} eth , {datetime.now().strftime("%m/%d/%Y:%H:%M:%S")}\n')


def main():
    amount_in = 0.01e18
    while True:
        amms = recon()
        for amm in amms:
            find_arb(
                amm,
                [other_amm for other_amm in amms if other_amm.get('address') != amm.get('address')],
                amount_in
        )
        time.sleep(1)


if __name__ == '__main__':
    main()
