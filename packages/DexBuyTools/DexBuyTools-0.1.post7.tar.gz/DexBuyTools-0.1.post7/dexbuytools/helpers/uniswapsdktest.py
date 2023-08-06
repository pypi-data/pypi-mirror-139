import web3
from uniswap import Uniswap
from web3 import Web3

RPC_URL = "https://mainnet.infura.io/v3/b5a6bdf5435b42128bdec7acaaa1b8f0"

weth_address = Web3.toChecksumAddress('0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2')
token_address = Web3.toChecksumAddress('0x2D569962C9119285995256E8B9f7622abaF6Bc24') #some shitcoin
#token_address = Web3.toChecksumAddress('0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48') #usdc

uniswap_v2 = Uniswap(address=None, private_key=None, version=2, provider=RPC_URL)
uniswap_v3 = Uniswap(address=None, private_key=None, version=3, provider=RPC_URL)

output_v2 = None
output_v3 = None

try:
    output_v2 = uniswap_v2.get_price_input(weth_address, token_address, int(0.1*10**18))
    output_v3 = uniswap_v3.get_price_input(weth_address, token_address, int(0.1*10**18))
except web3.exceptions.ContractLogicError as e:
    pass

pass

# val1 = None
# val2 = None
#
# try:
#     val1 = 1
#     raise Exception
# except Exception as e:
#     pass
#
# pass