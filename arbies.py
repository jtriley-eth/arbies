import requests
import time
from datetime import datetime

RPC_URL = 'https://eth-mainnet.g.alchemy.com/v2/<REDACTED>'

me = '0xb47A9B6F062c33ED78630478dFf9056687F840f2'
mock_runner = '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266'
token0 = '0x6b175474e89094c44da98b954eedeac495271d0f'
token1 = '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
uniswap = '0xa478c2975ab1ea89e8196811f51a7b7ade33eb11'
sushiswap = '0xc3d03e4f041fd4cd388c549ee2a29a9e5075882f'
shibaswap = '0x8faf958e36c6970497386118030e6297fff8d275'
croswap = '0x60a26d69263ef43e9a68964ba141263f19d71d51'

recon_code = '''
0x
608060405234801561000f575f80fd5b506370a0823160e01b5f5273a478c297
5ab1ea89e8196811f51a7b7ade33eb1160045260206024805f736b175474e890
94c44da98b954eedeac495271d0f5afa506020604460245f73c02aaa39b223fe
8d0a0e5c4f27ead9083c756cc25afa5073c3d03e4f041fd4cd388c549ee2a29a
9e5075882f6004526020606460245f736b175474e89094c44da98b954eedeac4
95271d0f5afa506020608460245f73c02aaa39b223fe8d0a0e5c4f27ead9083c
756cc25afa50738faf958e36c6970497386118030e6297fff8d2756004526020
60a460245f736b175474e89094c44da98b954eedeac495271d0f5afa50602060
c460245f73c02aaa39b223fe8d0a0e5c4f27ead9083c756cc25afa507360a26d
69263ef43e9a68964ba141263f19d71d51600452602060e460245f736b175474
e89094c44da98b954eedeac495271d0f5afa50602061010460245f73c02aaa39
b223fe8d0a0e5c4f27ead9083c756cc25afa50630240bc6b60e21b5f52604061
012460045f73a478c2975ab1ea89e8196811f51a7b7ade33eb115afa50604061
016460045f73c3d03e4f041fd4cd388c549ee2a29a9e5075882f5afa50604061
01a460045f738faf958e36c6970497386118030e6297fff8d2755afa50604061
01e460045f7360a26d69263ef43e9a68964ba141263f19d71d515afa61020060
24f3fe
'''.replace('\n', '')

runner_code = '''
0x
60806040523615610152576000803573c02aaa39b223fe8d0a0e5c4f27ead908
3c756cc28252736b175474e89094c44da98b954eedeac495271d0f6020528180
60a4818060208660fa1c169586519073a478c2975ab1ea89e8196811f51a7b7a
de33eb11835273c3d03e4f041fd4cd388c549ee2a29a9e5075882f602052738f
af958e36c6970497386118030e6297fff8d2756040527360a26d69263ef43e9a
68964ba141263f19d71d51608052828086818060608660f81c16516020826044
818060608c60f61c16519c63a9059cbb60e01b82528660045260018060fb1b03
8d166024525af173b47a9b6f062c33ed78630478dff9056687f840f233141682
51169663022c0d9f60e01b835282600452826024528860445260806064528260
84526020359060ff1c1560051b600401525af116968260045282602452306044
5260403590600401525af1166101525780fd5b00fea164736f6c634300081800
0a
'''.replace('\n', '')


def recon():
    encoded_recon = requests\
        .post(RPC_URL, json={"id":1,"jsonrpc": "2.0","method":"eth_call","params":[{"data":recon_code}]})\
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


def run_hypothetical(zero_for_one, amm0, amm1, amount_in, amount0_out, amount1_out):
    zero_for_one = int(zero_for_one)
    amm0 = [uniswap, sushiswap, shibaswap, croswap].index(amm0.get('address'))
    amm1 = [uniswap, sushiswap, shibaswap, croswap].index(amm1.get('address'))
    arg0 = hex(zero_for_one << 255 | amm0 << 253 | amm1 << 251 | int(amount_in))
    arg1 = hex(amount0_out).replace('0x', '').zfill(64)
    arg2 = hex(amount1_out).replace('0x', '').zfill(64)
    calldata = arg0 + arg1 + arg2
    print(runner_code)

    tx_data = {
            "from": me,
            "to": mock_runner,
            "data": calldata
    }

    state_diff = {
        token0: {'stateDiff':{'0xbc40fbf4394cd00f78fae9763b0c2c71b21ea442c42fdadc5b720537240ebac1': f"{int(1e18):#0{66}x}"}},
        token1: {'stateDiff':{'0xc651ee22c6951bb8b5bd29e8210fb394645a94315fe10eff2cc73de1aa75c137': f"{int(1e18):#0{66}x}"}},
        mock_runner: {'code': runner_code},
    }

    tx_res = requests\
        .post(RPC_URL, json={"jsonrpc": "2.0","method":"eth_call","params":[tx_data, "pending", state_diff],"id":1})\
        .json()

    return tx_res


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
            print(f'arb: {amm_name(amm)} -> {amm_name(other_amm)} , (dai -> eth -> dai) , profit {(amount_out - amount_in) / 1e18:.18f} dai , {datetime.now().strftime("%m/%d/%Y:%H:%M:%S")}\n')
            print(run_hypothetical(False, amm, other_amm, amount_in, simswap(other_amm, False, amount_out), amount_out))
        amount_out = simarb(amm, other_amm, False, amount_in)
        if amount_out > amount_in:
            print(f'arb: {amm_name(amm)} -> {amm_name(other_amm)} , (eth -> dai -> eth) , profit {(amount_out - amount_in) / 1e18:.18f} eth , {datetime.now().strftime("%m/%d/%Y:%H:%M:%S")}\n')
            print(run_hypothetical(True, amm, other_amm, amount_in, simswap(amm, True, amount_in), amount_out))


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
